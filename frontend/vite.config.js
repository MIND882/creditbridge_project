import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import tailwindcss from '@tailwindcss/vite';
import { viteSingleFile } from 'vite-plugin-singlefile';

export default defineConfig(({ command }) => ({
  plugins: [
    react(),
    tailwindcss(),
    // यह सिर्फ 'npm run build' करने पर एक्टिव होगा, 'npm run dev' में नहीं
    command === 'build' ? viteSingleFile() : null 
  ].filter(Boolean), // null वैल्यूज को हटाने के लिए
  server: {
    host: '0.0.0.0',
    port: 3000,
    allowedHosts: true,
    strictPort: true,
    cors: true,
    proxy: {
      '/v1': { target: 'http://localhost:8000', changeOrigin: true },
      '/api': { target: 'http://localhost:8000', changeOrigin: true },
      '/health': { target: 'http://localhost:8000', changeOrigin: true }
    }
  },
  preview: {
    host: '0.0.0.0',
    port: 3000,
    allowedHosts: true,
    cors: true
  }
}));
