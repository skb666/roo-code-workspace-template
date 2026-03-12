# 完整应用案例：Web 应用开发

## 案例背景

**项目**：开发一个任务管理 Web 应用
**技术栈**：React + Node.js + MongoDB
**目标**：实现用户注册、登录、任务 CRUD 功能
**预计周期**：3-5 个会话

---

## 阶段零：模式匹配

### 任务分析

```
任务特征：
- 多步骤项目
- 子任务可并行（前端/后端）
- 需要迭代验证

匹配模式：Orchestrator-Workers + Parallelization + Evaluator-Optimizer
```

### 工作流设计

```
协调器（Orchestrator）
    │
    ├── 架构设计（Architect）
    │
    ├── 并行开发（Parallelization）
    │   ├── 前端开发（Code）
    │   └── 后端开发（Code）
    │
    ├── 集成测试（Code）
    │
    └── 迭代优化（Evaluator-Optimizer）
        ├── 验证（Debug/Ask）
        └── 修复（Code）
```

---

## 阶段一：初始化

### 创建项目状态目录

```bash
mkdir -p .roo/project-state
```

### context.md

```markdown
# 项目上下文

## 项目概览

- **项目名称**：Task Manager
- **开始时间**：2026-03-11
- **目标**：开发一个支持用户认证和任务管理的 Web 应用

## 技术栈

- 前端：React 18, TailwindCSS
- 后端：Node.js, Express
- 数据库：MongoDB
- 认证：JWT

## 项目结构

```
task-manager/
├── client/           # React 前端
├── server/           # Node.js 后端
├── .roo/             # Roo 状态文件
└── README.md
```

## 核心约束

1. 使用 ES6+ 语法
2. API 遵循 RESTful 规范
3. 前后端分离开发
4. 必须有测试覆盖

## 快速启动

```bash
# 后端
cd server && npm install && npm run dev

# 前端
cd client && npm install && npm start
```
```

### feature-status.json

```json
{
  "project": "task-manager",
  "version": "1.0.0",
  "last_updated": "2026-03-11T10:00:00Z",
  "summary": {
    "total": 8,
    "completed": 0,
    "in_progress": 0,
    "pending": 8,
    "blocked": 0
  },
  "features": [
    {
      "id": "F001",
      "priority": "critical",
      "category": "infra",
      "description": "项目初始化",
      "details": "创建项目结构，配置开发环境",
      "steps": [
        "验证目录结构正确",
        "验证依赖安装成功",
        "验证开发服务器可启动"
      ],
      "passes": false,
      "verified_by": null,
      "verified_at": null,
      "notes": "",
      "dependencies": []
    },
    {
      "id": "F002",
      "priority": "critical",
      "category": "auth",
      "description": "用户注册",
      "details": "用户可以使用邮箱注册账户",
      "steps": [
        "访问注册页面",
        "填写邮箱和密码",
        "提交表单",
        "验证账户创建成功"
      ],
      "passes": false,
      "verified_by": null,
      "verified_at": null,
      "notes": "",
      "dependencies": ["F001"]
    },
    {
      "id": "F003",
      "priority": "critical",
      "category": "auth",
      "description": "用户登录",
      "details": "注册用户可以登录系统",
      "steps": [
        "访问登录页面",
        "输入邮箱和密码",
        "提交表单",
        "验证登录成功，跳转到主页"
      ],
      "passes": false,
      "verified_by": null,
      "verified_at": null,
      "notes": "",
      "dependencies": ["F002"]
    },
    {
      "id": "F004",
      "priority": "high",
      "category": "api",
      "description": "任务创建 API",
      "details": "已登录用户可以创建任务",
      "steps": [
        "发送 POST /api/tasks 请求",
        "验证返回 201 状态码",
        "验证数据库中创建了任务"
      ],
      "passes": false,
      "verified_by": null,
      "verified_at": null,
      "notes": "",
      "dependencies": ["F003"]
    },
    {
      "id": "F005",
      "priority": "high",
      "category": "api",
      "description": "任务列表 API",
      "details": "用户可以获取自己的任务列表",
      "steps": [
        "发送 GET /api/tasks 请求",
        "验证返回 200 状态码",
        "验证返回的任务列表正确"
      ],
      "passes": false,
      "verified_by": null,
      "verified_at": null,
      "notes": "",
      "dependencies": ["F004"]
    },
    {
      "id": "F006",
      "priority": "high",
      "category": "ui",
      "description": "任务列表页面",
      "details": "前端展示用户任务列表",
      "steps": [
        "登录后访问任务页面",
        "验证任务列表正确显示",
        "验证可以创建新任务"
      ],
      "passes": false,
      "verified_by": null,
      "verified_at": null,
      "notes": "",
      "dependencies": ["F005"]
    },
    {
      "id": "F007",
      "priority": "medium",
      "category": "api",
      "description": "任务更新 API",
      "details": "用户可以更新任务状态",
      "steps": [
        "发送 PUT /api/tasks/:id 请求",
        "验证返回 200 状态码",
        "验证任务状态已更新"
      ],
      "passes": false,
      "verified_by": null,
      "verified_at": null,
      "notes": "",
      "dependencies": ["F004"]
    },
    {
      "id": "F008",
      "priority": "medium",
      "category": "api",
      "description": "任务删除 API",
      "details": "用户可以删除任务",
      "steps": [
        "发送 DELETE /api/tasks/:id 请求",
        "验证返回 200 状态码",
        "验证任务已从数据库删除"
      ],
      "passes": false,
      "verified_by": null,
      "verified_at": null,
      "notes": "",
      "dependencies": ["F004"]
    }
  ]
}
```

### 初始 Git 提交

```bash
git init
git add .
git commit -m "chore: 项目初始化

- 创建项目结构
- 初始化状态管理文件
- 配置开发环境"
```

---

## 阶段二：增量执行

### Session #1 - 项目初始化

**目标**：完成 F001 项目初始化

**执行步骤**：

1. 创建项目目录结构
2. 初始化前端项目 (create-react-app)
3. 初始化后端项目 (express-generator)
4. 安装依赖
5. 验证开发服务器可启动

**验证**：

```bash
# 前端
cd client && npm start
# 验证：浏览器打开 localhost:3000，看到 React 页面

# 后端
cd server && npm run dev
# 验证：浏览器打开 localhost:5000，看到 API 响应
```

**更新状态**：

- F001.passes = true
- 提交 Git

---

### Session #2 - 用户注册

**目标**：完成 F002 用户注册

**恢复状态**：

```markdown
1. pwd → /home/user/task-manager
2. git log --oneline -3
3. 读取 feature-status.json → F002 是下一个待完成功能
```

**执行步骤**：

1. 设计用户数据模型
2. 实现注册 API
3. 实现前端注册页面
4. 编写单元测试
5. 端到端测试

**验证**：

| 步骤 | 操作 | 结果 |
|------|------|------|
| 1 | 访问 /register | ✅ 显示注册页面 |
| 2 | 填写邮箱密码 | ✅ 表单验证通过 |
| 3 | 提交表单 | ✅ 注册成功 |
| 4 | 检查数据库 | ✅ 用户已创建 |

**更新状态**：

- F002.passes = true
- 提交 Git

---

### Session #3 - 用户登录

**目标**：完成 F003 用户登录

**恢复状态**：

```markdown
1. pwd → /home/user/task-manager
2. git log --oneline -3
3. 读取 feature-status.json → F003 是下一个待完成功能
```

**执行步骤**：

1. 实现 JWT 生成逻辑
2. 实现登录 API
3. 实现前端登录页面
4. 实现登录状态持久化
5. 编写测试

**关键决策记录**：

```markdown
## ADR-001: 选择 JWT 作为认证方案

- **日期**：2026-03-11
- **状态**：已采纳
- **背景**：需要无状态的认证机制
- **决策**：使用 JWT
- **理由**：无需服务器端会话存储，适合前后端分离架构
- **后果**：需要处理 Token 刷新逻辑
```

**验证**：

| 步骤 | 操作 | 结果 |
|------|------|------|
| 1 | 访问 /login | ✅ 显示登录页面 |
| 2 | 输入已注册用户信息 | ✅ 表单验证通过 |
| 3 | 提交表单 | ✅ 登录成功，跳转主页 |
| 4 | 刷新页面 | ✅ 仍然保持登录状态 |

**更新状态**：

- F003.passes = true
- 提交 Git
- 更新 decisions.md

---

### Session #4 - 任务 CRUD（并行开发）

**目标**：完成 F004, F005, F007, F008

**并行策略**：

```
┌─────────────────┐     ┌─────────────────┐
│   前端开发       │     │   后端开发       │
│  (Code 模式)    │     │  (Code 模式)    │
│                 │     │                 │
│ - 任务列表页面  │     │ - 任务 CRUD API │
│ - 任务创建表单  │     │ - 数据模型      │
│ - 任务更新组件  │     │ - 权限验证      │
└─────────────────┘     └─────────────────┘
         │                       │
         └───────────┬───────────┘
                     │
                     ▼
              ┌─────────────┐
              │   集成测试   │
              └─────────────┘
```

**后端子任务**：

```javascript
new_task({
  mode: "code",
  message: `
## 上下文
项目是任务管理应用，已有用户认证功能。

## 范围
实现任务 CRUD API：
1. POST /api/tasks - 创建任务
2. GET /api/tasks - 获取任务列表
3. PUT /api/tasks/:id - 更新任务
4. DELETE /api/tasks/:id - 删除任务

## 要求
- 需要认证（使用已实现的 JWT 中间件）
- 任务属于当前用户
- 包含单元测试

## 完成后
使用 attempt_completion 返回 API 端点列表和测试结果摘要。
`
});
```

**前端子任务**：

```javascript
new_task({
  mode: "code",
  message: `
## 上下文
项目是任务管理应用，后端已有任务 CRUD API。

## 范围
实现任务管理前端页面：
1. 任务列表页面
2. 创建任务表单
3. 更新任务状态
4. 删除任务

## 要求
- 使用 React + TailwindCSS
- 调用后端 API
- 处理加载和错误状态

## 完成后
使用 attempt_completion 返回实现的组件列表。
`
});
```

---

## 阶段三：状态持久化

### session-log.md 示例

```markdown
## Session #4 - 2026-03-11 16:00

**目标**：完成任务 CRUD 功能

**完成情况**：
- [x] 实现任务创建 API
- [x] 实现任务列表 API
- [x] 实现任务更新 API
- [x] 实现任务删除 API
- [x] 实现前端任务页面
- [x] 集成测试

**关键决策**：
- 任务数据包含：title, description, status, dueDate
- 状态枚举：todo, in_progress, done

**Git 提交**：
- `feat(api): 实现任务 CRUD API` (a1b2c3d)
- `feat(ui): 实现任务管理页面` (e4f5g6h)
- `test: 添加任务 API 单元测试` (i7j8k9l)

**下一步**：
- 项目级验证
- 部署准备
```

---

## 阶段四：验证闭环

### 功能级验证（以 F006 为例）

```markdown
## F006 任务列表页面验证

| 检查项 | 结果 | 备注 |
|--------|------|------|
| 页面可访问 | ✅ | |
| 任务列表显示 | ✅ | |
| 创建任务功能 | ✅ | |
| 更新任务状态 | ✅ | |
| 删除任务 | ✅ | |
| 加载状态处理 | ✅ | |
| 错误状态处理 | ✅ | |

**验证结论**：✅ 通过
```

### 项目级验证

```markdown
## 项目验证

| 指标 | 目标值 | 实际值 | 结果 |
|------|--------|--------|------|
| 功能完成 | 8/8 | 8/8 | ✅ |
| 测试覆盖率 | ≥70% | 78% | ✅ |
| 测试通过率 | 100% | 100% | ✅ |
| 已知高危 Bug | 0 | 0 | ✅ |

**验证结论**：✅ 可以交付
```

---

## 案例总结

### 成功要素

1. **清晰的状态管理**
   - feature-status.json 明确功能状态
   - session-log.md 记录每次会话
   - decisions.md 记录关键决策

2. **增量执行**
   - 每次会话专注一个功能
   - 验证后才标记完成
   - 每次会话结束留下干净状态

3. **并行加速**
   - 前后端并行开发
   - 集成后再验证
   - 提高整体效率

4. **完整验证**
   - 单元测试 + 端到端测试
   - 功能级 + 项目级验证
   - 确保真正完成

### 耗时统计

| 会话 | 功能 | 耗时 |
|------|------|------|
| #1 | 项目初始化 | 30分钟 |
| #2 | 用户注册 | 1小时 |
| #3 | 用户登录 | 1小时 |
| #4 | 任务 CRUD | 2小时 |
| #5 | 验证和部署 | 30分钟 |
| **总计** | **8个功能** | **5小时** |
