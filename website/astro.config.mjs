import { defineConfig } from 'astro/config';
import { fileURLToPath } from 'node:url';

export default defineConfig({
  output: 'static',
  trailingSlash: 'always',
  vite: {
    server: {
      fs: { strict: true, allow: [fileURLToPath(new URL('.', import.meta.url))] },
    },
  },
});
