/**
 * Разовый конвертер: HTML-прототип разбора -> MDX для контент-коллекции.
 * Запуск: node scripts/html-to-mdx.mjs <входной .html> <выходной .mdx>
 *
 * Оставлен в репозитории как справка по тому, во что превращается разметка
 * блоков, если понадобится перенести ещё один старый прототип.
 */
import { readFileSync, writeFileSync } from 'node:fs';

const [, , inPath, outPath] = process.argv;
if (!inPath || !outPath) {
  console.error('usage: node scripts/html-to-mdx.mjs <in.html> <out.mdx>');
  process.exit(1);
}

let html = readFileSync(inPath, 'utf8');

// только содержимое <main>
const main = html.match(/<main[^>]*>([\s\S]*?)<\/main>/);
if (!main) {
  console.error('no <main> found');
  process.exit(1);
}
let s = main[1];

// --- разделы -------------------------------------------------------------
// <div class="sec-head"><span class="num">01</span><h2>Заголовок<button…></h2></div>
s = s.replace(
  /<section id="([^"]+)">\s*<div class="sec-head">\s*<span class="num">([^<]+)<\/span>\s*<h2>([\s\S]*?)<button[\s\S]*?<\/button><\/h2>\s*<\/div>/g,
  (_m, id, num, title) =>
    `<Section num="${num}" id="${id}" title="${title.trim()}">`
);
s = s.replace(/<\/section>/g, '</Section>');

// --- блоки регистра ------------------------------------------------------
const blocks = [
  ['blk interp', 'Interp'],
  ['blk voice', 'Voice'],
  ['blk unknown', 'Unknown'],
  ['blk', 'Fact'],
];

// Разбираем вручную, чтобы корректно найти закрывающий </div> с учётом вложенности.
function convertBlocks(src) {
  let out = '';
  let i = 0;
  const openRe = /<div class="(blk(?: interp| voice| unknown)?)">\s*<span class="tag">[^<]*<\/span>/g;
  openRe.lastIndex = 0;
  let m;
  while ((m = openRe.exec(src))) {
    const cls = m[1];
    const comp = blocks.find(([c]) => c === cls)[1];
    out += src.slice(i, m.index);
    // ищем закрывающий </div> с учётом вложенных <div>
    let depth = 1;
    let j = m.index + m[0].length;
    const tagRe = /<div\b[^>]*>|<\/div>/g;
    tagRe.lastIndex = j;
    let t;
    while ((t = tagRe.exec(src))) {
      if (t[0] === '</div>') depth--;
      else depth++;
      if (depth === 0) break;
    }
    const inner = src.slice(m.index + m[0].length, t.index);
    out += `<${comp}>\n${convertBlocks(inner).trim()}\n</${comp}>`;
    i = t.index + '</div>'.length;
    openRe.lastIndex = i;
  }
  out += src.slice(i);
  return out;
}
s = convertBlocks(s);

// --- обёртка таблиц ------------------------------------------------------
s = s.replace(/<div class="tbl-wrap">/g, '<Tbl>');
// закрывающие </div> у tbl-wrap уже съедены? нет — они остались; закроем по парам
// (внутри tbl-wrap нет вложенных div, поэтому первая же </div> — наша)
s = s.replace(/<Tbl>([\s\S]*?)<\/div>/g, (_m, inner) => `<Tbl>${inner}</Tbl>`);

// --- перекрёстная ссылка -------------------------------------------------
s = s.replace(
  /<div class="xref">\s*<span class="k">[^<]*<\/span>\s*<div>([\s\S]*?)<\/div>\s*<\/div>/g,
  (_m, inner) => `<Xref>\n${inner.trim()}\n</Xref>`
);

// --- источники в тексте --------------------------------------------------
s = s.replace(
  /<a class="src" href="([^"]+)"[^>]*>([\s\S]*?)<\/a>/g,
  (_m, href, text) => `<Src href="${href}">${text}</Src>`
);
s = s.replace(/<span class="src2">([\s\S]*?)<\/span>/g, (_m, t) => `<Src2>${t}</Src2>`);
s = s.replace(/<span class="unver">[^<]*<\/span>/g, '<Unver />');

// комментарии HTML в MDX недопустимы
s = s.replace(/<!--[sS]*?-->/g, '');

// --- JSX-совместимость ---------------------------------------------------
s = s.replace(/<br>/g, '<br />');
s = s.replace(/<hr>/g, '<hr />');
s = s.replace(/&nbsp;/g, ' ');

// --- отступы -------------------------------------------------------------
// строки с 4+ пробелами в начале markdown считает блоком кода, поэтому
// сносим отступы полностью
s = s
  .split('\n')
  .map((l) => l.replace(/^\s+/, ''))
  .join('\n')
  .replace(/\n{3,}/g, '\n\n')
  .trim();

writeFileSync(outPath, s + '\n', 'utf8');
console.log(`wrote ${outPath} (${s.length} chars)`);
