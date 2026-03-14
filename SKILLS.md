# 🧩 技能系统

> **AI Agent 工具集的核心能力** - 预装的 6 个核心技能，提供从任务规划到信息获取的全方位支持。

## 📋 技能概览

| 技能名称 | 位置 | 核心功能 | 适用场景 |
|----------|------|----------|----------|
| **web-search** | [`.roo/skills/web-search/`](.roo/skills/web-search/SKILL.md) | 网络搜索、结果聚合 | 需要实时信息、查找文档、搜索代码 |
| **web-reader** | [`.roo/skills/web-reader/`](.roo/skills/web-reader/SKILL.md) | 网页内容提取、元数据获取 | 读取文章、提取正文、批量处理 URL |
| **agent-workflow** | [`.roo/skills/agent-workflow/`](.roo/skills/agent-workflow/SKILL.md) | 全流程闭环执行框架 | 长时任务、多步骤项目、跨会话跟踪 |
| **gsd-workflow** | [`.roo/skills/gsd-workflow/`](.roo/skills/gsd-workflow/SKILL.md) | 规范驱动开发框架 | 生产级项目开发、解决 Context Rot 问题 |
| **task-master** | [`.roo/skills/task-master/`](.roo/skills/task-master/SKILL.md) | 全流程任务管理专家 | 复杂项目管理、任务规划、进度跟踪 |
| **think-tool** | [`.roo/skills/think-tool/`](.roo/skills/think-tool/SKILL.md) | 智能技能调度器与思考工具 | 复杂决策、多技能协调、结构化思考 |

---

## 🌐 Web Search - 网络搜索技能

**位置**: [`.roo/skills/web-search/`](.roo/skills/web-search/SKILL.md)

通过 SearXNG 提供网络搜索能力：

### 工具列表

| 工具 | 用途 | 搜索方式 |
|------|------|----------|
| `mcp__searxng-search__web_search` | 通用搜索 | engines: bing, baidu, 360search, sogou |
| `mcp__searxng-search__web_search` | 新闻搜索 | query + "新闻", time_range: day |
| `mcp__searxng-search__code_search` | 代码搜索 | engines: baidu kaifa |
| `mcp__searxng-search__academic_search` | 学术搜索 | categories: science |
| `mcp__searxng-search__image_search` | 图片搜索 | engines: bing images, baidu images |
| `mcp__searxng-search__wechat_search` | 微信文章 | engines: sogou wechat |

### 高级搜索语法

| 语法 | 说明 | 示例 |
|------|------|------|
| `"精确短语"` | 完全匹配 | `"React hooks"` |
| `-排除词` | 排除特定词 | `python -snake` |
| `site:example.com` | 站内搜索 | `tutorial site:react.dev` |
| `filetype:pdf` | 文件类型筛选 | `guide filetype:pdf` |

### 使用示例

```javascript
// 通用搜索
mcp__searxng-search__web_search({
  query: "React hooks 教程",
  language: "zh-CN",
  max_results: 5
})

// 代码搜索
mcp__searxng-search__code_search({
  query: "Python asyncio 并发编程",
  language: "python",
  max_results: 5
})
```

### 注意事项

- 引擎名称需包含空格，如 `"bing images"` 而非 `"bing_images"`
- 新闻、代码、学术搜索使用 `categories` 参数（单独指定引擎会超时）
- 中国可用的搜索引擎：`baidu, bing, sogou, 360search`

---

## 📖 Web Reader - 网页阅读技能

**位置**: [`.roo/skills/web-reader/`](.roo/skills/web-reader/SKILL.md)

读取网页内容并提取结构化信息：

### 工具列表

| 工具 | 用途 | 关键参数 |
|------|------|----------|
| `mcp__web-reader__read_url` | 读取单个 URL | `url`, `format`, `use_dynamic` |
| `mcp__web-reader__read_urls` | 批量读取 | `urls`, `format` |
| `mcp__web-reader__check_url` | 检查链接可用性 | `url` |

### 输出格式

| 格式 | 特点 | 适用场景 |
|------|------|----------|
| **Markdown** | LLM 友好，保留结构 | 文章阅读、文档提取 |
| **Text** | 纯文本 | 简单处理 |
| **JSON** | 结构化数据 | 程序化处理 |

### 使用示例

```javascript
// 基础用法 - 读取文章
mcp__web-reader__read_url({
  url: "https://example.com/article"
})

// 动态页面 - SPA 应用
mcp__web-reader__read_url({
  url: "https://spa.example.com",
  use_dynamic: true
})

// 批量读取
mcp__web-reader__read_urls({
  urls: ["url1", "url2", "url3"],
  format: "markdown"
})
```

### 注意事项

- 静态页面使用 Trafilatura 快速提取
- 动态页面需要 Playwright 渲染
- 默认超时 30 秒，可根据需要调整

---

## 🤖 Agent 工作流技能

**位置**: [`.roo/skills/agent-workflow/`](.roo/skills/agent-workflow/SKILL.md)

全面的 AI 代理工作流管理框架：

### 核心原则

```
① 保持简单   - 简单可组合模式 > 复杂框架
② 透明规划   - 明确展示每一步计划和进度
③ 精心设计   - 工具接口像 HCI 一样用心
④ 增量交付   - 每次完成一个可验证的小任务
⑤ 波浪并行   - 分析依赖，独立任务并行执行
⑥ 适时思考   - 复杂决策点停下来思考
```

### 执行模式

| 模式 | 适用场景 | 特点 |
|------|----------|------|
| **完整模式** | 复杂项目、长时任务 | 五阶段完整流程 |
| **快速模式** | 小任务、单一功能 | 简化流程，快速交付 |
| **波浪模式** | 多任务并行 | 依赖分析，分组并行 |

### 工作流程五阶段

1. **模式匹配** - 选择工作流模式和 Roo 模式
2. **初始化** - 创建状态文件，建立执行环境
3. **增量执行** - 每次专注于一个功能
4. **状态持久化** - 更新状态文件，Git 提交记录
5. **验证闭环** - 确保真正完成

### 使用示例

```javascript
// 委派子任务
new_task({
  mode: "code",
  message: `## 任务：开发注册页面`,
  todos: `
  - [ ] 创建表单组件
  - [ ] 添加字段验证
  - [ ] 集成 API 调用
  `
})
```

---

## 📋 GSD 工作流技能

**位置**: [`.roo/skills/gsd-workflow/`](.roo/skills/gsd-workflow/SKILL.md)

GSD (Get Shit Done) 规范驱动开发框架，解决 Context Rot 问题：

### 核心解决的问题

**Context Rot（上下文腐烂）**：传统 AI 编程中，随着对话进行，上下文窗口被填满，输出质量逐渐下降。GSD 通过每个任务独立上下文（200K tokens）保持质量始终稳定。

### 命令列表

| 命令 | 核心输出 |
|------|----------|
| `/gsd:init` | PROJECT.md, REQUIREMENTS.md, ROADMAP.md |
| `/gsd:discuss N` | 阶段偏好、技术选型决策 |
| `/gsd:plan N` | PLAN.md（原子任务计划） |
| `/gsd:execute N` | 原子提交、功能实现 |
| `/gsd:verify N` | 验证报告、状态更新 |
| `/gsd:quick` | 简化流程处理小任务 |

### 核心文档

- **PROJECT.md** - 项目愿景
- **REQUIREMENTS.md** - 需求清单
- **ROADMAP.md** - 阶段规划
- **PLAN.md** - 原子任务计划
- **STATE.md** - 状态追踪

### 适用场景

- ✅ 目标明确的项目开发
- ✅ 需要交付生产级代码
- ✅ 跨多个会话的复杂任务
- ✅ 需要 Git 历史清晰可追溯
- ✅ 团队协作项目

---

## 🎯 Task Master - 任务管理专家技能

**位置**: [`.roo/skills/task-master/`](.roo/skills/task-master/SKILL.md)

全流程任务管理专家，整合多种专业方法论：

### 方法论速查

| 方法 | 核心价值 | 应用阶段 |
|------|----------|----------|
| **WBS** | 层层分解，化繁为简 | 拆解 |
| **MECE** | 不重不漏，全面覆盖 | 拆解 |
| **SMART** | 目标清晰可衡量 | 规划 |
| **诺伊曼思维** | 原子拆解序列执行 | 规划 |
| **验证清单** | 质量把关 | 验证 |
| **金字塔原理** | 结论先行 | 汇报 |
| **SCQA** | 故事框架 | 汇报 |

### 工作流程四阶段

1. **任务拆解** - WBS 工作分解 + MECE 原则 + RACI 责任分配
2. **规划执行** - SMART 目标设定 + 诺伊曼思维拆解
3. **验证闭环** - 验证清单 + PDCA 循环
4. **汇报表达** - 金字塔原理 + SCQA 框架

### 使用示例

```javascript
// 更新 TODO 列表
update_todo_list({
  todos: `
  - [-] 任务拆解
  - [ ] 工作包 1.1.1: 注册页面开发
  - [ ] 工作包 1.1.2: 注册 API 开发
  - [ ] 验证改进
  - [ ] 汇报表达
  `
})
```

---

## 💭 Think Tool - 智能技能调度器

**位置**: [`.roo/skills/think-tool/`](.roo/skills/think-tool/SKILL.md)

智能技能调度器与思考工具双重功能：

### 双重模式

| 模式 | 触发场景 | 核心功能 |
|------|----------|----------|
| **思考模式** | 多工具调用、复杂决策 | 结构化思考、方案权衡 |
| **调度模式** | 技能关键词匹配、调度请求 | 技能发现、匹配、协调执行 |

### 调度器架构

```
用户输入 "/think-tool + 任务描述"
    ↓
步骤 1：任务解析 → 提取关键词、识别任务类型
    ↓
步骤 2：技能发现 → 查看 available_skills 列表
    ↓
步骤 3：技能匹配 → 计算匹配度分数
    ↓
步骤 4：技能调度 → 调用匹配技能
    ↓
步骤 5：结果返回 → 整合执行结果
```

### 使用示例

```
用户输入："/think-tool 搜索人工智能最新进展"

调度器分析：
1. 提取关键词：搜索、人工智能、最新进展
2. 匹配技能：web-search
3. 调度执行：调用 web-search 技能进行搜索
4. 返回结果：提供搜索结果摘要
```

---

## 技能协作关系

```
┌─────────────────────────────────────────────────────────────┐
│                    用户请求                                  │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
            ┌─────────────────┐
            │   think-tool    │ ← 智能调度器
            │  (模式选择/调度) │
            └────────┬────────┘
                     │
        ┌────────────┼────────────┐
        │            │            │
        ▼            ▼            ▼
┌──────────────┐ ┌──────────────┐ ┌──────────────┐
│ task-master  │ │agent-workflow│ │  gsd-workflow│
│ (任务规划)    │ │ (执行跟踪)    │ │ (规范开发)    │
└───────┬──────┘ └───────┬──────┘ └───────┬──────┘
        │                │                │
        └────────────────┼────────────────┘
                         │
                         ▼
            ┌─────────────────────────────┐
            │     web-search + web-reader │
            │      (搜索 + 阅读闭环)        │
            └─────────────────────────────┘
```

### 典型协作流程

1. **think-tool** 接收用户请求，分析任务类型
2. **task-master** 进行任务拆解和规划（复杂项目）
3. **agent-workflow** 或 **gsd-workflow** 负责执行跟踪
4. **web-search** 和 **web-reader** 提供信息获取能力

---

## 🔗 相关文档

- [返回 README.md](../README.md) - 项目主文档
- [CONTRIBUTING.md](../CONTRIBUTING.md) - 贡献指南
- [.roo/skills/](.roo/skills/) - 技能源代码目录

---
> **注意**：所有技能都预装在项目中，开箱即用。如需自定义或扩展技能，请参考技能目录中的 SKILL.md 文件。