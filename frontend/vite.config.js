import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";
import path from "path";

export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
    },
  },
  build: {
    outDir: "../forms/public/forms",
    emptyOutDir: true,
    manifest: true,
    rollupOptions: {
      input: "./index.html",
      output: {
        entryFileNames: "index.js",
        chunkFileNames: "chunks/[name]-[hash].js",
        assetFileNames: (info) => {
          if (info.name?.endsWith(".css")) return "index.css";
          return "assets/[name]-[hash][extname]";
        },
      },
    },
  },
  server: {
    port: 8083,
    proxy: {
      "^/(api|assets|files|private)": {
        target: "http://mysite.local:8000",
        changeOrigin: true,
        cookieDomainRewrite: "localhost",
        secure: false,
      },
    },
  },
  optimizeDeps: {
    include: ["frappe-ui", "vue", "vue-router", "pinia"],
  },
});
