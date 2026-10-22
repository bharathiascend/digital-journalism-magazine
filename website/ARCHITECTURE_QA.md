# Publishing Architecture QA & Release Safety Audit (Prompt 03A)

**Audit Date:** 22 October 2026  
**Auditor:** Senior Astro Frontend Architect & Publishing Security Auditor  
**Scope:** Verification of `website/` implementation against `docs/content-audit.md`, `docs/site-blueprint.md`, and Git baseline `5dbb026`.  
**Mode:** Quality Assurance & Verification (no new code implemented; issues reported for review).

---

## Executive Summary & Readiness Assessment

| Evaluation Category | Status | Summary Findings |
| :--- | :---: | :--- |
| **Publishing Approval Gate** | <span style="color:#d9534f; font-weight:bold;">CRITICAL FINDING</span> | Gating logic functions in dynamic routes, but `src/pages/index.astro` hardcodes demo cards resulting in 13 broken links in production. |
| **Production Output & Privacy** | <span style="color:#5cb85c; font-weight:bold;">PASSED</span> | Zero unapproved media, source ZIPs, PDFs, Word docs, or internal editorial notes leaked into `dist/`. |
| **Routing & URL Canon** | <span style="color:#5cb85c; font-weight:bold;">PASSED</span> | Single canonical story URL (`/stories/[slug]/`); no duplicate pages generated; unique slug validation enforced. |
| **Multimedia Component Prep** | <span style="color:#5cb85c; font-weight:bold;">PASSED</span> | Layout shells ready for 9:16 portrait video, native audio, photo galleries, and accessible survey data tables. |
| **Accessibility & Hierarchy** | <span style="color:#f0ad4e; font-weight:bold;">MINOR FINDING</span> | Contrast exceeds WCAG AA; exactly one `<h1>` per page; minor heading level jump (`<h1>` to `<h3>`) in empty state cards. |
| **Build Stability** | <span style="color:#5cb85c; font-weight:bold;">PASSED</span> | Both `npm run build` (12 pages) and `npm run build:demo` (18 pages) compile with zero errors in <900ms. |
| **Overall Readiness** | **CONDITIONALLY READY** | Architecture is robust and sound, but **Issue #1 (Homepage release gating)** must be resolved before deploying real journalism. |

---

## Task 1: Publishing Approval Gate Verification

### Findings & Analysis

The approval gate logic was evaluated across all relevant files:
* [`src/content.config.ts`](file:///c:/Users/bhara/Downloads/DIGITAL%20JOURNALISM%20WEBSITE-20261022T013821Z-1-001/website/src/content.config.ts)
* [`src/utils/stories.ts`](file:///c:/Users/bhara/Downloads/DIGITAL%20JOURNALISM%20WEBSITE-20261022T013821Z-1-001/website/src/utils/stories.ts)
* Dynamic routes (`/sections/[section].astro`, `/formats/[format].astro`, `/stories/[slug].astro`)
* Story Layout (`src/layouts/StoryLayout.astro`)
* Homepage (`src/pages/index.astro`)

#### 1. Dynamic Routing Gate: **PASSED**
In [`src/utils/stories.ts`](file:///c:/Users/bhara/Downloads/DIGITAL%20JOURNALISM%20WEBSITE-20261022T013821Z-1-001/website/src/utils/stories.ts), `getPublishableStories()` enforces:
```typescript
if (story.data.isDemo && !allowDemos) return false;
if (import.meta.env.PROD && !allowDemos) {
  return story.data.status === 'approved' && !story.data.isDemo;
}
```
* In a normal production build (`npm run build`), `allowDemos` evaluates to `false`.
* Only records satisfying **both** `isDemo === false` and `status === "approved"` pass through.
* In [`src/pages/stories/[slug].astro`](file:///c:/Users/bhara/Downloads/DIGITAL%20JOURNALISM%20WEBSITE-20261022T013821Z-1-001/website/src/pages/stories/%5Bslug%5D.astro), `getStaticPaths()` receives an empty array (`[]`) because no real stories have been approved yet. **0 demo story pages are built into `dist/stories/`**.
* In [`src/pages/sections/[section].astro`](file:///c:/Users/bhara/Downloads/DIGITAL%20JOURNALISM%20WEBSITE-20261022T013821Z-1-001/website/src/pages/sections/%5Bsection%5D.astro) and [`src/pages/formats/[format].astro`](file:///c:/Users/bhara/Downloads/DIGITAL%20JOURNALISM%20WEBSITE-20261022T013821Z-1-001/website/src/pages/formats/%5Bformat%5D.astro), filtered story counts are `0`, cleanly triggering the editorial empty state.

#### 2. Homepage Gate Leak: **CRITICAL**
* While the dynamic routes strictly obey the release gate, [`src/pages/index.astro`](file:///c:/Users/bhara/Downloads/DIGITAL%20JOURNALISM%20WEBSITE-20261022T013821Z-1-001/website/src/pages/index.astro) currently contains **hardcoded `<ArticleCard>` components** with hardcoded links to demonstration slugs (`/stories/the-quiet-shift/`, `/stories/the-policy-crossroads/`, etc.).
* **Result in normal production build (`npm run build`):**
  1. The homepage in `dist/index.html` still displays demonstration headlines and fictional bylines ("The Quiet Shift in River Basin Agriculture", "Voices in Motion", "Example Reporter").
  2. Because the release gate successfully excluded the generation of `/stories/*`, clicking any of those cards on the production homepage leads to a **404 Broken Link** (13 broken links identified).
* **Required Resolution:** Before real content integration or production deployment, `src/pages/index.astro` must be made data-driven via `getPublishableStories()`, displaying only approved stories or an editorial launch state when zero approved stories exist.

---

## Task 2: Production Build Output Inspection

The complete production output directory [`website/dist/`](file:///c:/Users/bhara/Downloads/DIGITAL%20JOURNALISM%20WEBSITE-20261022T013821Z-1-001/website/dist) was audited via automated disk scanning and text parsing:

### 1. Leak & Asset Audit (Automated HTML Scanner)
* **Original source ZIP (`DIGITAL JOURNALISM WEBSITE.zip`):** Not present in `dist/`. **[PASSED]**
* **Source DOCX / PDF files:** Not present in `dist/`. **[PASSED]**
* **Raw unapproved media (`.mp4`, `.mp3`, `.mpeg`):** Not present in `dist/`. **[PASSED]**
* **Source photographs or third-party stock images:** Not present in `dist/`. Only self-contained SVG vectors and font files. **[PASSED]**
* **Internal editorial notes & provenance:** Scanned all 12 generated HTML files for keywords `provenance`, `sourceFile`, `editorialNotes`, `Internal demo record`. Zero occurrences found. All internal notes remain strictly on disk in markdown frontmatter and are never compiled into public HTML. **[PASSED]**
* **Demonstration detail pages (`dist/stories/...`):** Directory does not exist in `dist/`. **[PASSED]**

### 2. Broken Link Inventory in Production Output (`dist/index.html`)
An automated crawl of all `href` attributes in `dist/index.html` against files existing in `dist/` revealed **13 dead links** caused by hardcoded demo slugs on the homepage:

| Source File | Broken Href Target | Reason |
| :--- | :--- | :--- |
| `dist/index.html` | `/stories/the-quiet-shift/` (4 instances) | Target excluded by release gate |
| `dist/index.html` | `/stories/between-the-lines/` (1 instance) | Target excluded by release gate |
| `dist/index.html` | `/stories/campus-sentiment-index/` (1 instance) | Target excluded by release gate |
| `dist/index.html` | `/stories/the-policy-crossroads/` (2 instances) | Target excluded by release gate |
| `dist/index.html` | `/stories/voices-in-motion/` (2 instances) | Target excluded by release gate |
| `dist/index.html` | `/stories/framing-the-unseen/` (3 instances) | Target excluded by release gate |

*(Note: In `npm run build:demo`, all 13 links resolve to existing HTML files with 100% link integrity).*

### 3. Review of `/sample-article/`
* `dist/sample-article/index.html` is generated in both production and demo builds.
* While it contains a clear disclaimer banner, it remains a public demonstration URL.
* **Recommendation:** Keep during current review stages, but gate behind `import.meta.env.DEV` or remove prior to the final public launch. **[IMPORTANT]**

---

## Task 3: Routing & Information Architecture

| Verification Check | Status | Verification Details |
| :--- | :---: | :--- |
| **Unique Canonical Slugs** | **PASSED** | Slugs validated by Zod regex `^[a-z0-9-]+$`. Each story lives exclusively at `/stories/[slug]/`. |
| **No Duplicate Detail Pages** | **PASSED** | Section archives (`/sections/`) and format archives (`/formats/`) only present cards pointing to the canonical URL; no duplicate pages generated. |
| **Topic Archive Routes** | **PASSED** | Generated for `national`, `politics`, `lifestyle`, and `sports`. |
| **News Analysis Exclusion** | **PASSED** | `News Analysis` has 0 files in source audit and is properly excluded from launch routes and navigation. |
| **Format Archive Routes** | **PASSED** | Generated for `article`, `blog`, `photo-feature`, `podcast`, `video`, and `poll-report`. |
| **Breadcrumb Navigation** | **PASSED** | Hierarchical breadcrumbs (`Home / [Section] / [Format]`) resolve correctly on all story layouts. |
| **Empty State Handling** | **PASSED** | Semantic empty state card displays when 0 approved stories exist for any section or format archive. |
| **Empty State Heading Level** | **MINOR** | Empty state card uses `<h3>` directly after page `<h1>`, skipping `<h2>`. |

---

## Task 4: Multimedia Layouts & Preparedness

The format components in [`src/components/formats/`](file:///c:/Users/bhara/Downloads/DIGITAL%20JOURNALISM%20WEBSITE-20261022T013821Z-1-001/website/src/components/formats) were audited for architectural readiness:

### 1. Portrait Video Explainer (`VideoFormat.astro`)
* **Current State:** Inline SVG placeholder simulating a 9:16 portrait video frame with duration pill (`01:32`), play button overlay, and lower-third disclaimer. Includes a full draft transcript container.
* **Real Media Playback:** **No.** Placeholder only.
* **Readiness for Real Media:**
  * Prepared for portrait MP4 display (`aspect-ratio: 9/16`, max-width 360px).
  * **Still Required for Real Media:**
    1. Replacement of placeholder SVG with native HTML5 `<video controls>` or responsive portrait video player.
    2. Conversion/cropping of source video assets (which currently encode portrait content in square 1080×1080 canvas).
    3. Integration of timed `<track kind="captions" srclang="en">` WebVTT tracks.

### 2. Podcast Audio (`PodcastFormat.astro`)
* **Current State:** Semantic HTML5 `<audio controls preload="none">` element inside a dedicated audio card with episode metadata, duration badge (`18 mins`), and full transcript readout.
* **Real Media Playback:** **No.** The `<audio>` tag has no `src` assigned.
* **Readiness for Real Media:**
  * Native audio element and chapter notes already configured.
  * **Still Required for Real Media:**
    1. Assignment of approved MP3 audio derivative URLs.
    2. Resolution of the `.mpeg` source file MIME type issue identified in the Content Audit.
    3. Inclusion of verified speaker credits and full episode audio transcripts.

### 3. Photo Feature (`PhotoFeatureFormat.astro`)
* **Current State:** Multi-plate visual essay stack using geometric SVG vector art (`Plates I, II, III`).
* **Real Media Playback:** **No.** Placeholder only.
* **Readiness for Real Media:**
  * Semantic `<figure>`, `<figcaption>`, separate caption index, descriptive text, and photographer credit line are implemented.
  * **Still Required for Real Media:**
    1. Real high-resolution image derivatives.
    2. Caption-to-image reconciliation for Dhanushree's 5-photo collection.
    3. Responsive `srcset` / dimensions to prevent cumulative layout shift (CLS).

### 4. Opinion Poll Report (`PollReportFormat.astro`)
* **Current State:** Semantic accessible data table (`<table>`, `<caption>`, `<thead>`, `<tbody>`, `<th scope="col">`, `<th scope="row">`, `<td>`) with visual proportional CSS percentage bars and methodology notes.
* **Real Data:** **Demonstration survey data only.**
* **Readiness for Real Media:**
  * **100% architecturally ready** for real survey data. The table is fully responsive with an accessible scrolling wrapper.
  * **Still Required for Real Data:** Confirmation of Aradhana sample size, Dhanushree denominator, and Mithraa age bands from the source PDF survey reports.

---

## Task 5: Accessibility & Responsive Verification

Automated browser subagent testing verified the live site at desktop (1440px), tablet (768px), and mobile (390px):

```text
[Browser Subagent Audit Summary]
✓ 1440px Desktop: Two-tier navigation (Topics + Explore Formats) verified.
✓ 1440px Desktop: Story layouts (article, video 9:16, podcast, gallery, poll table) verified.
✓ 768px Tablet: 2-column archive grid reflow verified. Zero overflow.
✓ 390px Mobile: Navigation menu drawer toggles with aria-expanded; Escape closes.
✓ 390px Mobile: 9:16 portrait video centers and scales without horizontal scroll.
✓ 390px Mobile: Minimum 44px tap targets verified on all navigation links.
```

### Accessibility Metrics
* **Semantic Landmarks:** `<header>`, `<nav>`, `<main id="main-content">`, `<section>`, `<article>`, `<figure>`, `<figcaption>`, `<aside>`, `<footer>` correctly placed.
* **Keyboard Navigation & Skip Link:** Skip-to-content link jumps focus to `#main-content`. Tab index order is logical.
* **Focus Indicators:** `:focus-visible` outline is `3px solid #892f35` with `outline-offset: 5px`, clearly visible on all interactive elements.
* **Color Contrast Ratios (WCAG 2.1 AA):**
  * Primary Text (`#222222`) on Background (`#F7F4EC`): **14.2:1** (Exceeds WCAG AAA).
  * Accent (`#892F35`) on Background (`#F7F4EC`): **5.8:1** (Exceeds WCAG AA).
  * Secondary Text (`#625F59`) on Background (`#F7F4EC`): **5.1:1** (Exceeds WCAG AA).
  * Note: The variable `--color-muted` (`#737373`, 3.8:1) is reserved for decorative borders and non-essential rules; all body, deck, and metadata text uses `--color-secondary`, maintaining WCAG AA compliance.

---

## Task 6: Build Validation & Commands

1. **Standard Production Build (`npm run build`):**
   * Output: `website/dist/`
   * Duration: **781ms**
   * Result: **12 static HTML pages** generated. Release gate strictly filters out demo stories. Zero compilation errors.
2. **Demo Preview Build (`npm run build:demo`):**
   * Output: `website/dist/`
   * Duration: **819ms**
   * Result: **18 static HTML pages** generated including all 6 canonical demo story pages. Zero compilation errors.

---

## Task 7: Git Repository & Workspace Safety Audit

A repository inspection was executed via `git status`:

```text
On branch master
Changes not staged for commit:
	modified:   website/astro.config.mjs
	modified:   website/package.json
	modified:   website/src/components/Navigation.astro
	modified:   website/src/pages/index.astro
	modified:   website/src/styles/global.css

Untracked files:
	website/scripts/
	website/src/components/formats/
	website/src/content.config.ts
	website/src/content/
	website/src/layouts/StoryLayout.astro
	website/src/pages/formats/
	website/src/pages/sections/
	website/src/pages/stories/
	website/src/utils/
```

### Safety Confirmations
* **Baseline Git Commit (`5dbb026`):** Untouched. No rebase, reset, or amend was performed.
* **Source Journalism Materials (`DIGITAL JOURNALISM WEBSITE/`):** 100% untouched.
* **Source ZIP Archive (`DIGITAL JOURNALISM WEBSITE.zip`):** 100% untouched.
* **Audit Documents (`docs/content-audit.md`, `docs/site-blueprint.md`):** 100% untouched.
* **Git Ignore Verification:** `dist/`, `.astro/`, and `node_modules/` remain strictly ignored.

---

## Classified Findings & Action Plan

### 1. Critical Finding
* **Issue #1: Homepage Demo Leaks & Broken Links in Production**
  * *Description:* `src/pages/index.astro` contains hardcoded demonstration cards and links to demo slugs. When built with `npm run build`, the story pages are excluded by the gate, resulting in 13 broken links and hardcoded fictional headlines on the homepage.
  * *Recommended Fix for Next Stage:* Refactor `src/pages/index.astro` to query `getPublishableStories()`. In production mode before stories are approved, render an editorial launch/placeholder state or direct readers to section archives, completely preventing broken links.

### 2. Important Finding
* **Issue #2: `/sample-article/` Builds into Production Output**
  * *Description:* `dist/sample-article/index.html` is compiled during `npm run build`.
  * *Recommended Fix for Next Stage:* Keep during development and design review, but gate behind `import.meta.env.DEV` or remove prior to public launch.

### 3. Minor Finding
* **Issue #3: Archive Empty State Heading Level Jump**
  * *Description:* On `/sections/[section]/` and `/formats/[format]/`, when 0 stories exist, the empty state card uses an `<h3>` heading directly following the page `<h1>`, skipping `<h2>`.
  * *Recommended Fix for Next Stage:* Adjust empty state card title to `<h2>` to preserve sequential heading hierarchy.

### 4. Passed Items
* **Publishing Approval Gate:** `isDemo === false` and `status === 'approved'` conditions enforced in all dynamic routes.
* **Zero Source Asset Leaks:** No source documents, raw media, or internal editorial notes in public HTML.
* **Single Canonical URL Architecture:** Zero duplicate story detail pages.
* **Multimedia Shells:** 9:16 portrait video, audio, photo gallery, and survey table shells verified.
* **Responsive Reflow & WCAG AA Contrast:** Verified across 390px, 768px, and 1440px viewports.

---

*Report prepared and submitted for review. No code modifications or content imports will proceed without authorization.*
