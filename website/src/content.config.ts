import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

const stories = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/stories' }),
  schema: z.object({
    title: z.string(),
    slug: z.preprocess((val) => {
      if (typeof val === 'string') {
        return val.trim().toLowerCase().replace(/[^a-z0-9-]/g, '-');
      }
      return val;
    }, z.string().regex(/^[a-z0-9-]+$/)),
    section: z.enum(['national', 'politics', 'lifestyle', 'sports', 'analysis']),
    format: z.enum(['article', 'blog', 'video', 'podcast', 'photo-feature', 'poll-report']),
    status: z.enum(['draft', 'needs-review', 'approved']).default('draft'),
    isDemo: z.preprocess((val) => {
      if (typeof val === 'string') return val.toLowerCase() === 'true';
      return Boolean(val);
    }, z.boolean().default(false)),
    subtitle: z.string().optional(),
    excerpt: z.string().optional(),
    publishedAt: z.preprocess((val) => {
      if (val === null || val === undefined || val === '') return undefined;
      if (val instanceof Date) return val.toISOString().slice(0, 10);
      if (typeof val === 'string') {
        const trimmed = val.trim();
        if (!trimmed) return undefined;
        if (/^\d{4}-\d{2}-\d{2}/.test(trimmed)) {
          return trimmed.slice(0, 10);
        }
        const parsed = new Date(trimmed);
        if (!isNaN(parsed.getTime())) {
          return parsed.toISOString().slice(0, 10);
        }
        return trimmed;
      }
      return val;
    }, z.string().optional()),
    dateLabel: z.string().optional(),
    authors: z
      .array(
        z.object({
          name: z.string().optional().default('Staff Reporter'),
          role: z.string().optional().default('Writer'),
        })
      )
      .optional()
      .default([]),
    // Internal provenance & editorial notes: kept out of deployable output
    provenance: z
      .object({
        sourceFile: z.string().optional(),
        category: z.string().optional(),
        editorialNotes: z.string().optional(),
      })
      .optional(),
    // Format-specific presentation & media fields
    heroImage: z
      .object({
        src: z.string().optional(),
        alt: z.string().optional(),
        variant: z.enum(['paper', 'arches', 'orbit', 'frames', 'sound']).catch('paper').default('paper'),
        caption: z.string().optional(),
        credit: z.string().optional(),
      })
      .optional(),
    video: z
      .object({
        duration: z.string().optional(),
        mediaUrl: z.string().optional(),
        poster: z.string().optional(),
        transcriptPlaceholder: z.string().optional(),
      })
      .optional(),
    podcast: z
      .object({
        duration: z.string().optional(),
        mediaUrl: z.string().optional(),
        episodeNotes: z.string().optional(),
        audioPlaceholder: z.string().optional(),
      })
      .optional(),
    photoGallery: z
      .array(
        z.object({
          src: z.string().optional(),
          alt: z.string().optional(),
          variant: z.enum(['paper', 'arches', 'orbit', 'frames', 'sound']).optional(),
          caption: z.string().optional().default(''),
          credit: z.string().optional(),
          reviewNotice: z.string().optional(),
        })
      )
      .optional()
      .default([]),
    pollData: z
      .object({
        question: z.string().optional().default(''),
        sampleSize: z.string().optional(),
        methodologyNote: z.string().optional(),
        results: z
          .array(
            z.object({
              label: z.string().optional().default(''),
              percentage: z.coerce.number().optional().default(0),
              count: z.coerce.number().optional(),
            })
          )
          .optional()
          .default([]),
        charts: z
          .array(
            z.object({
              src: z.string().optional(),
              caption: z.string().optional().default(''),
            })
          )
          .optional()
          .default([]),
      })
      .optional(),
    editorialReview: z
      .object({
        reviewFlags: z.array(z.string()).optional(),
        missingItems: z.array(z.string()).optional(),
        notes: z.string().optional(),
      })
      .optional(),
  }),
});

export const collections = { stories };
