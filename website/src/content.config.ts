import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

const stories = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/stories' }),
  schema: z.object({
    title: z.string(),
    slug: z.string().regex(/^[a-z0-9-]+$/),
    section: z.enum(['national', 'politics', 'lifestyle', 'sports', 'analysis']),
    format: z.enum(['article', 'blog', 'video', 'podcast', 'photo-feature', 'poll-report']),
    status: z.enum(['draft', 'needs-review', 'approved']),
    isDemo: z.boolean().default(false),
    subtitle: z.string().optional(),
    excerpt: z.string().optional(),
    publishedAt: z.union([
  z.string(),
  z.date().transform((date) =>
    date.toISOString().slice(0, 10)
  ),
]).optional(),
    dateLabel: z.string().optional(),
    authors: z
      .array(
        z.object({
          name: z.string(),
          role: z.string().default('Writer'),
        })
      )
      .optional(),
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
        variant: z.enum(['paper', 'arches', 'orbit', 'frames', 'sound']).default('paper'),
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
          caption: z.string(),
          credit: z.string().optional(),
          reviewNotice: z.string().optional(),
        })
      )
      .optional(),
    pollData: z
      .object({
        question: z.string(),
        sampleSize: z.string().optional(),
        methodologyNote: z.string().optional(),
        results: z.array(
          z.object({
            label: z.string(),
            percentage: z.number(),
            count: z.number().optional(),
          })
        ),
        charts: z
          .array(
            z.object({
              src: z.string(),
              caption: z.string(),
            })
          )
          .optional(),
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
