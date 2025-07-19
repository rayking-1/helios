import { defineConfig, loadEnv } from 'vite';
import react from '@vitejs/plugin-react';
import path from 'path';

// https://vitejs.dev/config/
export default defineConfig(({ mode }) => {
  // 加载环境变量
  const env = loadEnv(mode, process.cwd());
  
  // API 目标地址，默认为本地开发地址
  const apiTarget = env.VITE_API_BASE_URL || 'http://localhost:8000';
  
  return {
    plugins: [react()],
    resolve: {
      alias: {
        '@': path.resolve(__dirname, './src'),
      },
    },
    server: {
      port: 3000,
      host: true, // 监听所有地址，包括局域网和公网地址
      // 如果需要代理API请求，可以在这里配置
      proxy: {
        '/api': {
          target: apiTarget,
          changeOrigin: true,
          rewrite: (path) => path.replace(/^\/api/, '')
        }
      }
    }
  };
}); 
export default defineConfig({
  plugins: [react()],
  server: {
    port: 3000,
    // 如果需要代理API请求，可以在这里配置
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, '')
      }
    }
  }
}); 