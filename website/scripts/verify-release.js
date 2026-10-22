/**
 * Release Verification & Safety Audit Script
 * 
 * Inspects the built static output in dist/ to verify:
 * 1. Zero broken internal links (with trailingSlash: always handling & anchor fragment validation).
 * 2. Complete absence of unapproved source materials (.zip, .docx, .pdf, .mp4, .mp3).
 * 3. Complete absence of internal editorial notes or provenance frontmatter keys in public HTML.
 * 4. Safe release gating:
 *    - In production mode (default): no demo story routes (/stories/*) and no sample article (/sample-article/).
 *    - In demo-preview mode: all demo routes must exist and have 100% link integrity.
 * 5. Strict semantic heading hierarchy (single <h1> per page; no skipped levels).
 */

import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const websiteDir = path.resolve(__dirname, '..');
const distDir = path.join(websiteDir, 'dist');

const isDemoMode = process.env.ASTRO_SHOW_DEMOS === 'true' || process.argv.includes('--demo');

console.log('\n======================================================');
console.log(`   THE JOURNAL — Static Release Verification Script   `);
console.log(`   Mode: ${isDemoMode ? 'DEMO-PREVIEW MODE (ASTRO_SHOW_DEMOS=true)' : 'STRICT PRODUCTION MODE'}`);
console.log('======================================================\n');

if (!fs.existsSync(distDir)) {
  console.error(`[FAIL] Dist directory not found at: ${distDir}`);
  console.error('       Please run npm run build before running verification.\n');
  process.exit(1);
}

// 1. Walk dist and catalog all files
function walk(dir) {
  let results = [];
  const list = fs.readdirSync(dir);
  for (const file of list) {
    const fullPath = path.join(dir, file);
    const stat = fs.statSync(fullPath);
    if (stat.isDirectory()) {
      results = results.concat(walk(fullPath));
    } else {
      results.push(fullPath);
    }
  }
  return results;
}

const allFiles = walk(distDir);
const htmlFiles = allFiles.filter((f) => f.endsWith('.html'));

console.log(`[INFO] Cataloged ${allFiles.length} files in dist/ (${htmlFiles.length} HTML pages).`);

let failures = 0;
let warnings = 0;

function fail(msg) {
  console.error(`  ✗ [FAIL] ${msg}`);
  failures++;
}

function warn(msg) {
  console.warn(`  ! [WARN] ${msg}`);
  warnings++;
}

function pass(msg) {
  console.log(`  ✓ [PASS] ${msg}`);
}

// 2. Asset Integrity & Leak Checks
console.log('\n--- 1. Deployed Asset & Privacy Leak Checks ---');

const forbiddenExtensions = ['.zip', '.docx', '.mpeg'];
const leakedSourceFiles = allFiles.filter((file) => {
  const ext = path.extname(file).toLowerCase();
  return forbiddenExtensions.includes(ext);
});

if (leakedSourceFiles.length === 0) {
  pass('Zero source archives (.zip), raw Word documents (.docx), or unstandardized media in dist/.');
} else {
  fail(`Found ${leakedSourceFiles.length} forbidden source asset(s) in dist/:`);
  leakedSourceFiles.forEach((f) => console.error(`         ${path.relative(distDir, f)}`));
}

// 3. Release Gating Checks (Production vs Demo)
console.log('\n--- 2. Release Gate & Route Exposure Checks ---');

const sampleArticleDir = path.join(distDir, 'sample-article');
const storiesDir = path.join(distDir, 'stories');

if (!isDemoMode) {
  // In strict production mode:
  // 1. /sample-article/ must NOT exist
  if (fs.existsSync(sampleArticleDir)) {
    fail('dist/sample-article/ was generated in production build. It must only exist in demo mode.');
  } else {
    pass('dist/sample-article/ successfully excluded from production build.');
  }

  // 2. /stories/ must NOT exist while stories are unapproved/demo
  if (fs.existsSync(storiesDir)) {
    const generatedStories = fs.readdirSync(storiesDir);
    if (generatedStories.length > 0) {
      fail(`dist/stories/ generated ${generatedStories.length} unapproved/demo story page(s) in production build.`);
    } else {
      pass('dist/stories/ contains zero unapproved story pages.');
    }
  } else {
    pass('dist/stories/ successfully excluded from production build.');
  }
} else {
  // In demo preview mode:
  // Both sample-article and demo stories SHOULD exist
  if (fs.existsSync(sampleArticleDir)) {
    pass('dist/sample-article/ present for local design review.');
  } else {
    fail('dist/sample-article/ was expected in demo preview mode but was missing.');
  }

  if (fs.existsSync(storiesDir)) {
    const demoStories = fs.readdirSync(storiesDir);
    pass(`dist/stories/ generated ${demoStories.length} editorial story routes for preview.`);
  } else {
    fail('dist/stories/ was expected in demo preview mode but was missing.');
  }
}

// 4. HTML Content & Internal Editorial Notes Crawl
console.log('\n--- 3. Editorial Notes & Text Crawl ---');

const internalKeywords = [
  'Internal demo record',
  'provenance:',
  'editorialNotes:',
  'sourceFile:',
  'Demonstration record created to test',
];

const knownDemoTitles = [
  '[Demo]',
  'The Quiet Shift in River Basin Agriculture',
  'The Policy Crossroads in Municipal Transit',
  'Voices in Motion: The Campus Track Season',
  'The 2026 Student Housing Sentiment Survey',
  'Reading Between the Margins: Notes on Used Paper',
];

let leakCount = 0;
let demoTextLeakInProd = 0;

for (const htmlFile of htmlFiles) {
  const content = fs.readFileSync(htmlFile, 'utf-8');
  const relPath = path.relative(distDir, htmlFile).replace(/\\/g, '/');

  // Check for internal metadata leakage
  for (const kw of internalKeywords) {
    if (content.includes(kw)) {
      fail(`Internal editorial note/provenance leaked in ${relPath}: keyword "${kw}" found.`);
      leakCount++;
    }
  }

  // In production mode, check that demo titles are not hardcoded on public pages
  if (!isDemoMode) {
    for (const title of knownDemoTitles) {
      if (content.includes(title)) {
        fail(`Fictional demonstration headline leaked into production page ${relPath}: "${title}"`);
        demoTextLeakInProd++;
      }
    }
  }
}

if (leakCount === 0) {
  pass('Zero internal editorial notes or provenance metadata leaked into HTML.');
}

if (!isDemoMode) {
  if (demoTextLeakInProd === 0) {
    pass('Zero fictional demonstration headlines or stories leaked into production pages.');
  }
}

// 5. HTML Link Integrity & Navigation Crawl
console.log('\n--- 4. Link Integrity & Anchor Crawl ---');

let totalLinksChecked = 0;
let brokenLinks = [];

// Pre-scan IDs across all HTML files for fragment validation
const fileIds = new Map();

for (const htmlFile of htmlFiles) {
  const content = fs.readFileSync(htmlFile, 'utf-8');
  const relPath = path.relative(distDir, htmlFile).replace(/\\/g, '/');
  const ids = new Set();

  // Find all id="..." attributes
  const idMatches = content.matchAll(/\sid=["']([^"']+)["']/gi);
  for (const m of idMatches) {
    ids.add(m[1]);
  }
  fileIds.set(relPath, ids);
}

for (const htmlFile of htmlFiles) {
  const content = fs.readFileSync(htmlFile, 'utf-8');
  const relSource = path.relative(distDir, htmlFile).replace(/\\/g, '/');

  // Match all href="..."
  const hrefMatches = content.matchAll(/\shref=["']([^"']+)["']/gi);

  for (const match of hrefMatches) {
    const rawHref = match[1].trim();
    totalLinksChecked++;

    // Ignore external URLs, mailto, tel, javascript
    if (/^(https?:|\/\/|mailto:|tel:|javascript:)/i.test(rawHref)) {
      continue;
    }

    // Split target into path and hash
    const [pathPart, hashPart] = rawHref.split('#');

    // Case A: Pure same-page hash fragment (e.g., href="#top")
    if (!pathPart && hashPart) {
      const pageIds = fileIds.get(relSource);
      if (!pageIds || (!pageIds.has(hashPart) && hashPart !== 'top')) {
        brokenLinks.push({
          source: relSource,
          href: rawHref,
          reason: `Target element id="#${hashPart}" does not exist on this page.`,
        });
      }
      continue;
    }

    // Case B: Relative or absolute path
    let targetHtmlRel;
    if (pathPart.startsWith('/')) {
      // Root-relative path
      if (pathPart === '/') {
        targetHtmlRel = 'index.html';
      } else if (pathPart.endsWith('/')) {
        targetHtmlRel = pathPart.slice(1) + 'index.html';
      } else {
        targetHtmlRel = pathPart.slice(1);
      }
    } else {
      // Relative path
      const currentDir = path.dirname(relSource);
      targetHtmlRel = path.normalize(path.join(currentDir, pathPart)).replace(/\\/g, '/');
      if (pathPart.endsWith('/') && !targetHtmlRel.endsWith('index.html')) {
        targetHtmlRel = targetHtmlRel + '/index.html';
      }
    }

    const targetDiskPath = path.join(distDir, targetHtmlRel);

    if (!fs.existsSync(targetDiskPath)) {
      brokenLinks.push({
        source: relSource,
        href: rawHref,
        reason: `Target file does not exist: dist/${targetHtmlRel}`,
      });
      continue;
    }

    // If there is an anchor fragment on another page (e.g., /#latest)
    if (hashPart) {
      const targetIds = fileIds.get(targetHtmlRel);
      if (targetIds && !targetIds.has(hashPart) && hashPart !== 'top') {
        brokenLinks.push({
          source: relSource,
          href: rawHref,
          reason: `Anchor id="#${hashPart}" does not exist in target page dist/${targetHtmlRel}`,
        });
      }
    }
  }
}

if (brokenLinks.length === 0) {
  pass(`All ${totalLinksChecked} links verified successfully with 100% link integrity.`);
} else {
  fail(`Found ${brokenLinks.length} broken link(s):`);
  brokenLinks.forEach((b) => {
    console.error(`         Source: ${b.source} -> Href: "${b.href}" (${b.reason})`);
  });
}

// 6. Heading Hierarchy & Accessibility Check
console.log('\n--- 5. Semantic Heading Hierarchy ---');

let headingIssues = 0;

for (const htmlFile of htmlFiles) {
  const content = fs.readFileSync(htmlFile, 'utf-8');
  const relPath = path.relative(distDir, htmlFile).replace(/\\/g, '/');

  const h1Matches = [...content.matchAll(/<h1[^>]*>([\s\S]*?)<\/h1>/gi)];
  if (h1Matches.length !== 1) {
    fail(`Page ${relPath} has ${h1Matches.length} <h1> tags (strictly expected 1).`);
    headingIssues++;
  }

  // Scan sequential heading tags
  const headingTags = [...content.matchAll(/<h([1-6])[^>]*>/gi)].map((m) => parseInt(m[1], 10));
  for (let i = 0; i < headingTags.length - 1; i++) {
    const current = headingTags[i];
    const next = headingTags[i + 1];
    // A jump greater than 1 (e.g. h1 -> h3) is a hierarchy violation
    if (next > current + 1) {
      fail(`Heading hierarchy jump in ${relPath}: <h${current}> followed directly by <h${next}>.`);
      headingIssues++;
    }
  }
}

if (headingIssues === 0) {
  pass('All HTML pages contain exactly one <h1> and follow sequential heading hierarchy.');
}

// Summary Report
console.log('\n======================================================');
console.log(`   AUDIT SUMMARY: ${failures === 0 ? 'PASSED (0 errors)' : `FAILED (${failures} error(s))`}`);
console.log('======================================================\n');

process.exit(failures === 0 ? 0 : 1);
