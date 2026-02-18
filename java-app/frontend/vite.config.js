import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import { VitePWA } from 'vite-plugin-pwa';
export default defineConfig({
    plugins: [
        react(),
        VitePWA({
            registerType: 'autoUpdate',
            manifest: {
                name: 'Hidden Gems',
                short_name: 'Hidden Gems',
                description: 'Discover local businesses in Richmond, VA',
                theme_color: '#0d9488',
                background_color: '#e2e8f0',
                display: 'standalone',
                start_url: '/',
                icons: [],
            },
            workbox: { globPatterns: ['**/*.{js,css,html,ico,png,svg,woff2}'] },
            devOptions: { enabled: true },
        }),
    ],
    server: {
        port: 5173,
        proxy: {
            '/api': {
                target: 'http://localhost:8080',
                changeOrigin: true,
            },
        },
    },
});
