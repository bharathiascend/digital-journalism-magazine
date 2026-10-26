import { getCollection, type CollectionEntry } from 'astro:content';

export type StoryEntry = CollectionEntry<'stories'>;

export interface SectionMeta {
  id: 'national' | 'politics' | 'lifestyle' | 'sports' | 'analysis';
  label: string;
  description: string;
  shortLabel: string;
}

export const SECTIONS: SectionMeta[] = [
  {
    id: 'national',
    label: 'National',
    shortLabel: 'National',
    description: 'In-depth reporting and sustained inquiry into institutions, environment, public life, and civic mobilisation across the nation.',
  },
  {
    id: 'politics',
    label: 'Politics',
    shortLabel: 'Politics',
    description: 'Critical analysis of power, policy debates, and political movements beyond short-term election cycles.',
  },
  {
    id: 'analysis',
    label: 'News Analysis',
    shortLabel: 'Analysis',
    description: 'Forensic media framing analyses, government accountability deep dives, and systemic institutional critiques.',
  },
  {
    id: 'lifestyle',
    label: 'Lifestyle & Entertainment',
    shortLabel: 'Lifestyle',
    description: 'Culture, society, arts, cinema, and everyday life explored with nuance, rigor, and critical distance.',
  },
  {
    id: 'sports',
    label: 'Sports',
    shortLabel: 'Sports',
    description: 'Long-form perspectives on athletics, sporting culture, community competitions, and the human dimension of movement.',
  },
];

export interface FormatMeta {
  id: 'article' | 'blog' | 'video' | 'podcast' | 'photo-feature' | 'poll-report';
  label: string;
  badgeLabel: string;
  description: string;
}

export const FORMATS: FormatMeta[] = [
  {
    id: 'article',
    label: 'Articles & Essays',
    badgeLabel: 'Article',
    description: 'Long-form investigative reporting, reported features, and deeply researched essays.',
  },
  {
    id: 'blog',
    label: 'Essays & Blog',
    badgeLabel: 'Essay',
    description: 'Reflective dispatches, personal commentary, and critical readings from student contributors.',
  },
  {
    id: 'photo-feature',
    label: 'Photo Features',
    badgeLabel: 'Photo Feature',
    description: 'Visual journalism, photo essays, and observational photography documenting communities and events.',
  },
  {
    id: 'podcast',
    label: 'Podcasts',
    badgeLabel: 'Podcast',
    description: 'Spoken conversations, audio reporting, and thoughtful dialogue on pressing public concerns.',
  },
  {
    id: 'video',
    label: 'Video Explainers',
    badgeLabel: 'Video Explainer',
    description: 'Mobile-first vertical video explainers breaking down complex developments with clarity.',
  },
  {
    id: 'poll-report',
    label: 'Opinion Poll Reports',
    badgeLabel: 'Poll Report',
    description: 'Independent campus survey findings, statistical distributions, and methodology summaries.',
  },
];

export interface StoryFilterOptions {
  includeDemos?: boolean;
}

/**
 * Safe release gate:
 * - Production builds (`import.meta.env.PROD === true` and ASTRO_SHOW_DEMOS !== 'true'):
 *   Strictly excludes demonstration records (`isDemo: true`) and unapproved records (`status !== 'approved'`).
 *   This ensures no demo records or draft notes ever leak into a production deployment.
 * - Local development (`import.meta.env.DEV === true` or ASTRO_SHOW_DEMOS === 'true'):
 *   Includes demonstration records to enable thorough layout, responsive, and typography review.
 */
export async function getPublishableStories(options: StoryFilterOptions = {}): Promise<StoryEntry[]> {
  const all = await getCollection('stories');
  const allowDemos =
    options.includeDemos ??
    (import.meta.env.DEV || import.meta.env.ASTRO_SHOW_DEMOS === 'true');

  return all.filter((story) => {
    // Release gate check 1: demonstration records
    if (story.data.isDemo && !allowDemos) {
      return false;
    }
    // Release gate check 2: production approval status
    if (import.meta.env.PROD && !allowDemos) {
      return story.data.status === 'approved' && !story.data.isDemo;
    }
    return true;
  });
}

export function getSectionMeta(sectionId: string): SectionMeta | undefined {
  return SECTIONS.find((s) => s.id === sectionId);
}

export function getFormatMeta(formatId: string): FormatMeta | undefined {
  return FORMATS.find((f) => f.id === formatId);
}
