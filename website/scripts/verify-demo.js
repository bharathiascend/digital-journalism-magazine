process.env.ASTRO_SHOW_DEMOS = 'true';
process.argv.push('--demo');
await import('./verify-release.js');
