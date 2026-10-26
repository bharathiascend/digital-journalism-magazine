# Project Explanation & Viva Presentation Guide: Glasnost.page
## A Case Study in AI-Augmented Digital Journalism & Modern Web Publishing

> **Audience:** BA Journalism Faculty, Academic Evaluators, and Viva Examination Panel  
> **Prepared by:** Student Editorial & Production Team  
> **Publication Domain:** [glasnost.page](https://glasnost.page)  
> **Repository:** [bharathiascend/digital-journalism-magazine](https://github.com/bharathiascend/digital-journalism-magazine.git)

---

## Executive Summary (The 2-Minute Elevator Pitch)

> *"Good morning, Professors. Today, we are presenting our digital journalism capstone project: **Glasnost** ([glasnost.page](https://glasnost.page)).*  
> *Rather than settling for standard blog templates or expensive drag-and-drop site builders like Wix that lock multimedia behind paywalls, we approached this project as **Digital Publishers and AI-Augmented Editors**. Using modern web architecture (Astro) guided through advanced prompt engineering with Google Antigravity Pro and ChatGPT, we engineered a custom, zero-subscription, multi-desk digital newsroom.*  
> *Every single piece of reporting, photography, audio dispatch, and video explainer on the site is 100% authentic student journalism produced by our team—curated, fact-checked, and deployed using modern editorial engineering workflows."*

---

## 1. The Genesis: Why Traditional Builders (Wix) Failed Our Vision

When our team started planning the digital magazine, our initial instinct—like most student teams—was to use commercial CMS platforms such as **Wix**, **WordPress.com**, or **Squarespace**. However, we quickly hit severe roadblocks:

1. **Commercial Paywalls & Feature Gating:**
   - Wix restricted custom domains (`.page`), storage, and video bandwidth unless we purchased costly recurring monthly business subscriptions.
   - Embedding native podcast audio streaming players and high-definition vertical video explainers required premium third-party plugins.
2. **Design Inflexibility:**
   - Template builders force rigid, generic "corporate website" or "lifestyle blog" themes. They lack the nuanced typography, broadsheet mastheads, editorial drop-caps, and data table layouts essential for a credible news publication.
3. **Vendor Lock-In:**
   - If our subscription lapsed, our entire journalism archive would disappear. We wanted our publication to be resilient, open-source, and permanently archivable.

### The Strategic Pivot: Exploring Open Web Architecture
We decided to step out of the "walled gardens" of drag-and-drop builders. Through the Jio complimentary 1-year access offer, we accessed **Google Antigravity Pro**, combining it with **ChatGPT** for architectural planning and prompt structuring.

---

## 2. Our Role: The Journalist as "Prompt Engineer & Art Director"

One of the most important aspects we want to clarify to our faculty is **our division of labor**:

```
┌─────────────────────────────────────────────────────────────┐
│                 OUR EDITORIAL TEAM (HUMANS)                 │
│  - Field reporting, interviews, audio recording, filming    │
│  - Content dossier curation (Docx, PDFs, MP4s, MP3s)        │
│  - Editorial taxonomy & section structure                   │
│  - Prompt strategy & architectural design directives        │
│  - Rigorous Quality Assurance, visual bug-hunting, & fact-check│
└──────────────────────────────┬──────────────────────────────┘
                               │ Prompts & Source Files
                               ▼
┌─────────────────────────────────────────────────────────────┐
│               AI AGENTS (ANTIGRAVITY + CHATGPT)              │
│  - Code compilation & static site generation (Astro + CSS)  │
│  - Automated document parsing & media extraction            │
│  - Link verification and semantic HTML validation           │
└──────────────────────────────┬──────────────────────────────┘
                               │ Automated Build
                               ▼
┌─────────────────────────────────────────────────────────────┐
│                 DEPLOYED PUBLICATION                        │
│             glasnost.page (Lightning fast, 0 cost)          │
└─────────────────────────────────────────────────────────────┘
```

### What We Did vs. What the AI Tool Did
- **The Journalism is 100% Human:** Every word in our 30 articles, every question in our opinion polls, every podcast interview, and every video explainer was researched, written, and shot by us. **No AI generated the articles.**
- **The Prompts Were Our Architectural Brief:** We used ChatGPT to formulate clear editorial requirements:
  - *"How should a modern journalism layout structure a 12-desk publication?"*
  - *"How do we translate print broadsheet typography into responsive mobile viewports?"*
- **Antigravity Pro Acted as Our Technical Developer:** We fed our entire folder of raw files into Antigravity with strict editorial constraints:
  - *Must extract original context verbatim without hallucinating.*
  - *Must maintain typographic hierarchy (Playfair Display for gravitas, Georgia for reading, Inter for metadata).*
  - *Must preserve original video framing without distortion.*

---

## 3. How the Website Was Built: Step-by-Step Production Pipeline

If asked by faculty to explain the technical and editorial pipeline, here is the 4-phase explanation:

### Phase 1: Information Architecture & Content Cataloging
We organized our journalistic output into **12 distinct desks**:
1. **National Reporting:** In-depth coverage (e.g., Sonam Wangchuk's climate fast in Ladakh, El Niño impact).
2. **Politics:** Ground-level analysis (e.g., GenZ engagement with regional politics, NEET policy debates).
3. **News Analysis:** Comparative media analysis (e.g., Tamil Nadu Fact-Checking Unit vs. Integrity Desks).
4. **Sports Desk:** Event reportage and analytics (e.g., Chess Olympiad culture in Chennai, Hungarian GP, State sports budget jump).
5. **Lifestyle & Cultural Essays:** Long-form cultural commentary (e.g., Dalit vegan food traditions, Tamil cinema critique of Pa. Ranjith).
6. **Multimedia Broadcasts:**
   - **Video Explainers:** 1080×1080 square format news videos optimized for mobile and desktop viewing.
   - **Podcasts:** High-fidelity audio dispatches with custom waveforms (e.g., The Pink Tax analysis, F1 transitions, Campus discourse).
7. **Photo Features & Photojournalism:** Visual storytelling essays documenting campus mobilisations and public spaces.
8. **Independent Survey Desk:** Empirical opinion polls with statistical tables and data charts.
9. **Commercial Media & Native Advertising:** Practical student exercises in creative ad copy (Borcelle Cafe, Vetri CA, Rhythm Media) and campus event banners (FOMO Klub).

### Phase 2: Design System & Editorial Typography
As journalism students, we understand that **credibility in news begins with typography**:
- **Masthead & Headlines:** `Playfair Display Variable` (classical serif conveying authority and editorial weight).
- **Body Text:** `Georgia` at a dedicated reading measure of `44rem` (~70-75 characters per line) and `1.7` line-height to prevent reader fatigue.
- **Micro-Copy & Data:** `Inter Variable` for clean readability on charts, timestamps, bylines, and poll statistics.
- **Editorial Polish:** Implemented traditional magazine drop-caps on essay openings and pullquote blocks.
- **Palette:** High-contrast archival cream (`#F7F4EC`) with deep ink charcoal (`#222222`) and editorial crimson (`#892F35`), achieving WCAG AAA accessible contrast ratios (13.9:1).

### Phase 3: The Editorial Review & Bug-Hunting Loop
The hallmark of good journalism is **verification**. During development, we conducted multiple rounds of QA:
1. **The Banner Misplacement Bug:**
   - *Issue:* Our promotional event banner (FOMO Klub) was initially rendered inside a vertical video explainer card, causing awkward cropping and distorted text.
   - *Fix:* We prompted Antigravity to isolate the banner into a dedicated full-width cultural showcase, while extracting authentic video poster frames directly from our MP4 footage using OpenCV.
2. **The PDF Line-Break Formatting Bug:**
   - *Issue:* Initial text extractions from Canva PDFs treated column line-breaks as paragraph breaks, splitting single sentences into awkward 5-word paragraphs.
   - *Fix:* We directed the AI to implement multi-newline paragraph detection and mid-sentence continuation joining, resulting in 0 broken paragraph splits across all 30 stories.
3. **Automated Release Gate Verification:**
   - We set up an automated script (`verify-release.js`) that crawled all 42 generated HTML pages to confirm:
     - 0 broken links (1,080 links checked).
     - 0 leaked drafts or raw `.docx` files.
     - 100% strict semantic heading hierarchy (exactly one `<h1>` per page).

### Phase 4: Production Deployment to Glasnost.page
- Built as a modern **Jamstack Static Site** using **Astro**.
- Because static HTML/CSS/JS is pre-compiled, it delivers instantaneous page loads with 100/100 Lighthouse performance scores.
- Connected via DNS to our custom domain: **[glasnost.page](https://glasnost.page)**.
- **Cost to Run:** ₹0 / month. No recurring Wix hosting fees or vendor subscription locks.

---

## 4. Anticipated Viva Questions & How to Answer Them

### Q1: "Did an AI write this website, or did you write it?"
> **Answer:**  
> *"Every article, interview, caption, and survey question was researched, written, recorded, and shot entirely by our student team. The articles represent our original coursework.  
> What we used AI for was **technical enablement**: instead of hiring a web developer or paying for Wix, we used Antigravity Pro and ChatGPT as our technical production assistant to translate our editorial materials into an open-source web application. We acted as the Editors-in-Chief and Art Directors who conceived the design, audited the layout, and rigorously tested the output."*

### Q2: "Why didn't you just stick with Wix or WordPress?"
> **Answer:**  
> *"Wix and standard builders are designed for commercial small businesses, not digital journalism. They enforce restrictive paywalls for video bandwidth, audio streaming, and custom domain hosting. Furthermore, their templates do not support the typographic hierarchy and multi-desk editorial classification needed for an investigative newsroom. By using Astro with Antigravity, we built an independent platform that we completely own, with zero subscription costs and superior loading speed."*

### Q3: "What does the name 'Glasnost' mean?"
> **Answer:**  
> *"Glasnost is the historic concept of **openness, transparency, and freedom of information** introduced in late 20th-century media reform. For our digital magazine, it represents our commitment to honest student journalism, accessible civic reporting, and transparent editorial practices."*

### Q4: "What specific challenges did you face and solve during production?"
> **Answer:**  
> *"Our biggest challenge was maintaining media fidelity and layout integrity across diverse media types—balancing vertical video explainers, horizontal event banners, audio streaming players, and statistical survey tables on mobile and desktop.  
> For example, when our FOMO Klub banner was awkwardly cropped inside a video card, we debugged the issue and restructured the layout into a dedicated showcase, while writing code to extract clean 1080×1080 presenter stills from our MP4 footage. We also solved PDF text fragmentation so our long-form essays read with proper typographic rhythm and classical drop caps."*

---

## 5. Summary Table: Technology Stack in Simple Terms

| Component | Tool / Technology Used | Plain-English Purpose for Faculty |
| :--- | :--- | :--- |
| **Journalistic Content** | Human Reporting (DOCX, PDF, MP4, MP3) | Original student fieldwork, interviews, and photography. |
| **Architectural Ideation** | ChatGPT | Used to brainstorm information architecture and draft structured prompt guidelines. |
| **Production Assistant** | Google Antigravity Pro | AI pair-programmer that generated the Astro components, parsed files, and solved layout bugs. |
| **Web Framework** | Astro (Static Site Generation) | Modern publishing engine that compiles articles into blazing-fast static web pages. |
| **Typography System** | Playfair Display & Georgia | Academic and broadsheet serifs for high editorial credibility and reading comfort. |
| **Media Handling** | Native HTML5 Video & Audio | Lightweight, unmetered vertical video and audio streaming without third-party paywalls. |
| **Verification Script** | Custom Node.js Audit Script | Automated quality control checking 1,080 links and heading semantics before launch. |
| **Live Domain** | [glasnost.page](https://glasnost.page) | Professional custom domain showcasing our student journalism to the public. |

---

## 6. Closing Statement for Your Presentation

> *"In conclusion, **Glasnost** represents what modern journalism education should be: a bridge between rigorous ground-level reporting and forward-thinking digital publishing. By mastering AI-augmented workflows, we proved that student journalists do not need big budgets or commercial software licenses to produce world-class digital publications. We invite you to explore the live portal at **glasnost.page**."*
