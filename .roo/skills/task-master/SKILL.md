---
name: task-master
description: 全流程任务管理专家。整合 WBS+MECE 任务拆解、SMART 目标设定、诺伊曼思维问题重构、金字塔原理汇报表达。支持 ROADMAP 阶段规划、原子任务计划、波浪式并行执行。适用于复杂项目管理、任务规划、进度跟踪和成果汇报。
---

# Task Master - 全流程任务管理专家

## 快速参考

| 阶段 | 核心方法 | Roo 工具 |
|------|----------|----------|
| ① 拆解 | WBS + MECE + RACI | `update_todo_list` |
| ② 规划 | SMART + 诺伊曼 | `new_task` |
| ③ 验证 | 验证清单 + PDCA | `execute_command` + `attempt_completion` |
| ④ 汇报 | 金字塔 + SCQA | `attempt_completion` |

## Roo 能力

**命令行工具**：可调用 `execute_command` 执行任意 shell 命令
- 运行测试验证完成度
- 执行构建和部署
- 数据处理和脚本执行

**Git 版本管理**：
- 每个工作包完成后提交：`git add` + `git commit`
- 查看进度：`git log --oneline`
- 回滚错误：`git reset`、`git revert`

## 使用场景

**✅ 使用此技能**：
- 复杂项目需要系统化拆解
- 需要制定可执行的目标
- 需要跟踪进度并验证完成
- 需要向上级/客户汇报成果
- 需要确保任务符合 MECE 原则

**❌ 不使用此技能**：
- 简单单任务无需拆解
- 仅需查询信息
- 已有成熟流程无需调整

## 方法论速查

| 方法 | 核心价值 | 应用阶段 |
|------|----------|----------|
| **WBS** | 层层分解，化繁为简 | 拆解 |
| **MECE** | 不重不漏，全面覆盖 | 拆解 |
| **SMART** | 目标清晰可衡量 | 规划 |
| **诺伊曼思维** | 原子拆解序列执行 | 规划 |
| **验证清单** | 质量把关 | 验证 |
| **金字塔原理** | 结论先行 | 汇报 |
| **SCQA** | 故事框架 | 汇报 |

---

## 工作流程

### 阶段一：任务拆解（Decompose）

**目的**：将复杂任务分解为可执行的工作包

**方法**：WBS 工作分解 + MECE 原则 + RACI 责任分配

**执行步骤**：

1. **用 5W2H 明确边界**
   ```
   What    - 做什么？
   Why     - 为什么做？
   Who     - 谁来做？
   When    - 何时完成？
   Where   - 在哪做？
   How     - 怎么做？
   How Much- 多少资源？
   ```

2. **WBS 层级分解**
   ```
   项目 → 任务 → 工作包 → 活动
   
   示例：
   用户系统（1.0）
   ├── 用户注册（1.1）
   │   ├── 注册页面开发（1.1.1）
   │   └── 注册 API 开发（1.1.2）
   └── 用户登录（1.2）
       ├── 登录页面开发（1.2.1）
       └── 登录 API 开发（1.2.2）
   ```

3. **MECE 检验**
   - ✅ 相互独立：没有两个工作包做同样的事
   - ✅ 完全穷尽：所有必要工作都已识别

4. **更新 TODO 列表**
   ```javascript
   update_todo_list({
     todos: `
     - [-] 任务拆解
     - [ ] 工作包 1.1.1: 注册页面开发
     - [ ] 工作包 1.1.2: 注册 API 开发
     - [ ] 工作包 1.2.1: 登录页面开发
     - [ ] 工作包 1.2.2: 登录 API 开发
     - [ ] 验证改进
     - [ ] 汇报表达
     `
   })
   ```

**输出**：WBS 分解树 + 工作包清单

**模板**：[`templates/wbs-template.md`](templates/wbs-template.md)

**详细方法**：[`references/wbs-mece-guide.md`](references/wbs-mece-guide.md)

---

### 阶段二：规划执行（Plan & Execute）

**目的**：为每个工作包设定明确目标和执行步骤

**方法**：SMART 目标设定 + 诺伊曼思维拆解

**执行步骤**：

1. **设定 SMART 目标**
   ```
   S (Specific)   - 具体的：做什么？谁负责？
   M (Measurable) - 可衡量：完成标准是什么？
   A (Achievable) - 可实现：有资源吗？
   R (Relevant)   - 相关性：与大局相关吗？
   T (Time-bound) - 有时限：何时完成？
   ```

2. **诺伊曼思维拆解**
   ```
   将复杂问题拆解为原子步骤：
   1. 识别当前状态
   2. 定义目标状态
   3. 列出中间状态序列
   4. 逐步执行
   ```

3. **委派任务（使用 new_task）**
   ```javascript
   // ⚠️ 子任务在全新上下文中执行，需提供完整信息
   new_task({
     mode: "code",
     message: `
   ## 任务：开发注册页面

   ⚠️ **独立上下文环境** - 使用 agent-workflow 技能执行

   ### SMART 目标
   - S: 开发用户注册表单页面
   - M: 表单可提交，验证正常
   - A: 使用现有组件库
   - R: 用户系统核心功能
   - T: 今天完成

   ### 上下文
   - 项目状态文件：.roo/project-state/
   - 相关文件：[文件列表]

   ### 要求
   - 包含邮箱、密码、确认密码字段
   - 客户端验证
   - 调用注册 API

   ### 执行指引
   1. 读取状态文件了解项目上下文
   2. 按 agent-workflow 技能执行
   3. 完成后更新状态文件并提交
   4. 使用 attempt_completion 返回结果
     `,
     todos: `
     - [ ] 读取状态文件恢复上下文
     - [ ] 创建表单组件
     - [ ] 添加字段验证
     - [ ] 集成 API 调用
     - [ ] 测试功能
     - [ ] 更新状态文件
     `
   })
   ```

4. **识别依赖关系**
   ```
   并行任务：可同时执行
   串行任务：有前置依赖
   
   示例：
   ├── 并行：前端页面 + 后端 API（可同时开发）
   └── 串行：API 开发 → API 集成测试
   ```

**输出**：SMART 目标卡 + 执行步骤

**模板**：[`templates/smart-goal-card.md`](templates/smart-goal-card.md)

**详细方法**：[`references/smart-neumann-guide.md`](references/smart-neumann-guide.md)

---

### 阶段二-B：ROADMAP 阶段规划

**目的**：将项目划分为可管理的阶段，设定里程碑

**方法**：阶段划分 + 里程碑定义 + 成功标准

**执行步骤**：

1. **阶段划分原则**
   ```
   每个阶段应该：
   - 有明确的目标和交付物
   - 可独立验证和部署
   - 时间跨度适中（1-2 周）
   - 有清晰的边界
   ```

2. **ROADMAP 结构**
   ```markdown
   # 开发路线图
   
   ## Phase 1: 核心功能
   - 时间：Week 1-2
   - 目标：实现核心用户流程
   - 功能：
     - REQ-001: 用户认证
     - REQ-002: 数据管理
   - 成功标准：
     - [ ] 核心流程可运行
     - [ ] 测试覆盖 > 80%
   
   ## Phase 2: 增强功能
   ...
   ```

3. **里程碑定义**
   ```
   里程碑特征：
   - 可验证的交付物
   - 明确的完成日期
   - 利益相关者可见
   - 决策检查点
   ```

**输出**：ROADMAP 文档 + 里程碑清单

---

### 阶段二-C：原子任务计划

**目的**：将工作包拆解为独立可执行的原子任务

**原则**：
```
原子任务特征：
1. 独立性 - 不依赖其他未完成任务
2. 完整性 - 完成后有可验证的交付物
3. 时限性 - 可在单次会话内完成
4. 可验证 - 有明确的验收标准
```

**任务依赖分析**：

```
步骤：
1. 列出所有原子任务
2. 识别每个任务的依赖
3. 构建依赖图
4. 分组波浪执行

示例：
[A1: 数据库设计] ──┬──▶ [A3: API 开发]
                  │
[A2: 前端骨架] ───┴──▶ [A4: 集成测试]
```

**波浪式并行执行**：

```javascript
// 将任务按依赖分组
const waves = [
  ['A1', 'A2'],  // 第1波：无依赖，并行执行
  ['A3', 'A4'],  // 第2波：依赖第1波，并行执行
  ['A5']         // 第3波：依赖第2波
]

// 每波内并行，波间顺序
for (const wave of waves) {
  await Promise.all(wave.map(task => executeTask(task)))
}
```

**原子任务模板**：

```markdown
### 任务 ID: A1
- **名称**: 数据库设计
- **描述**: 设计并创建用户表和订单表
- **依赖**: 无
- **预计时间**: 2h
- **文件**: `src/db/schema.sql`
- **验收标准**:
  - [ ] 表创建成功
  - [ ] 索引正确
  - [ ] 外键约束有效
- **状态**: pending
```

---

### 阶段三：验证改进（Verify & Improve）

**目的**：确保每个工作包真正完成，持续改进

**方法**：验证检查清单 + 5 Whys + PDCA

**执行步骤**：

1. **对照 SMART 检查完成度**
   ```markdown
   - [ ] 目标是否达成？
   - [ ] 衡量标准是否满足？
   - [ ] 资源是否有效利用？
   ```

2. **验证清单检查**
   ```markdown
   功能验证：
   - [ ] 功能按预期工作
   - [ ] 边界情况处理
   - [ ] 错误处理完善
   
   质量验证：
   - [ ] 代码规范
   - [ ] 测试覆盖
   - [ ] 文档更新
   ```

3. **偏差分析（如有）**
   ```
   5 Whys 分析：
   问题 → 为什么？→ 根因
   ```

4. **PDCA 改进**
   ```
   Plan   - 制定改进计划
   Do     - 执行改进
   Check  - 检查效果
   Act    - 标准化或新一轮
   ```

5. **命令行验证**
   ```bash
   # 使用 execute_command 运行测试
   npm test              # Node.js 项目
   pytest tests/         # Python 项目
   cargo test            # Rust 项目

   # 构建验证
   npm run build
   ```

6. **Git 提交记录**
   ```bash
   # 每个工作包完成后提交
   git add .
   git commit -m "feat: 完成工作包 1.1.1 - 注册页面"

   # 查看提交历史
   git log --oneline -10
   ```

7. **更新 TODO 列表**
   ```javascript
   update_todo_list({
     todos: `
     - [x] 任务拆解
     - [x] 工作包 1.1.1: 注册页面开发
     - [-] 工作包 1.1.2: 注册 API 开发
     - [ ] 工作包 1.2.1: 登录页面开发
     - [ ] 工作包 1.2.2: 登录 API 开发
     - [ ] 验证改进
     - [ ] 汇报表达
     `
   })
   ```

**输出**：验证报告 + 改进措施

**模板**：[`templates/verify-checklist.md`](templates/verify-checklist.md)

**详细方法**：[`references/verify-checklist.md`](references/verify-checklist.md)

---

### 阶段四：汇报表达（Report）

**目的**：结构化呈现项目成果

**方法**：金字塔原理 + SCQA 故事框架

**SCQA 框架**：

```
S (Situation)  - 背景：当前情况
C (Complication) - 冲突：遇到的问题
Q (Question)   - 问题：需要解决什么
A (Answer)     - 答案：解决方案和成果
```

**汇报结构**：

```
1. 核心结论（结论先行）
   
2. 支撑论点（归类分组）
   ├── 论点 1
   │   ├── 数据支撑
   │   └── 事实依据
   ├── 论点 2
   └── 论点 3

3. 后续计划
```

**使用 attempt_completion 汇报**：

```javascript
attempt_completion({
  result: `
   ## 用户系统开发完成报告
   
   ### 核心结论
   用户注册登录功能已完整实现，通过所有测试，可进入部署阶段。
   
   ### 完成情况
   | 功能 | 状态 | 测试覆盖 |
   |------|------|----------|
   | 用户注册 | ✓ | 95% |
   | 用户登录 | ✓ | 92% |
   | JWT 认证 | ✓ | 100% |
   
   ### 关键成果
   1. 完成注册/登录页面开发
   2. 实现 JWT 认证机制
   3. 编写完整单元测试
   
   ### 后续建议
   - 配置生产环境
   - 进行安全审计
   `
})
```

**模板**：[`templates/scqa-report-template.md`](templates/scqa-report-template.md)

**详细方法**：[`references/pyramid-scqa-guide.md`](references/pyramid-scqa-guide.md)

---

## 完整示例

查看 [`examples/complete-example.md`](examples/complete-example.md) 了解软件功能开发任务的完整管理流程。

---

## 与其他技能的协作

| 技能 | 协作点 | 使用场景 |
|------|--------|----------|
| `agent-workflow` | 执行框架 | 长时任务执行 |
| `think-tool` | 决策分析 | 方案选择时 |
| `gsd-workflow` | 规范驱动开发 | 生产级项目 |
| `code-review-expert` | 代码验证 | 验证阶段 |
| `drawio` | 可视化汇报 | 汇报阶段 |

---

## 文件结构

```
task-master/
├── SKILL.md                     # 本文件：技能入口
├── references/                  # 详细方法指南
│   ├── wbs-mece-guide.md        # WBS+MECE 拆解方法
│   ├── smart-neumann-guide.md   # SMART 目标 + 诺伊曼思维
│   ├── verify-checklist.md      # 验证检查清单
│   └── pyramid-scqa-guide.md    # 金字塔原理 + SCQA
├── templates/                   # 可直接套用的模板
│   ├── wbs-template.md          # WBS 分解模板
│   ├── smart-goal-card.md       # SMART 目标卡
│   ├── verify-checklist.md      # 验证清单模板
│   └── scqa-report-template.md  # SCQA 汇报模板
└── examples/                    # 完整应用案例
    └── complete-example.md      # 软件功能开发案例
```

---

## 注意事项

1. **每个阶段完成后更新 TODO 列表**
2. **使用 JSON 格式存储状态** - 减少误改风险
3. **完成每个工作包后使用 attempt_completion**
4. **汇报应结论先行，数据支撑**
5. **PDCA 循环贯穿整个项目**
