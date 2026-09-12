/**
 * Экспорт разбора в PDF для публикации в канале.
 *
 *   npm run pdf -- upenn
 *   npm run pdf -- cornell jhu duke
 *   npm run pdf              (все разборы)
 *
 * Печатает страницу с дев-сервера через headless Chrome. Печатные стили
 * лежат в src/styles/global.css в блоке @media print: они убирают шапку,
 * оглавление и кнопки, разворачивают вёрстку в одну колонку и дописывают
 * адреса ссылок, потому что на бумаге они не кликаются.
 */
import { spawn, spawnSync } from 'node:child_process';
import { mkdirSync, readdirSync, existsSync } from 'node:fs';
import { join, resolve } from 'node:path';

const PORT = 4321;
const OUT = resolve('exports');
const CONTENT = resolve('src/content/universities');

const CHROME = [
  'C:/Program Files/Google/Chrome/Application/chrome.exe',
  'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe',
  'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe',
].find((p) => existsSync(p));

if (!CHROME) {
  console.error('Не найден Chrome или Edge — без них PDF не собрать.');
  process.exit(1);
}

// какие разборы печатаем
let slugs = process.argv.slice(2);
if (slugs.length === 0) {
  slugs = readdirSync(CONTENT)
    .filter((f) => f.endsWith('.mdx') && !f.startsWith('_'))
    .map((f) => f.replace(/\.mdx$/, ''));
}

// имя университета из frontmatter — чтобы файл назывался по-человечески
import { readFileSync } from 'node:fs';
function titleOf(slug) {
  try {
    const src = readFileSync(join(CONTENT, `${slug}.mdx`), 'utf8');
    const m = src.match(/^name:\s*(.+)$/m);
    return m ? m[1].trim().replace(/^(["'])(.*)\1$/, '$2') : slug;
  } catch {
    return slug;
  }
}

async function waitForServer(url, tries = 60) {
  for (let i = 0; i < tries; i++) {
    try {
      const r = await fetch(url);
      if (r.ok) return true;
    } catch {}
    await new Promise((r) => setTimeout(r, 500));
  }
  return false;
}

const dev = spawn('npm', ['run', 'dev', '--', '--port', String(PORT)], {
  stdio: 'ignore',
  shell: true,
});

try {
  const ok = await waitForServer(`http://localhost:${PORT}/`);
  if (!ok) throw new Error('дев-сервер не поднялся');

  mkdirSync(OUT, { recursive: true });

  for (const slug of slugs) {
    const file = join(OUT, `${titleOf(slug)} — разбор.pdf`);
    const res = spawnSync(
      CHROME,
      [
        '--headless',
        '--disable-gpu',
        '--no-first-run',
        `--user-data-dir=${resolve('.chrome-pdf-profile')}`,
        '--no-pdf-header-footer',
        `--print-to-pdf=${file}`,
        `http://localhost:${PORT}/u/${slug}`,
      ],
      { encoding: 'utf8' }
    );
    if (res.status === 0) console.log(`✓ ${file}`);
    else console.error(`✗ ${slug}: ${res.stderr?.slice(0, 200)}`);
  }
} finally {
  dev.kill();
  // на Windows npm запускается через оболочку, поэтому добиваем дерево процессов
  if (process.platform === 'win32' && dev.pid) {
    spawnSync('taskkill', ['/pid', String(dev.pid), '/T', '/F'], { stdio: 'ignore' });
  }
}
