# Frontend 目录

此目录是前端代码的标准位置。在当前项目结构中，实际前端代码位于 `../helios-frontend` 目录。

## 目录结构说明

根据AG2开发规范，前端应包含以下结构：

```
frontend/
├── src/
│   ├── api/             # GraphQL API 调用
│   ├── components/      # React 组件
│   ├── hooks/           # 自定义 Hooks (例如 useWebSocket)
│   ├── store/           # Zustand 状态管理
│   └── pages/           # 页面组件
├── package.json         # Node.js 依赖和脚本
└── tsconfig.json        # TypeScript 配置
```

实际项目中，请使用 `../helios-frontend` 目录进行开发。 