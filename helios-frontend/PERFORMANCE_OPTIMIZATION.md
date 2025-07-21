# Helios Frontend 性能优化指南

本文档提供了针对Helios自适应规划系统前端的性能优化策略和最佳实践。

## 1. 应用加载性能优化

### 1.1 代码分割

使用React的`React.lazy`和`Suspense`实现代码分割，减少初始加载bundle大小：

```jsx
// 优化前
import AIWorkshopPage from './pages/AIWorkshopPage';

// 优化后
const AIWorkshopPage = React.lazy(() => import('./pages/AIWorkshopPage'));

// 在路由中使用
<Route 
  path="/workshop" 
  element={
    <Suspense fallback={<LoadingSpinner />}>
      <AIWorkshopPage />
    </Suspense>
  }
/>
```

### 1.2 静态资源优化

- **图片压缩**: 使用`vite-plugin-imagemin`对所有图片进行自动压缩
  ```bash
  npm install vite-plugin-imagemin --save-dev
  ```
  
  在`vite.config.ts`中配置:
  ```typescript
  import imagemin from 'vite-plugin-imagemin';
  
  export default defineConfig({
    plugins: [
      // 其他插件...
      imagemin({
        gifsicle: { optimizationLevel: 7, interlaced: false },
        optipng: { optimizationLevel: 7 },
        mozjpeg: { quality: 80 },
        pngquant: { quality: [0.8, 0.9], speed: 4 },
        svgo: { plugins: [{ name: 'removeViewBox' }] },
      })
    ]
  });
  ```

- **使用WebP格式**: 将JPG/PNG图片转换为WebP格式以减小文件大小

- **字体优化**: 只加载必要的字重和字符集，使用`font-display: swap`加快字体渲染

### 1.3 预加载与预取

在`index.html`中为关键资源添加预加载标签:

```html
<link rel="preload" href="/fonts/custom-font.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/api/v1/user-config" as="fetch" crossorigin>
```

## 2. 渲染性能优化

### 2.1 React组件优化

- **使用React.memo**防止不必要的重渲染:

  ```jsx
  const TaskItem = React.memo(({ task, onUpdate }) => {
    // 组件内容...
  });
  ```

- **使用useCallback**确保函数引用稳定:

  ```jsx
  const handleTaskUpdate = useCallback((taskId, status) => {
    // 处理任务更新
  }, [/* 依赖项 */]);
  ```

- **使用useMemo**缓存计算结果:

  ```jsx
  const sortedTasks = useMemo(() => {
    return tasks.sort((a, b) => new Date(a.dueDate) - new Date(b.dueDate));
  }, [tasks]);
  ```

### 2.2 虚拟化长列表

对于任务列表等可能包含大量项目的组件，使用`react-window`或`react-virtualized`实现虚拟化:

```jsx
import { FixedSizeList } from 'react-window';

// 在TaskList组件中
return (
  <FixedSizeList
    height={500}
    width="100%"
    itemCount={tasks.length}
    itemSize={60}
  >
    {({ index, style }) => (
      <TaskItem 
        style={style}
        task={tasks[index]}
        onUpdate={handleTaskUpdate} 
      />
    )}
  </FixedSizeList>
);
```

### 2.3 减少重绘和回流

- 使用CSS的`transform`和`opacity`属性来实现动画，而不是改变布局属性
- 批量DOM操作，例如使用DocumentFragment
- 避免在循环中读取布局属性（如offsetHeight）

## 3. 网络请求优化

### 3.1 优化API调用

- **实现请求去重**: 使用库如`react-query`或自定义hooks避免重复请求

  ```jsx
  import { useQuery } from 'react-query';
  
  function useTasks() {
    return useQuery('tasks', fetchTasks, {
      staleTime: 60000, // 1分钟内视为新鲜数据
      cacheTime: 900000, // 15分钟的缓存时间
    });
  }
  ```

- **GraphQL查询优化**: 只请求需要的字段

  ```graphql
  # 优化前
  query {
    plan {
      id
      title
      description
      createdAt
      updatedAt
      tasks {
        id
        title
        description
        status
        dueDate
        priority
        tags
      }
    }
  }
  
  # 优化后
  query {
    plan {
      id
      title
      tasks {
        id
        title
        status
        dueDate
      }
    }
  }
  ```

### 3.2 WebSocket优化

- **消息批处理**: 减少小型独立更新消息
- **添加断线重连机制**:

  ```javascript
  // hooks/useWebSocket.ts
  function useWebSocket(url) {
    // ...现有代码
    
    useEffect(() => {
      function connect() {
        const ws = new WebSocket(url);
        
        ws.onclose = (event) => {
          console.log(`WebSocket连接关闭: ${event.code}`);
          // 指数回退重连
          setTimeout(() => {
            connect();
          }, Math.min(1000 * Math.pow(2, reconnectAttempt), 30000));
          setReconnectAttempt(prev => prev + 1);
        };
        
        // 连接成功后重置重连计数
        ws.onopen = () => {
          setReconnectAttempt(0);
        };
        
        // 其他事件处理...
        
        setSocket(ws);
      }
      
      connect();
      
      return () => {
        socket?.close();
      };
    }, [url]);
    
    // ...剩余代码
  }
  ```

## 4. 状态管理优化

### 4.1 Zustand Store分片

将全局状态分割成独立的小型store，避免整体重新渲染:

```typescript
// store/useTaskStore.ts
import create from 'zustand';

export const useTaskStore = create((set) => ({
  tasks: [],
  isLoading: false,
  fetchTasks: async () => {
    set({ isLoading: true });
    try {
      const tasks = await fetchTasksFromAPI();
      set({ tasks, isLoading: false });
    } catch (error) {
      set({ isLoading: false });
      console.error(error);
    }
  },
}));

// store/usePlanStore.ts - 类似实现
```

### 4.2 选择性订阅

使用选择器函数只订阅组件关心的状态部分:

```jsx
// 优化前 - 订阅整个store
const { tasks, plans, user, settings } = useAppStore();

// 优化后 - 只订阅需要的状态
const tasks = useAppStore(state => state.tasks);
```

## 5. 自动化性能监测

### 5.1 Lighthouse CI集成

将Lighthouse集成到CI/CD流水线:

```yaml
# .github/workflows/lighthouse.yml
name: Lighthouse CI
on: [push]
jobs:
  lighthouse:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Lighthouse
        uses: treosh/lighthouse-ci-action@v9
        with:
          urls: |
            https://staging.helios-planner.com/
            https://staging.helios-planner.com/login
          uploadArtifacts: true
          temporaryPublicStorage: true
```

### 5.2 性能预算

在`lighthouse-ci-config.js`中设置性能预算:

```javascript
module.exports = {
  ci: {
    collect: {
      // ...
    },
    assert: {
      preset: 'lighthouse:recommended',
      assertions: {
        'interactive': ['error', {maxNumericValue: 3000}],
        'first-contentful-paint': ['error', {maxNumericValue: 2000}],
        'largest-contentful-paint': ['error', {maxNumericValue: 2500}],
        'cumulative-layout-shift': ['error', {maxNumericValue: 0.1}],
        'total-blocking-time': ['error', {maxNumericValue: 200}],
        'max-potential-fid': ['error', {maxNumericValue: 100}],
      },
    },
  },
};
```

## 6. 性能检测与调试工具

1. **React DevTools Profiler**: 识别渲染瓶颈的最佳工具
2. **Chrome Performance面板**: 检测JavaScript执行和渲染性能
3. **WebPageTest.org**: 测试各种网络条件下的性能
4. **Vite Bundle Analyzer**: 分析bundle大小
   ```bash
   npm install rollup-plugin-visualizer --save-dev
   ```
   
   配置到`vite.config.ts`:
   ```typescript
   import { visualizer } from 'rollup-plugin-visualizer';
   
   export default defineConfig({
     plugins: [
       // ...其他插件
       visualizer({
         open: true,
         gzipSize: true,
         brotliSize: true,
       }),
     ],
   });
   ``` 
 

本文档提供了针对Helios自适应规划系统前端的性能优化策略和最佳实践。

## 1. 应用加载性能优化

### 1.1 代码分割

使用React的`React.lazy`和`Suspense`实现代码分割，减少初始加载bundle大小：

```jsx
// 优化前
import AIWorkshopPage from './pages/AIWorkshopPage';

// 优化后
const AIWorkshopPage = React.lazy(() => import('./pages/AIWorkshopPage'));

// 在路由中使用
<Route 
  path="/workshop" 
  element={
    <Suspense fallback={<LoadingSpinner />}>
      <AIWorkshopPage />
    </Suspense>
  }
/>
```

### 1.2 静态资源优化

- **图片压缩**: 使用`vite-plugin-imagemin`对所有图片进行自动压缩
  ```bash
  npm install vite-plugin-imagemin --save-dev
  ```
  
  在`vite.config.ts`中配置:
  ```typescript
  import imagemin from 'vite-plugin-imagemin';
  
  export default defineConfig({
    plugins: [
      // 其他插件...
      imagemin({
        gifsicle: { optimizationLevel: 7, interlaced: false },
        optipng: { optimizationLevel: 7 },
        mozjpeg: { quality: 80 },
        pngquant: { quality: [0.8, 0.9], speed: 4 },
        svgo: { plugins: [{ name: 'removeViewBox' }] },
      })
    ]
  });
  ```

- **使用WebP格式**: 将JPG/PNG图片转换为WebP格式以减小文件大小

- **字体优化**: 只加载必要的字重和字符集，使用`font-display: swap`加快字体渲染

### 1.3 预加载与预取

在`index.html`中为关键资源添加预加载标签:

```html
<link rel="preload" href="/fonts/custom-font.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/api/v1/user-config" as="fetch" crossorigin>
```

## 2. 渲染性能优化

### 2.1 React组件优化

- **使用React.memo**防止不必要的重渲染:

  ```jsx
  const TaskItem = React.memo(({ task, onUpdate }) => {
    // 组件内容...
  });
  ```

- **使用useCallback**确保函数引用稳定:

  ```jsx
  const handleTaskUpdate = useCallback((taskId, status) => {
    // 处理任务更新
  }, [/* 依赖项 */]);
  ```

- **使用useMemo**缓存计算结果:

  ```jsx
  const sortedTasks = useMemo(() => {
    return tasks.sort((a, b) => new Date(a.dueDate) - new Date(b.dueDate));
  }, [tasks]);
  ```

### 2.2 虚拟化长列表

对于任务列表等可能包含大量项目的组件，使用`react-window`或`react-virtualized`实现虚拟化:

```jsx
import { FixedSizeList } from 'react-window';

// 在TaskList组件中
return (
  <FixedSizeList
    height={500}
    width="100%"
    itemCount={tasks.length}
    itemSize={60}
  >
    {({ index, style }) => (
      <TaskItem 
        style={style}
        task={tasks[index]}
        onUpdate={handleTaskUpdate} 
      />
    )}
  </FixedSizeList>
);
```

### 2.3 减少重绘和回流

- 使用CSS的`transform`和`opacity`属性来实现动画，而不是改变布局属性
- 批量DOM操作，例如使用DocumentFragment
- 避免在循环中读取布局属性（如offsetHeight）

## 3. 网络请求优化

### 3.1 优化API调用

- **实现请求去重**: 使用库如`react-query`或自定义hooks避免重复请求

  ```jsx
  import { useQuery } from 'react-query';
  
  function useTasks() {
    return useQuery('tasks', fetchTasks, {
      staleTime: 60000, // 1分钟内视为新鲜数据
      cacheTime: 900000, // 15分钟的缓存时间
    });
  }
  ```

- **GraphQL查询优化**: 只请求需要的字段

  ```graphql
  # 优化前
  query {
    plan {
      id
      title
      description
      createdAt
      updatedAt
      tasks {
        id
        title
        description
        status
        dueDate
        priority
        tags
      }
    }
  }
  
  # 优化后
  query {
    plan {
      id
      title
      tasks {
        id
        title
        status
        dueDate
      }
    }
  }
  ```

### 3.2 WebSocket优化

- **消息批处理**: 减少小型独立更新消息
- **添加断线重连机制**:

  ```javascript
  // hooks/useWebSocket.ts
  function useWebSocket(url) {
    // ...现有代码
    
    useEffect(() => {
      function connect() {
        const ws = new WebSocket(url);
        
        ws.onclose = (event) => {
          console.log(`WebSocket连接关闭: ${event.code}`);
          // 指数回退重连
          setTimeout(() => {
            connect();
          }, Math.min(1000 * Math.pow(2, reconnectAttempt), 30000));
          setReconnectAttempt(prev => prev + 1);
        };
        
        // 连接成功后重置重连计数
        ws.onopen = () => {
          setReconnectAttempt(0);
        };
        
        // 其他事件处理...
        
        setSocket(ws);
      }
      
      connect();
      
      return () => {
        socket?.close();
      };
    }, [url]);
    
    // ...剩余代码
  }
  ```

## 4. 状态管理优化

### 4.1 Zustand Store分片

将全局状态分割成独立的小型store，避免整体重新渲染:

```typescript
// store/useTaskStore.ts
import create from 'zustand';

export const useTaskStore = create((set) => ({
  tasks: [],
  isLoading: false,
  fetchTasks: async () => {
    set({ isLoading: true });
    try {
      const tasks = await fetchTasksFromAPI();
      set({ tasks, isLoading: false });
    } catch (error) {
      set({ isLoading: false });
      console.error(error);
    }
  },
}));

// store/usePlanStore.ts - 类似实现
```

### 4.2 选择性订阅

使用选择器函数只订阅组件关心的状态部分:

```jsx
// 优化前 - 订阅整个store
const { tasks, plans, user, settings } = useAppStore();

// 优化后 - 只订阅需要的状态
const tasks = useAppStore(state => state.tasks);
```

## 5. 自动化性能监测

### 5.1 Lighthouse CI集成

将Lighthouse集成到CI/CD流水线:

```yaml
# .github/workflows/lighthouse.yml
name: Lighthouse CI
on: [push]
jobs:
  lighthouse:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Lighthouse
        uses: treosh/lighthouse-ci-action@v9
        with:
          urls: |
            https://staging.helios-planner.com/
            https://staging.helios-planner.com/login
          uploadArtifacts: true
          temporaryPublicStorage: true
```

### 5.2 性能预算

在`lighthouse-ci-config.js`中设置性能预算:

```javascript
module.exports = {
  ci: {
    collect: {
      // ...
    },
    assert: {
      preset: 'lighthouse:recommended',
      assertions: {
        'interactive': ['error', {maxNumericValue: 3000}],
        'first-contentful-paint': ['error', {maxNumericValue: 2000}],
        'largest-contentful-paint': ['error', {maxNumericValue: 2500}],
        'cumulative-layout-shift': ['error', {maxNumericValue: 0.1}],
        'total-blocking-time': ['error', {maxNumericValue: 200}],
        'max-potential-fid': ['error', {maxNumericValue: 100}],
      },
    },
  },
};
```

## 6. 性能检测与调试工具

1. **React DevTools Profiler**: 识别渲染瓶颈的最佳工具
2. **Chrome Performance面板**: 检测JavaScript执行和渲染性能
3. **WebPageTest.org**: 测试各种网络条件下的性能
4. **Vite Bundle Analyzer**: 分析bundle大小
   ```bash
   npm install rollup-plugin-visualizer --save-dev
   ```
   
   配置到`vite.config.ts`:
   ```typescript
   import { visualizer } from 'rollup-plugin-visualizer';
   
   export default defineConfig({
     plugins: [
       // ...其他插件
       visualizer({
         open: true,
         gzipSize: true,
         brotliSize: true,
       }),
     ],
   });
   ``` 
 
 