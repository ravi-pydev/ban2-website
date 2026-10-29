import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

// In development (`npm run dev`) the React app runs on port 5173 and forwards
// API and image requests to Django on port 8000 (`make run`).
// `npm run build` writes the production files to dist/, which Django serves.
const DJANGO = 'http://127.0.0.1:8000';

export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    proxy: {
      '/api': DJANGO,
      '/static': DJANGO,
    },
  },
  build: {
    outDir: 'dist',
  },
});
