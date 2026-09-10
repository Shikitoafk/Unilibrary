/** Форматирование чисел и подписи уровней — общее для карточек, сравнения и страницы разбора. */

const nbsp = ' ';

export function usd(n: number | null | undefined): string {
  if (n == null) return '—';
  return '$' + n.toLocaleString('ru-RU').replace(/\s/g, nbsp);
}

export function usdShort(n: number | null | undefined): string {
  if (n == null) return '—';
  if (n >= 1000) return '$' + (n / 1000).toFixed(1).replace('.', ',') + nbsp + 'тыс.';
  return '$' + n;
}

export function usdRange(r: [number, number] | null | undefined): string {
  if (!r) return '—';
  const [a, b] = r;
  if (a === b) return usdShort(a);
  return (
    '$' +
    (a / 1000).toFixed(1).replace('.', ',') +
    '–' +
    (b / 1000).toFixed(1).replace('.', ',') +
    nbsp +
    'тыс.'
  );
}

export function pct(n: number | null | undefined): string {
  if (n == null) return '—';
  return String(n).replace('.', ',') + '%';
}

export function range(r: [number, number] | null | undefined): string {
  if (!r) return '—';
  return r[0] + '–' + r[1];
}

export function yesNo(v: boolean): string {
  return v ? 'да' : 'нет';
}

export const testPolicyLabel: Record<string, string> = {
  required: 'обязательны',
  optional: 'по желанию',
  blind: 'не смотрят',
  unknown: '—',
};

export const fitNames: Record<string, string> = {
  academic: 'Академическое',
  research: 'Исследовательское',
  intellectual: 'Интеллектуальное',
  culture: 'Культурное',
  financial: 'Финансовое',
  admissions: 'Поступление',
};

export const fitOrder = [
  'academic',
  'research',
  'intellectual',
  'culture',
  'financial',
  'admissions',
] as const;

/** «10 сентября 2026» — без хвостового «г.», чтобы не плодить двойную точку в конце фразы. */
export function dateRu(d: Date): string {
  return d
    .toLocaleDateString('ru-RU', { day: 'numeric', month: 'long', year: 'numeric' })
    .replace(/\s*г\.$/, '');
}
