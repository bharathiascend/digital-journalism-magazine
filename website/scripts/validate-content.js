/**
 * Content Validation Script
 * Validates markdown frontmatter in website/src/content/stories
 * Ensures Pages CMS saves adhere to schema requirements before Vercel build.
 */
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const storiesDir = path.resolve(__dirname, '../src/content/stories');

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
  if (!formatMatch || !validFormats.includes(formatMatch[1])) {
    console.error(`  ✗ [FAIL] ${file}: Invalid or missing format '${formatMatch ? formatMatch[1] : 'undefined'}'`);
    errors++;
  }

  // Check status
  const statusMatch = frontmatter.match(/^status:\s*["']?([a-z0-9-]+)["']?/m);
  if (!statusMatch || !validStatuses.includes(statusMatch[1])) {
    console.error(`  ✗ [FAIL] ${file}: Invalid or missing status '${statusMatch ? statusMatch[1] : 'undefined'}'`);
    errors++;
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
