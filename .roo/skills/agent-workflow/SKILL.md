---
name: agent-workflow
description: Agent 全流程闭环执行框架。适用于长时任务、多步骤项目、需要跨上下文窗口的复杂任务。包含模式匹配、初始化、增量执行、状态持久化、验证闭环五个阶段。
---

# Agent Workflow - 全流程闭环执行框架

## 快速参考

| 阶段 | 核心动作 | Roo 工具 |
|------|----------|----------|
| ① 模式匹配 | 选择工作流模式 | `switch_mode` |
| ② 初始化 | 创建状态文件 | 文件操作 + `execute_command` |
| ③ 增量执行 | 完成单个功能 | `new_task` + `execute_command` |
| ④ 状态持久化 | 更新状态文件 | 文件操作 + Git |
| ⑤ 验证闭环 | 确保真正完成 | `attempt_completion` |

## Roo 能力

**命令行工具**：可调用 `execute_command` 执行任意 shell 命令
- 运行测试：`npm test`、`pytest` 等
- 构建项目：`npm run build`、`make` 等
- 安装依赖：`npm install`、`pip install` 等

**Git 版本管理**：
- 初始化：`git init`、`git clone`
- 提交：`git add`、`git commit`
- 分支：`git branch`、`git checkout`、`git merge`
- 状态：`git status`、`git log`、`git diff`

## 使用场景

**✅ 使用此技能**：
- 长时任务（跨越多个上下文窗口）
- 复杂多步骤项目
- 需要状态恢复和追溯
- 子任务需要委派给不同模式

**❌ 不使用此技能**：
- 简单单次交互可完成的任务
- 仅需查询信息
- 步骤固定无需规划

## 核心原则

```
① 保持简单   - 简单可组合模式 > 复杂框架
② 透明规划   - 明确展示每一步计划和进度
③ 精心设计   - 工具接口像 HCI 一样用心
④ 增量交付   - 每次完成一个可验证的小任务
```

---

## 工作流程

### 阶段一：模式匹配（Route）

**目的**：识别任务类型，选择合适的工作流模式和 Roo 模式

**决策树**：

```
任务是否有固定步骤？
├── 是 → Prompt Chaining（串行 new_task）
└── 否 → 需要动态规划？
    ├── 是 → Orchestrator-Workers（协调器模式）
    └── 否 → 能否并行执行？
        ├── 是 → Parallelization（并行 new_task）
        └── 否 → 需要迭代改进？
            ├── 是 → Evaluator-Optimizer（Code/Debug 循环）
            └── 否 → Autonomous Agent（完整循环）
```

**Roo 模式映射**：

| 工作流模式 | 推荐 Roo 模式 | 工具调用示例 |
|-----------|-------------|-------------|
| Prompt Chaining | `code` / `ask` | 串行 `new_task` |
| Routing | 多模式切换 | `switch_mode` |
| Parallelization | `code` | 并行 `new_task` |
| Orchestrator-Workers | `orchestrator` | `new_task` + `update_todo_list` |
| Evaluator-Optimizer | `code` + `debug` | `switch_mode` 循环 |
| Autonomous Agent | `orchestrator` | 完整工具链 |

**详细方法**：[`references/workflow-patterns.md`](references/workflow-patterns.md)

---

### 阶段二：初始化（Initialize）

**目的**：建立任务执行环境，创建状态持久化文件

**执行步骤**：

1. **创建状态目录**
   ```
   .roo/project-state/
   ├── context.md           # 项目上下文摘要
   ├── decisions.md         # 架构决策记录
   ├── feature-status.json  # 功能完成状态（JSON 格式）
   └── session-log.md       # 会话日志
   ```

2. **生成功能清单**（JSON 格式）
   ```json
   {
     "features": [
       {
         "id": "F001",
         "description": "功能描述",
         "steps": ["验证步骤1", "验证步骤2"],
         "passes": false
       }
     ]
   }
   ```

3. **初始化 TODO 列表**
   ```
   update_todo_list({
     todos: `
     - [-] 初始化项目状态
     - [ ] 功能 F001: xxx
     - [ ] 功能 F002: xxx
     - [ ] 验证闭环
     `
   })
   ```

4. **Git 初始化提交**
   ```bash
   # 使用 execute_command
   git add .roo/project-state/
   git commit -m "chore: 初始化项目状态管理"
   ```

**模板**：[`templates/init-state.md`](templates/init-state.md)

---

### 阶段三：增量执行（Execute）

**目的**：每次专注于一个功能，完成后留下清晰状态

**核心原则**：
- ❌ 一次只做一个功能
- ❌ 不标记未验证的功能为完成
- ✅ 每次会话结束时代码可工作

**执行流程**：

```
1. 恢复上下文
   ├── 读取 session-log.md（上次进度）
   ├── 读取 feature-status.json（当前状态）
   └── 读取 decisions.md（已做决策）

2. 选择单个功能 → 从清单中选择优先级最高的未完成功能

3. 委派执行 → 根据功能类型选择合适的 Roo 模式

4. **验证完成**
   ```bash
   # 使用 execute_command 运行测试
   npm test              # 前端项目
   pytest                # Python 项目
   go test ./...         # Go 项目
   ```

5. **更新状态文件**
   - 更新 `feature-status.json`
   - 更新 `session-log.md`

6. **Git 提交记录**
   ```bash
   git add .
   git commit -m "feat: 完成功能 F001 - 用户登录"
   ```

7. **更新 TODO 列表**
   ```javascript
   update_todo_list({
     todos: `
     - [x] 功能 F001: 用户登录
     - [-] 功能 F002: 用户注册
     - [ ] 验证闭环
     `
   })
   ```
```

**new_task 调用示例**：

```javascript
new_task({
  mode: "code",  // 或 "architect", "debug" 等
  message: `
## 任务：实现用户登录功能

### 上下文
- 项目：[项目名]
- 技术栈：[技术栈]
- 相关文件：[文件列表]

### 要求
- 实现账号密码登录
- 实现 JWT 令牌生成
- 包含输入验证和错误处理

### 完成标准
- 单元测试通过
- API 可正常调用
- 使用 attempt_completion 返回实现摘要

### 注意
- 仅执行上述指令，不得偏离
- 完成后使用 attempt_completion 报告结果
  `,
  todos: `
  - [ ] 分析现有代码结构
  - [ ] 实现登录接口
  - [ ] 添加 JWT 支持
  - [ ] 编写测试
  `
})
```

**详细方法**：[`references/incremental-execution.md`](references/incremental-execution.md)

---

### 阶段四：状态持久化（Persist）

**目的**：确保任务状态可在上下文窗口间传递

**持久化策略**：

| 策略 | 场景 | 实现 |
|------|------|------|
| Compaction | 会话内过长 | 智能总结关键决策 |
| Structured Notes | 跨会话 | 写入 `.roo/project-state/` |
| Git History | 代码追溯 | 频繁提交，清晰消息 |
| Feature Status | 进度跟踪 | JSON 状态文件 |

**会话结束前必须更新**：

```
1. context.md      → 更新已完成工作摘要
2. decisions.md    → 记录新决策（如有）
3. feature-status.json → 更新功能状态
4. session-log.md  → 添加本次会话记录
```

**模板**：[`templates/session-log.md`](templates/session-log.md)

---

### 阶段五：验证闭环（Verify）

**目的**：确保每个功能真正完成，避免过早宣布胜利

**功能级验证清单**：

```markdown
- [ ] 代码可运行（无语法/运行时错误）
- [ ] 单元测试通过
- [ ] 端到端测试通过
- [ ] 边界情况处理
- [ ] 错误处理完善
- [ ] 代码已 Review
- [ ] 文档已更新
```

**项目级验证清单**：

```markdown
- [ ] 所有功能完成
- [ ] 所有测试通过
- [ ] 无已知严重 Bug
- [ ] 代码可部署
- [ ] 文档完整
```

**attempt_completion 使用**：

```javascript
attempt_completion({
  result: `
## 任务完成报告

### 完成的功能
- F001: 用户登录 ✓
- F002: 权限管理 ✓
- F003: 数据导出 ✓

### 关键决策
- 选择 JWT 作为认证方案
- 使用 Redis 缓存会话

### 已知问题
- [如有] 描述已知限制

### 后续建议
- [如有] 改进建议
  `
})
```

**模板**：[`templates/verify-checklist.md`](templates/verify-checklist.md)

---

## 上下文工程策略

### 原则：上下文 = 有限资源

```
每个 Token 都消耗注意力预算
→ 选择最小的高信号 Token 集合
→ 最大化期望结果的可能性
```

### 三大策略

**1. 按需检索（Just-in-Time Retrieval）**
```
❌ 预先加载所有可能相关的文件
✅ 维护轻量引用，按需加载
   - 保存文件路径而非内容
   - 用 glob/grep 定位后读取
   - 用 head/tail 预览大文件
```

**2. 工具结果清理（Tool Result Clearing）**
```
❌ 在历史中保留完整工具结果
✅ 只保留关键摘要
   - 深层历史可总结后丢弃
   - 保留关键错误和决策依据
```

**3. 子代理隔离（Sub-agent Isolation）**
```
┌─────────────┐
│ 主 Agent    │ ← 保持轻量，专注协调
└──────┬──────┘
       ├──▶ 子 Agent A ──▶ 返回精简摘要
       ├──▶ 子 Agent B ──▶ 返回精简摘要
       └──▶ 子 Agent C ──▶ 返回精简摘要

好处：子 Agent 可大量探索，主 Agent 只接收 1-2k Token 摘要
```

**详细方法**：[`references/context-engineering.md`](references/context-engineering.md)

---

## 与其他技能的协作

| 技能 | 协作点 | 使用场景 |
|------|--------|----------|
| `task-master` | 任务拆解和目标设定 | 项目规划阶段 |
| `code-review-expert` | 代码质量验证 | 验证阶段 |
| `web-search` | 信息收集和研究 | 需要外部信息时 |
| `drawio` | 架构图和流程图 | 设计阶段 |

---

## 快速开始

```
用户输入：我有一个复杂任务需要执行 →

1. 【阶段一】模式匹配 → 确定工作流模式
2. 【阶段二】初始化 → 创建项目状态文件、功能清单
3. 【阶段三】增量执行 → 每次完成一个功能
4. 【阶段四】状态持久化 → 更新状态、提交记录
5. 【阶段五】验证闭环 → 确保真正完成
```

---

## 文件结构

```
agent-workflow/
├── SKILL.md                     # 本文件：技能入口
├── references/                  # 详细方法指南
│   ├── workflow-patterns.md     # 六种工作流模式详解
│   ├── incremental-execution.md # 增量执行方法
│   └── context-engineering.md   # 上下文工程策略
├── templates/                   # 可直接套用的模板
│   ├── init-state.md            # 初始化状态模板
│   ├── session-log.md           # 会话日志模板
│   ├── verify-checklist.md      # 验证清单模板
│   └── feature-status.json      # 功能状态模板
└── examples/                    # 完整应用案例
    └── web-app-development.md   # Web 应用开发案例
```

---

## 注意事项

1. **功能清单使用 JSON 格式** - 减少误改风险
2. **一次一个功能** - 避免贪多
3. **验证是必须步骤** - 不可跳过
4. **状态持久化** - 长时任务成功的关键
5. **使用 attempt_completion** - 完成后必须报告结果
