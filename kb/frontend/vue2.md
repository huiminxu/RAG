# 遇见 Vue3

Vue3 已经成为 Vue CLI 的默认版本，同时 Vue3 和 Vite 已经成为面试重点。

## Vue3 的变化

### 源码

1. **Monorepo** 管理源代码（如 Babel、Element Plus）
2. **TypeScript** 重写

### 性能

1. **Proxy** 代替 Vue2 的 `Object.defineProperty`
2. **BlockTree**、Slot 编译优化、Diff 算法优化

### API

- Composition API
- Hooks

## Vue3 如何使用

| 方式 | 说明 |
|------|------|
| CDN | 使用 CDN（Content Delivery Network）方式引入 Vue |
| 手动引入 | 下载 Vue 的 JS 文件，手动引入 |
| NPM | 通过 npm 包管理工具安装使用 |
| Vue CLI | 通过 Vue CLI 创建项目并使用 |

## 声明式 vs 命令式

- **声明式**（Vue）：描述结果，框架负责实现过程
- **命令式**（JavaScript）：逐步描述实现过程
  

  author: huiminxu