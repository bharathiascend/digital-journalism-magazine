/**
 * Content Validation Script
 * Validates markdown frontmatter & content in website/src/content/stories
 * Ensures Pages CMS saves and automated extractions adhere to schema and quality requirements.
 */
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const storiesDir = path.resolve(__dirname, '../src/content/stories');
const publicDir = path.resolve(__dirname, '../public');

console.log('\n======================================================');
console.log('   GLASNOST — Editorial Content Pre-Build Validation  ');
console.log('======================================================\n');

const files = fs.readdirSync(storiesDir).filter((f) => f.endsWith('.md'));
let errors = 0;
let warnings = 0;

const validSections = ['national', 'politics', 'lifestyle', 'sports', 'analysis'];
const validFormats = ['article', 'blog', 'video', 'podcast', 'photo-feature', 'poll-report'];
const validStatuses = ['draft', 'needs-review', 'approved'];

files.forEach((file) => {
  const filePath = path.join(storiesDir, file);
  const content = fs.readFileSync(filePath, 'utf8');

  // Check YAML frontmatter presence
  if (!content.startsWith('---')) {
    console.error(`  ✗ [FAIL] ${file}: Missing frontmatter opening delimiter '---'`);
    errors++;
    return;
  }

  const endIdx = content.indexOf('\n---', 3);
  if (endIdx === -1) {
    console.error(`  ✗ [FAIL] ${file}: Missing frontmatter closing delimiter '---'`);
    errors++;
    return;
  }

  const frontmatter = content.slice(3, endIdx);
  const body = content.slice(endIdx + 4);

  // Check slug matches filename
  const slugMatch = frontmatter.match(/^slug:\s*["']?([a-z0-9-]+)["']?/m);
  const expectedSlug = path.basename(file, '.md');
  if (!slugMatch) {
    console.error(`  ✗ [FAIL] ${file}: Missing 'slug' field in frontmatter`);
    errors++;
  } else if (slugMatch[1] !== expectedSlug) {
    console.warn(`  ! [WARN] ${file}: Slug '${slugMatch[1]}' does not match filename '${expectedSlug}'`);
    warnings++;
  }

  // Check section
  const sectionMatch = frontmatter.match(/^section:\s*["']?([a-z0-9-]+)["']?/m);
  if (!sectionMatch || !validSections.includes(sectionMatch[1])) {
    console.error(`  ✗ [FAIL] ${file}: Invalid or missing section '${sectionMatch ? sectionMatch[1] : 'undefined'}'`);
    errors++;
  }

  // Check format
  const formatMatch = frontmatter.match(/^format:\s*["']?([a-z0-9-]+)["']?/m);
  const format = formatMatch ? formatMatch[1] : null;
  if (!format || !validFormats.includes(format)) {
    console.error(`  ✗ [FAIL] ${file}: Invalid or missing format '${format}'`);
    errors++;
  }

  // Check status
  const statusMatch = frontmatter.match(/^status:\s*["']?([a-z0-9-]+)["']?/m);
  const status = statusMatch ? statusMatch[1] : null;
  if (!status || !validStatuses.includes(status)) {
    console.error(`  ✗ [FAIL] ${file}: Invalid or missing status '${status}'`);
    errors++;
  }

  // Check isDemo
  const isDemoMatch = frontmatter.match(/^isDemo:\s*(true|false)/m);
  const isDemo = isDemoMatch ? isDemoMatch[1] === 'true' : false;

  // Check publication date metadata
  const publishedAtMatch = frontmatter.match(/^publishedAt:\s*["']?([^"'\r\n]+)["']?/m);
  if (!publishedAtMatch) {
    console.error(`  ✗ [FAIL] ${file}: Missing 'publishedAt' date in frontmatter`);
    errors++;
  } else {
    const dateVal = publishedAtMatch[1].trim();
    if (!/^\d{4}-\d{2}-\d{2}$/.test(dateVal)) {
      console.error(`  ✗ [FAIL] ${file}: Invalid date format for publishedAt ('${dateVal}'). Expected YYYY-MM-DD.`);
      errors++;
    }
  }

  // Check author metadata
  if (!isDemo && !/["']?authors["']?:\s*(\[|[\r\n]+\s*-)/m.test(frontmatter)) {
    console.warn(`  ! [WARN] ${file}: Frontmatter should specify structured 'authors' metadata.`);
    warnings++;
  }

  // Check empty published article bodies
  const trimmedBody = body.trim();
  if (!isDemo && ['article', 'blog'].includes(format)) {
    if (trimmedBody.length === 0) {
      console.error(`  ✗ [FAIL] ${file}: Approved ${format} has an empty body! Authentic journalism content must not be blank.`);
      errors++;
    } else if (trimmedBody.length < 200) {
      console.warn(`  ! [WARN] ${file}: Suspiciously short article body (${trimmedBody.length} chars). Requires editorial review.`);
      warnings++;
    }
  }

  // Check for squashed / single dense paragraphs in long articles
  if (!isDemo && ['article', 'blog'].includes(format) && trimmedBody.length > 1500) {
    const paras = trimmedBody.split(/\n\s*\n/).filter((p) => p.trim().length > 0);
    if (paras.length === 1) {
      console.warn(`  ! [WARN] ${file}: Long article (${trimmedBody.length} chars) contains only 1 paragraph. Verify paragraph breaks.`);
      warnings++;
    }
  }

  // Check for merged unicode bullet points on a single line
  const lines = body.split(/\r?\n/);
  lines.forEach((line, lineNum) => {
    const bulletCount = (line.match(/[●•]/g) || []).length;
    if (bulletCount > 1) {
      console.error(`  ✗ [FAIL] ${file}:${lineNum + 1}: Multiple merged bullets detected on single line ('${line.slice(0, 60)}...'). Format as Markdown list items.`);
      errors++;
    }
  });

  // Check referenced media paths on disk
  const mediaRegex = /["'\(](\/media\/[^"'#?\)\s]+)["'\)]/g;
  let mediaMatch;
  while ((mediaMatch = mediaRegex.exec(content)) !== null) {
    const relMediaPath = mediaMatch[1];
    // Remove leading slash
    const diskPath = path.join(publicDir, relMediaPath.replace(/^\//, ''));
    if (!fs.existsSync(diskPath)) {
      console.error(`  ✗ [FAIL] ${file}: Referenced media file does not exist on disk: '${relMediaPath}'`);
      errors++;
    }
  }

  // Format-specific metadata validation
  if (format === 'podcast') {
    const durationMatch = frontmatter.match(/["']?duration["']?\s*:\s*["']?([^"',\r\n]+)["']?/);
    if (!durationMatch) {
      console.warn(`  ! [WARN] ${file}: Podcast is missing 'duration' metadata.`);
      warnings++;
    } else {
      const dur = durationMatch[1].trim();
      if (!/^\d{1,2}:\d{2}(:\d{2})?$/.test(dur)) {
        console.warn(`  ! [WARN] ${file}: Podcast duration '${dur}' does not match standard mm:ss format.`);
        warnings++;
      }
    }
  }

  // Check for duplicate h1 in body
  const bodyH1 = body.match(/^#\s+.+$/m);
  if (bodyH1) {
    console.error(`  ✗ [FAIL] ${file}: Markdown body contains an <h1> tag ('${bodyH1[0]}'). Use 'subtitle' in frontmatter or <h2> in body.`);
    errors++;
  }
});

console.log(`\nValidated ${files.length} stories: ${errors} error(s), ${warnings} warning(s).\n`);

if (errors > 0) {
  process.exit(1);
} else {
  console.log('  ✓ All content files passed pre-build validation.\n');
}
