import { resolve } from "node:path";
import { defineConfig } from "vite";

export default defineConfig({
  root: resolve(__dirname, "apps/web"),
  publicDir: resolve(__dirname, "content"),
  server: {
    host: "127.0.0.1",
    port: 4173,
    strictPort: true
  },
  build: {
    outDir: resolve(__dirname, "dist/web"),
    emptyOutDir: true
  }
});
