import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    host: true, // Listen on all addresses (required for Docker)
    port: 5173,
    strictPort: true,
    allowedHosts: [
      '.trycloudflare.com', // Allow all Cloudflare tunnels
    ],
    watch: {
      usePolling: true, // Required for hot reload in Docker on Windows
    },
  },
})
