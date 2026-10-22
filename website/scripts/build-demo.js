process.env.ASTRO_SHOW_DEMOS = 'true';
import { spawnSync } from 'node:child_process';

const result = spawnSync('npx', ['astro', 'build'], {
  stdio: 'inherit',
  shell: true,
  env: process.env,
});

process.exit(result.status ?? 0);
