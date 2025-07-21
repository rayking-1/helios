# Helios Adaptive Planner 常见问题排查指南

本文档收集了项目开发过程中可能遇到的常见问题及其解决方案。

## 环境问题

### Python 环境

1. **问题: 缺少模块或库**
   - **解决方案**: 确保已激活虚拟环境，然后运行 `pip install -r requirements.txt`
   - **验证**: 运行 `pip list` 检查已安装的包

2. **问题: PYTHONPATH 配置错误**
   - **解决方案**: 设置正确的 PYTHONPATH 环境变量
     ```powershell
     $env:PYTHONPATH = "C:\path\to\helios_adaptive_planner"
     ```
   - **验证**: 运行 `echo $env:PYTHONPATH` 确认路径正确

### Node.js 环境

1. **问题: 依赖包冲突**
   - **解决方案**: 
     ```bash
     cd helios-frontend
     rm -rf node_modules package-lock.json
     npm install
     ```
   - **验证**: 运行 `npm list` 检查依赖状态

## AI 智能体问题

1. **问题: AI 生成的代码质量不佳或无法运行**
   - **解决方案**:
     - 优化 Prompt: 使指令更清晰、具体，提供足够上下文
     - 使用 `@` 符号引用相关文件或代码片段
     - 对生成代码进行迭代修正
   - **示例**:
     ```
     "请使用 pyautogen 框架实现一个 AnalystAgent 类，它应该能够 @backend/tools/user_interaction_tools.py 中的工具函数，并处理 @backend/models/goal_model.py 中定义的数据结构"
     ```

2. **问题: 智能体执行停滞**
   - **原因**: 可能是 API 密钥无效、调用配额耗尽、网络问题
   - **解决方案**:
     - 检查环境变量中的 API 密钥是否正确设置
     - 查看日志中是否有 API 调用错误
     - 确认网络连接稳定
   - **验证**: 运行 `python backend/utils/validate_api_keys.py` 测试 API 连接

## 前后端集成问题

1. **问题: WebSocket 连接失败**
   - **排查步骤**:
     1. 检查后端服务是否运行正常
     2. 查看浏览器开发者工具的 Network 和 Console 选项卡
     3. 确认 WebSocket URL 和端口是否正确
     4. 检查有无 CORS 跨域错误
   - **解决方案**:
     - 确保后端已正确配置 CORS
     - 检查前端 WebSocket URL 是否与后端匹配
     - 参考 `backend/DEBUGGING_MANUAL.md` 中的 WebSocket 重连策略

2. **问题: 前端状态管理与后端数据不同步**
   - **排查步骤**:
     1. 使用浏览器开发工具的 Network 面板监控 API 请求响应
     2. 检查 Zustand store 是否正确更新
   - **解决方案**:
     - 确保 API 调用成功后正确更新 store
     - 使用 React DevTools 调试组件与状态更新

## 测试问题

1. **问题: 测试失败 - 模块导入错误**
   - **解决方案**:
     - 确保测试文件中正确设置了 `sys.path`
     - 检查导入路径是否正确
     ```python
     import sys, os
     sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
     ```

2. **问题: E2E 测试 - Playwright 无法找到元素**
   - **解决方案**:
     - 使用 Playwright 的调试工具：`npx playwright codegen http://localhost:3000`
     - 增加等待时间：`page.wait_for_selector("your-selector", timeout=10000)`
     - 检查选择器是否正确，尝试使用多种选择器策略（ID、CSS、文本）

## 性能优化问题

1. **问题: LLM 调用延迟高**
   - **解决方案**:
     - 实现 LLM 响应缓存
     - 对相似请求进行批处理
     - 考虑使用更快的模型或本地部署的模型

2. **问题: 前端加载速度慢**
   - **解决方案**:
     - 实现代码分割：`const Component = React.lazy(() => import('./Component'))`
     - 优化图片和静态资源
     - 启用 Gzip/Brotli 压缩

## 工具与资源

- **日志分析**：使用 `backend/utils/log_analyzer.py` 分析结构化日志
  ```bash
  python backend/utils/log_analyzer.py --report
  ```

- **调试手册**：参考 `backend/DEBUGGING_MANUAL.md` 获取详细的问题排查流程

- **项目配置检查**：运行 `python backend/utils/verify_env.py` 验证环境配置 
 

本文档收集了项目开发过程中可能遇到的常见问题及其解决方案。

## 环境问题

### Python 环境

1. **问题: 缺少模块或库**
   - **解决方案**: 确保已激活虚拟环境，然后运行 `pip install -r requirements.txt`
   - **验证**: 运行 `pip list` 检查已安装的包

2. **问题: PYTHONPATH 配置错误**
   - **解决方案**: 设置正确的 PYTHONPATH 环境变量
     ```powershell
     $env:PYTHONPATH = "C:\path\to\helios_adaptive_planner"
     ```
   - **验证**: 运行 `echo $env:PYTHONPATH` 确认路径正确

### Node.js 环境

1. **问题: 依赖包冲突**
   - **解决方案**: 
     ```bash
     cd helios-frontend
     rm -rf node_modules package-lock.json
     npm install
     ```
   - **验证**: 运行 `npm list` 检查依赖状态

## AI 智能体问题

1. **问题: AI 生成的代码质量不佳或无法运行**
   - **解决方案**:
     - 优化 Prompt: 使指令更清晰、具体，提供足够上下文
     - 使用 `@` 符号引用相关文件或代码片段
     - 对生成代码进行迭代修正
   - **示例**:
     ```
     "请使用 pyautogen 框架实现一个 AnalystAgent 类，它应该能够 @backend/tools/user_interaction_tools.py 中的工具函数，并处理 @backend/models/goal_model.py 中定义的数据结构"
     ```

2. **问题: 智能体执行停滞**
   - **原因**: 可能是 API 密钥无效、调用配额耗尽、网络问题
   - **解决方案**:
     - 检查环境变量中的 API 密钥是否正确设置
     - 查看日志中是否有 API 调用错误
     - 确认网络连接稳定
   - **验证**: 运行 `python backend/utils/validate_api_keys.py` 测试 API 连接

## 前后端集成问题

1. **问题: WebSocket 连接失败**
   - **排查步骤**:
     1. 检查后端服务是否运行正常
     2. 查看浏览器开发者工具的 Network 和 Console 选项卡
     3. 确认 WebSocket URL 和端口是否正确
     4. 检查有无 CORS 跨域错误
   - **解决方案**:
     - 确保后端已正确配置 CORS
     - 检查前端 WebSocket URL 是否与后端匹配
     - 参考 `backend/DEBUGGING_MANUAL.md` 中的 WebSocket 重连策略

2. **问题: 前端状态管理与后端数据不同步**
   - **排查步骤**:
     1. 使用浏览器开发工具的 Network 面板监控 API 请求响应
     2. 检查 Zustand store 是否正确更新
   - **解决方案**:
     - 确保 API 调用成功后正确更新 store
     - 使用 React DevTools 调试组件与状态更新

## 测试问题

1. **问题: 测试失败 - 模块导入错误**
   - **解决方案**:
     - 确保测试文件中正确设置了 `sys.path`
     - 检查导入路径是否正确
     ```python
     import sys, os
     sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
     ```

2. **问题: E2E 测试 - Playwright 无法找到元素**
   - **解决方案**:
     - 使用 Playwright 的调试工具：`npx playwright codegen http://localhost:3000`
     - 增加等待时间：`page.wait_for_selector("your-selector", timeout=10000)`
     - 检查选择器是否正确，尝试使用多种选择器策略（ID、CSS、文本）

## 性能优化问题

1. **问题: LLM 调用延迟高**
   - **解决方案**:
     - 实现 LLM 响应缓存
     - 对相似请求进行批处理
     - 考虑使用更快的模型或本地部署的模型

2. **问题: 前端加载速度慢**
   - **解决方案**:
     - 实现代码分割：`const Component = React.lazy(() => import('./Component'))`
     - 优化图片和静态资源
     - 启用 Gzip/Brotli 压缩

## 工具与资源

- **日志分析**：使用 `backend/utils/log_analyzer.py` 分析结构化日志
  ```bash
  python backend/utils/log_analyzer.py --report
  ```

- **调试手册**：参考 `backend/DEBUGGING_MANUAL.md` 获取详细的问题排查流程

- **项目配置检查**：运行 `python backend/utils/verify_env.py` 验证环境配置 
 
 