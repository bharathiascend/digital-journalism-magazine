import { defineConfig } from 'astro/config';
import { fileURLToPath } from 'node:url';

export default defineConfig({
  output: 'static',
  trailingSlash: 'always',
  vite: {
    define: {
      'import.meta.env.ASTRO_SHOW_DEMOS': JSON.stringify(process.env.ASTRO_SHOW_DEMOS || ''),
    },
    server: {
      fs: { strict: true, allow: [fileURLToPath(new URL('.', import.meta.url))] },
    },
  },
});
