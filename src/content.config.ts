import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

/**
 * Одна запись = один университет = один .mdx файл в src/content/universities/.
 *
 * Frontmatter — это то, по чему работают фильтры на главной и таблица
 * сравнения. Тело файла — сам разбор.
 *
 * Уровни соответствия (fit): 0 — не подходит, 4 — очень высокое.
 * Для admissions это не соответствие, а сложность: 4 = очень сложно.
 */

const fitItem = z.object({
  score: z.number().int().min(0).max(4),
  note: z.string(),
});

const universities = defineCollection({
  // файлы с подчёркиванием в начале — служебные (шаблон, черновики), их не публикуем
  loader: glob({ pattern: ['**/*.mdx', '!**/_*.mdx'], base: './src/content/universities' }),
  schema: z.object({
    name: z.string(),
    city: z.string(),
    country: z.string(),
    countryCode: z.string().length(2),
    founded: z.number().int(),

    // короткий тезис на карточку и в шапку страницы
    thesis: z.string(),
    // акцентный цвет университета (его институциональный)
    accent: z.string().default('#A4161A'),
    accentDark: z.string().default('#E4736C'),

    // под какой профиль читателя написаны разделы «Ты × универ» и вердикт
    profile: z.string(),
    // номер выпуска в канале, если есть
    issue: z.number().int().optional(),
    updated: z.coerce.date(),
    pdf: z.string().regex(/^\/downloads\/[a-z0-9-]+\.pdf$/).optional(),

    // ---- поступление ----
    acceptanceRate: z.number().nullable(),
    acceptanceNote: z.string().optional(),
    statsNote: z.string().optional(),
    satRange: z.tuple([z.number(), z.number()]).nullable(),
    actRange: z.tuple([z.number(), z.number()]).nullable(),
    testPolicy: z.enum(['required', 'optional', 'blind', 'unknown']),
    separateCollegeAdmission: z.boolean().default(false),

    // ---- деньги, всё в USD в год ----
    costOfAttendance: z.tuple([z.number(), z.number()]).nullable(),
    meetsFullNeed: z.boolean(),
    aidForInternationals: z.boolean(),
    avgGrant: z.number().nullable(),
    avgPackage: z.number().nullable(),
    meritAid: z.boolean(),
    needBlind: z.boolean().default(false),

    // ---- профиль ----
    strengths: z.array(z.string()).default([]),
    campusType: z.enum(['college town', 'big city', 'suburb', 'campus bubble']),
    climate: z.string().optional(),

    fit: z.object({
      academic: fitItem,
      research: fitItem,
      intellectual: fitItem,
      culture: fitItem,
      financial: fitItem,
      admissions: fitItem,
    }),

    sources: z.object({
      official: z.array(z.object({ label: z.string(), url: z.string().optional() })).default([]),
      data: z.array(z.object({ label: z.string(), url: z.string().optional() })).default([]),
      reviews: z.array(z.object({ label: z.string(), url: z.string().optional() })).default([]),
      news: z.array(z.object({ label: z.string(), url: z.string().optional() })).default([]),
    }),

    // предупреждение о вторичных источниках, если оно нужно этому разбору
    sourceCaveat: z.string().optional(),
  }),
});

const scholarships = defineCollection({
  loader: glob({ pattern: ['**/*.mdx', '!**/_*.mdx'], base: './src/content/scholarships' }),
  schema: z.object({
    name: z.string(),
    country: z.string(),
    thesis: z.string(),
    accent: z.string(),
    accentDark: z.string(),
    profile: z.string(),
    updated: z.coerce.date(),
    cycle: z.string(),
    pdf: z.string().regex(/^\/downloads\/[a-z0-9-]+\.pdf$/),
    sources: z.array(z.object({ label: z.string(), url: z.string().url() })),
  }),
});

export const collections = { universities, scholarships };
