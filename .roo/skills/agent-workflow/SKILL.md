---
name: agent-workflow
description: Agent 全流程闭环执行框架。适用于长时任务、多步骤项目、需要跨上下文窗口的复杂任务。包含模式匹配、初始化、增量执行、状态持久化、验证闭环五个阶段。支持波浪式并行执行、快速模式和思考工具集成。
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
⑤ 波浪并行   - 分析依赖，独立任务并行执行
⑥ 适时思考   - 复杂决策点停下来思考
```

## 执行模式

|| 模式 | 适用场景 | 特点 |
|------|----------|------|
| **完整模式** | 复杂项目、长时任务 | 五阶段完整流程 |
| **快速模式** | 小任务、单一功能 | 简化流程，快速交付 |
| **波浪模式** | 多任务并行 | 依赖分析，分组并行 |

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
// ⚠️ 重要：子任务在全新上下文中执行，无父任务对话历史
new_task({
  mode: "code",  // 或 "architect", "debug" 等
  message: `
## 任务：实现用户登录功能

⚠️ **这是一个独立的上下文环境**
- 你没有父任务的对话历史
- 请使用 agent-workflow 技能来执行此任务
- 所有必需信息都在本消息中提供

### 上下文
- 项目：[项目名]
- 技术栈：[技术栈]
- 相关文件：[文件列表]
- 状态文件位置：.roo/project-state/

### 要求
- 实现账号密码登录
- 实现 JWT 令牌生成
- 包含输入验证和错误处理

### 完成标准
- 单元测试通过
- API 可正常调用
- 使用 attempt_completion 返回实现摘要

### 执行指引
1. 首先读取状态文件恢复上下文
2. 按照 agent-workflow 技能执行
3. 完成后更新状态文件
4. Git 提交
5. 使用 attempt_completion 报告结果
  `,
  todos: `
  - [ ] 读取状态文件恢复上下文
  - [ ] 分析现有代码结构
  - [ ] 实现登录接口
  - [ ] 添加 JWT 支持
  - [ ] 编写测试
  - [ ] 更新状态文件
  `
})
```

**独立上下文原则**：

```
┌─────────────────────────────────────────────────────────────────┐
│                    子任务独立上下文                               │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  父任务上下文                      子任务上下文                  │
│  ┌──────────────┐                ┌──────────────┐              │
│  │ 对话历史     │                │ 全新环境     │              │
│  │ 工具调用结果 │    new_task    │ 无父任务历史 │              │
│  │ 中间状态     │ ────────────▶  │ 仅消息内容   │              │
│  └──────────────┘                └──────────────┘              │
│                                                                 │
│  关键点：                                                        │
│  1. 子任务看不到父任务的对话历史                                  │
│  2. 所有必需信息必须在 message 中提供                            │
│  3. 通过状态文件传递跨上下文信息                                  │
│  4. 子任务应按 agent-workflow 独立执行                           │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
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

## 波浪式并行执行

### 概念

分析任务依赖关系，将独立任务分组，每组（波浪）并行执行，最大化效率。

```
传统顺序执行（总时间 = T1 + T2 + T3 + T4）:
[A1] ──▶ [A2] ──▶ [A3] ──▶ [A4]

波浪式并行执行（总时间 ≈ T1 + T3）:
第1波: [A1] ──┬──▶ 第2波: [A3]
             │
       [A2] ─┴──▶ [A4]
```

### 实现步骤

**1. 依赖分析**

```markdown
分析每个任务的前置依赖：
- A1: 无依赖
- A2: 无依赖
- A3: 依赖 A1
- A4: 依赖 A1, A2
- A5: 依赖 A3, A4
```

**2. 波浪分组**

```javascript
// 将任务按依赖关系分组
const waves = groupByDependencies(tasks)
// 结果：
// wave 0: [A1, A2]  // 无依赖
// wave 1: [A3, A4]  // 依赖 wave 0
// wave 2: [A5]      // 依赖 wave 1
```

**3. 并行执行**

```javascript
// 在 Roo 中实现波浪式并行
// ⚠️ 每个子任务都是独立上下文，需提供完整信息
for (const wave of waves) {
  // 当前波浪的所有任务并行启动
  const results = await Promise.all(
    wave.map(task => 
      new_task({
        mode: "code",
        message: `
## 任务：${task.id} - ${task.name}

⚠️ **独立上下文环境** - 使用 agent-workflow 技能执行

### 上下文
- 项目状态文件：.roo/project-state/
- 依赖任务：${task.dependencies}

### 要求
${task.requirements}

### 执行指引
1. 读取状态文件恢复上下文
2. 按 agent-workflow 技能执行
3. 完成后更新状态文件并提交
        `
      })
    )
  )
  
  // 等待当前波浪全部完成，再进入下一波浪
  await processResults(results)
}
```

### 适用场景

- ✅ 多个独立功能可同时开发
- ✅ 前后端分离开发
- ✅ 多模块并行测试
- ❌ 任务间有强依赖关系
- ❌ 需要频繁同步的任务

### 失败恢复机制

**问题**：波浪中某个任务失败，后续依赖任务无法继续

**解决方案**：

```javascript
// 带重试的波浪执行
const results = { success: [], failed: [], pending: [] }

for (const wave of waves) {
  // 执行当前波浪
  const waveResults = await Promise.allSettled(
    wave.map(task => executeTask(task))
  )
  
  // 分类结果
  waveResults.forEach((result, index) => {
    if (result.status === 'fulfilled') {
      results.success.push(wave[index])
    } else {
      results.failed.push({
        task: wave[index],
        error: result.reason,
        retryable: isRetryable(result.reason)
      })
    }
  })
  
  // 检查是否可以继续
  const nextWaveDeps = waves[waveIndex + 1]?.flatMap(t => t.dependencies) || []
  const blockedTasks = nextWaveDeps.filter(dep => results.failed.includes(dep))
  
  if (blockedTasks.length > 0) {
    // 有依赖任务失败，标记受影响任务
    results.pending.push(...blockedTasks)
    console.warn(`⚠️ ${blockedTasks.length} 个任务因依赖失败被阻塞`)
  }
}
```

**状态文件记录失败**：

```markdown
# STATE.md 失败记录格式

## 阻塞项
- A3: API 开发
  - 状态: blocked
  - 原因: 依赖任务 A1 失败
  - 失败详情: [错误信息]
  - 重试建议: [如何修复]

## 失败历史
- [2026-03-13 14:30] A1 失败 - 数据库连接超时
```

### 并发冲突处理

**问题**：多个并行任务可能修改同一文件

**预防策略**：

```markdown
1. 任务规划时识别文件冲突
   - 检查任务文件列表是否重叠
   - 有重叠的任务放入不同波浪

2. 文件所有权声明
   - 在 PLAN.md 中明确每个任务负责的文件
   - 禁止修改其他任务的文件

3. 状态文件原子更新
   - 使用 JSON 格式便于合并
   - 每个任务更新独立区域
```

**冲突检测模板**：

```javascript
// 在规划阶段检测文件冲突
const fileOwnership = {}
tasks.forEach(task => {
  task.files.forEach(file => {
    if (fileOwnership[file]) {
      console.warn(`⚠️ 文件冲突: ${file} 被 ${fileOwnership[file]} 和 ${task.id} 同时修改`)
      // 将冲突任务放入不同波浪
    }
    fileOwnership[file] = task.id
  })
})
```

### 子任务结果汇总

**问题**：并行任务结果分散，难以追踪

**解决方案**：使用结构化的结果收集

```javascript
// 父任务收集所有子任务结果
const summary = {
  totalTasks: 0,
  completed: 0,
  failed: 0,
  results: []
}

// 每个子任务返回标准化格式
attempt_completion({
  result: `
## 任务完成报告: ${taskId}

### 交付物
- 文件: src/auth/login.ts
- 功能: 用户登录 API

### 测试结果
- 单元测试: ✓ 12/12 通过
- 集成测试: ✓ 5/5 通过

### 关键决策
- 使用 JWT 认证

### 后续任务依赖
- A4 需要: 登录接口地址 /api/auth/login
  `
})
```

**汇总模板**：

```markdown
# 波浪执行汇总报告

## 执行概览
- 总任务: 10
- 成功: 8
- 失败: 1
- 阻塞: 1

## 各波浪结果

### Wave 1 (并行)
| 任务 | 状态 | 交付物 |
|------|------|--------|
| A1 | ✓ | 数据库 Schema |
| A2 | ✓ | 前端骨架 |

### Wave 2 (并行)
| 任务 | 状态 | 交付物 |
|------|------|--------|
| A3 | ✓ | 认证 API |
| A4 | ✗ | 集成测试 - 依赖 A1 修复 |

## 下一步
1. 修复 A1 数据库连接问题
2. 重试 A4 集成测试
```

---

## 快速模式

### 适用场景

- 小功能实现
- Bug 修复
- 配置调整
- 单文件修改

### 简化流程

```
完整模式 (5 阶段):
模式匹配 → 初始化 → 增量执行 → 状态持久化 → 验证闭环

快速模式 (3 步骤):
快速确认 → 执行 → 验证
```

### 执行模板

```markdown
## 快速任务: [任务名称]

### 确认
- 目标: [一句话目标]
- 范围: [影响范围]

### 执行
- [ ] 步骤 1
- [ ] 步骤 2

### 验证
- [ ] 基本功能测试
- [ ] 无回归

### 完成标准
[如何判断任务完成]
```

---

## 思考工具集成

在复杂决策点，调用 `think-tool` 技能进行深入分析。

### 触发条件

```markdown
自动触发思考的场景：
1. 需要从 3+ 方案中选择
2. 涉及架构决策
3. 影响范围不明确
4. 错误代价较高
```

### 集成示例

```markdown
## 在阶段二（初始化）的集成

规划任务时：
1. 识别候选方案
2. 调用 think-tool 分析
3. 记录决策依据
4. 继续执行

## 在阶段三（增量执行）的集成

执行前检查：
1. 当前任务是否需要思考？
2. 如需要，停下来分析
3. 明确方案后再执行
```

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
| `think-tool` | 复杂决策分析 | 决策节点 |
| `gsd-workflow` | 规范驱动开发 | 生产级项目 |
| `web-search` | 信息收集和研究 | 需要外部信息时 |
| `code-review-expert` | 代码质量验证 | 验证阶段 |
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
6. **失败要有记录** - 便于恢复和重试
7. **并行任务检查文件冲突** - 避免合并冲突

---

## 状态文件管理

### 膨胀问题

长期项目可能导致状态文件过大，影响上下文效率。

### 分层管理策略

```
.roo/project-state/
├── active/                    # 活跃状态（常加载）
│   ├── current-phase.json     # 当前阶段任务
│   └── context-summary.md     # 上下文摘要
├── archive/                   # 归档状态（按需加载）
│   ├── phase-1-summary.md     # 阶段1完成摘要
│   ├── phase-2-summary.md     # 阶段2完成摘要
│   └── decisions-history.md   # 历史决策
└── meta/
    └── index.json             # 索引文件
```

### 状态精简规则

```markdown
规则：
1. 已完成任务只保留摘要，不保留详情
2. 决策记录只保留最终决策，不保留讨论过程
3. 超过 30 天的历史移入 archive/
4. 每个 Phase 完成后生成摘要
```

### 精简模板

```markdown
# Phase N 完成摘要

## 时间范围
2026-03-01 ~ 2026-03-14

## 交付物
- 功能 A: 已完成
- 功能 B: 已完成
- 功能 C: 已完成

## 关键决策
1. 选择 PostgreSQL 作为数据库
2. 使用 Redis 做会话缓存

## 遗留问题
- [如有] 描述

## 文件变更
- 新增: 45 文件
- 修改: 23 文件
- 删除: 5 文件

## Git 提交
- 提交数: 28
- 最后提交: abc123
```

---

## 技能选择指南

### 场景决策树

```
你的任务是什么？
│
├─ 生产级项目开发 ─────────────────▶ gsd-workflow
│   └─ 需要规范文档、阶段规划、原子执行
│
├─ 复杂多步骤任务 ─────────────────▶ agent-workflow
│   └─ 需要状态持久化、增量执行
│
├─ 任务拆解和规划 ─────────────────▶ task-master
│   └─ 需要WBS分解、SMART目标
│
├─ 复杂决策分析 ───────────────────▶ think-tool
│   └─ 多方案选择、架构决策
│
└─ 简单任务 ───────────────────────▶ 直接执行
    └─ 不需要特殊技能
```

### 技能组合建议

| 场景 | 推荐组合 | 说明 |
|------|----------|------|
| 新项目启动 | gsd-workflow → task-master | 先规划后执行 |
| 复杂功能开发 | agent-workflow + think-tool | 执行中做决策 |
| 多模块并行 | task-master → agent-workflow (波浪模式) | 规划后并行执行 |
| 问题排查 | think-tool → agent-workflow (debug模式) | 分析后修复 |

### 切换时机

```markdown
gsd-workflow → agent-workflow
  当：规划完成，开始执行
  动作：读取 GSD 状态文件，继续执行

task-master → agent-workflow
  当：任务拆解完成，需要执行
  动作：按工作包创建子任务

agent-workflow → think-tool
  当：遇到复杂决策点
  动作：停下来分析，记录决策后继续
```
