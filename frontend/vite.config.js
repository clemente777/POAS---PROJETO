
/*
|--------------------------------------------------------------------------
| Arquivo: vite.config.js
| Projeto: Petonline24h
|--------------------------------------------------------------------------
|
| Configura o ambiente de desenvolvimento e a compilação do frontend.
| Integra React e habilita recursos PWA por meio do Service Worker.
|
*/

import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import { VitePWA } from 'vite-plugin-pwa'

export default defineConfig({
  plugins: [
    react(),

    VitePWA({
      // Mantém o manifesto existente em frontend/public.
      manifest: false,

      // Atualiza o Service Worker automaticamente.
      registerType: 'autoUpdate',

      // Arquivos estáticos que poderão funcionar offline.
      workbox: {
        globPatterns: [
          '**/*.{js,css,html,ico,png,svg,webmanifest,woff2}',
        ],

        // Remove caches antigos após atualizações.
        cleanupOutdatedCaches: true,
      },
    }),
  ],

  // Mantém o acesso pela rede local.
  server: {
    host: true,
    port: 5173,
  },
})
