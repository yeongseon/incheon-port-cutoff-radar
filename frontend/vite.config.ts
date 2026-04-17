import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'

export default defineConfig(({ mode }) => ({
  plugins: [react(), tailwindcss()],
  base: mode === 'demo' ? '/incheon-port-cutoff-radar/app/' : '/',
  define: {
    'import.meta.env.VITE_DEMO_MODE': JSON.stringify(mode === 'demo' ? 'true' : 'false'),
  },
  server: {
    proxy: mode !== 'demo' ? {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      },
    } : undefined,
  },
}))
