# AI Agent 工具集 - 搜索与阅读

![GitHub](https://img.shields.io/badge/GitHub-模板仓库-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![Roo Code](https://img.shields.io/badge/Roo_Code-已启用-orange)

> **AI Agent 的眼睛**：搜索 + 阅读，让 AI Agent 能够看世界。

---

## 📑 目录

- [AI Agent 工具集 - 搜索与阅读](#ai-agent-工具集---搜索与阅读)
  - [📑 目录](#-目录)
  - [🎯 项目概述](#-项目概述)
    - [核心定位](#核心定位)
    - [技术栈](#技术栈)
    - [协作闭环](#协作闭环)
  - [🚀 核心功能](#-核心功能)
    - [🌐 Web Search - 网络搜索](#-web-search---网络搜索)
    - [📖 Web Reader - 网页阅读](#-web-reader---网页阅读)
    - [🔧 预装技能](#-预装技能)
  - [🏗️ 技术架构](#️-技术架构)
  - [🏁 快速开始](#-快速开始)
    - [前置依赖](#前置依赖)
      - [Python 虚拟环境设置（推荐）](#python-虚拟环境设置推荐)
    - [启动服务](#启动服务)
    - [服务验证](#服务验证)
    - [MCP 客户端配置](#mcp-客户端配置)
    - [⚠️ 常见问题](#️-常见问题)
  - [🧩 技能系统](#-技能系统)
    - [技能概览](#技能概览)
    - [🌐 Web Search - 网络搜索技能](#-web-search---网络搜索技能)
      - [工具列表](#工具列表)
      - [高级搜索语法](#高级搜索语法)
      - [使用示例](#使用示例)
      - [注意事项](#注意事项)
    - [📖 Web Reader - 网页阅读技能](#-web-reader---网页阅读技能)
      - [工具列表](#工具列表-1)
      - [输出格式](#输出格式)
      - [使用示例](#使用示例-1)
      - [注意事项](#注意事项-1)
    - [🤖 Agent 工作流技能](#-agent-工作流技能)
      - [核心原则](#核心原则)
      - [执行模式](#执行模式)
      - [工作流程五阶段](#工作流程五阶段)
      - [使用示例](#使用示例-2)
    - [📋 GSD 工作流技能](#-gsd-工作流技能)
      - [核心解决的问题](#核心解决的问题)
      - [命令列表](#命令列表)
      - [核心文档](#核心文档)
      - [适用场景](#适用场景)
    - [🎯 Task Master - 任务管理专家技能](#-task-master---任务管理专家技能)
      - [方法论速查](#方法论速查)
      - [工作流程四阶段](#工作流程四阶段)
      - [使用示例](#使用示例-3)
    - [💭 Think Tool - 智能技能调度器](#-think-tool---智能技能调度器)
      - [双重模式](#双重模式)
      - [调度器架构](#调度器架构)
      - [使用示例](#使用示例-4)
    - [技能协作关系](#技能协作关系)
      - [典型协作流程](#典型协作流程)
  - [🔍 MCP 服务器详解](#-mcp-服务器详解)
    - [SearXNG Search - 搜索服务](#searxng-search---搜索服务)
      - [搜索语法](#搜索语法)
    - [Web Reader - 阅读服务](#web-reader---阅读服务)
      - [特性](#特性)
  - [📄 使用示例](#-使用示例)
    - [完整工作流](#完整工作流)
    - [动态页面处理](#动态页面处理)
  - [� 版本信息](#-版本信息)
    - [版本号](#版本号)
    - [更新日志](#更新日志)
      - [\[v1.0.0\] - 2026-03-14](#v100---2026-03-14)
    - [兼容性](#兼容性)
      - [系统要求](#系统要求)
      - [MCP 客户端兼容性](#mcp-客户端兼容性)
      - [Python 依赖](#python-依赖)
      - [浏览器要求](#浏览器要求)
  - [🤝 贡献指南](#-贡献指南)
    - [开发环境设置](#开发环境设置)
      - [1. 克隆项目](#1-克隆项目)
      - [2. 安装依赖](#2-安装依赖)
      - [3. 启动开发服务](#3-启动开发服务)
      - [4. 运行测试](#4-运行测试)
    - [代码规范](#代码规范)
      - [Python 代码规范](#python-代码规范)
      - [代码风格要求](#代码风格要求)
      - [文档字符串规范](#文档字符串规范)
    - [提交规范](#提交规范)
      - [提交类型](#提交类型)
      - [提交格式](#提交格式)
      - [提交示例](#提交示例)
    - [测试要求](#测试要求)
      - [单元测试](#单元测试)
      - [集成测试](#集成测试)
      - [运行测试](#运行测试)
    - [问题反馈](#问题反馈)
      - [报告 Bug](#报告-bug)
      - [功能请求](#功能请求)
      - [联系方式](#联系方式)
  - [🐛 故障排除](#-故障排除)
    - [MCP 连接问题](#mcp-连接问题)
    - [SearXNG 问题](#searxng-问题)
    - [Web Reader 问题](#web-reader-问题)
    - [端口冲突](#端口冲突)
    - [网络问题](#网络问题)
  - [📁 项目结构](#-项目结构)
  - [📄 许可证](#-许可证)
  - [🙏 致谢](#-致谢)

---

## 🎯 项目概述

这是一个为 AI Agent 开发的预配置工作区模板，提供完整的网络信息获取能力。通过 **搜索（web-search）** + **阅读（web-reader）** 的协作闭环，让 AI Agent 能够自主获取互联网信息。

### 核心定位

- **"AI Agent 的眼睛"**：赋予 AI Agent 主动搜索和阅读网页的能力
- **隐私保护**：本地部署，不依赖第三方 API，完全控制数据流
- **开箱即用**：预配置 Roo Code 技能系统，快速集成到 AI 工作流

### 技术栈

| 组件 | 技术 | 说明 |
|------|------|------|
| **搜索引擎** | SearXNG | 隐私保护的元搜索引擎 |
| **内容提取** | Trafilatura | 高质量网页正文提取 |
| **动态渲染** | Playwright | 支持 JavaScript 动态页面 |
| **协议标准** | MCP (Model Context Protocol) | 标准化的 AI 工具接口 |
| **容器化** | Docker + Docker Compose | 一键部署，环境隔离 |
| **AI 集成** | Roo Code 技能系统 | 预配置工作流和任务管理 |

### 协作闭环

```
用户问题 → web-search → URL 列表 + 摘要
                              ↓
                        Agent 选择相关链接
                              ↓
                        web-reader → 完整内容
                              ↓
                        Agent 综合回答用户
```

---

## 🚀 核心功能

### 🌐 Web Search - 网络搜索

- **元搜索引擎**：聚合 Bing、Baidu、Google 等多个引擎结果
- **多类型支持**：新闻、图片、代码、学术、微信公众号文章
- **隐私保护**：本地部署，不追踪用户行为
- **完全免费**：无需 API Key，无调用限制

### 📖 Web Reader - 网页阅读

- **高质量提取**：基于 Trafilatura 精准识别正文内容
- **动态页面支持**：Playwright 渲染 JavaScript 应用
- **多格式输出**：Markdown、Text、JSON 灵活选择
- **批量处理**：一次性读取多个 URL

### 🔧 预装技能

- **web-search**：网络搜索技能
- **web-reader**：网页阅读技能
- **agent-workflow**：Agent 工作流管理与执行跟踪
- **task-master**：专业任务规划与进度跟踪

---

## 🏗️ 技术架构

```
┌─────────────────────────────────────────────────────────────┐
│                      AI Agent (Roo Code)                     │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────┐  │
│  │ task-master     │  │ agent-workflow  │  │ 其他技能... │  │
│  └────────┬────────┘  └────────┬────────┘  └─────────────┘  │
│           │                    │                             │
│           └──────────┬─────────┘                             │
│                      │                                        │
│         ┌────────────┴────────────┐                          │
│         │    MCP Client (.roo/)   │                          │
│         └────────────┬────────────┘                          │
└──────────────────────│───────────────────────────────────────┘
                       │ MCP Protocol
         ┌─────────────┴─────────────┐
         │                           │
         ▼                           ▼
┌─────────────────┐         ┌─────────────────┐
│  SearXNG MCP    │         │  Web Reader MCP │
│  (搜索服务)      │         │  (阅读服务)      │
└────────┬────────┘         └────────┬────────┘
         │                           │
         ▼                           ▼
┌─────────────────┐         ┌─────────────────┐
│   SearXNG       │         │   Playwright    │
│   搜索引擎       │         │   + Trafila     │
│   (端口 8080)   │         │   内容提取       │
└─────────────────┘         └─────────────────┘
```

---

## 🏁 快速开始

### 前置依赖

确保系统已安装以下工具：

```bash
# 检查 Docker
docker --version
docker-compose --version

# 检查 Python (3.10+)
python3 --version
```

#### Python 虚拟环境设置（推荐）

```bash
# 创建虚拟环境
python3 -m venv .venv

# 激活虚拟环境
# Linux/macOS
source .venv/bin/activate
# Windows
# .venv\Scripts\activate

# 安装 MCP 客户端和依赖
pip install mcp trafilatura playwright

# 安装浏览器（动态页面渲染必需）
playwright install chromium
```

### 启动服务

```bash
# 方式一：启动所有服务（推荐）
docker-compose up -d

# 方式二：仅启动 SearXNG 搜索服务
cd searxng && docker-compose up -d
```

### 服务验证

```bash
# 验证 SearXNG 服务
curl http://localhost:8080/search?q=test&format=json

# 检查容器运行状态
docker ps | grep searxng

# 访问 SearXNG Web 界面
# 浏览器打开：http://localhost:8080
```

### MCP 客户端配置

在 Roo Code 的 `.roo/mcp.json` 中配置：

```json
{
  "mcpServers": {
    "searxng-search": {
      "command": "python",
      "args": ["mcp/searxng_mcp/mcp_server.py"],
      "env": {
        "SEARXNG_BASE_URL": "http://localhost:8080"
      }
    },
    "web-reader": {
      "command": "python",
      "args": ["mcp/web_reader_mcp/mcp_server.py"]
    }
  }
}
```

### ⚠️ 常见问题

| 问题 | 解决方案 |
|------|----------|
| **端口 8080 冲突** | `sudo lsof -i :8080` 查看占用进程，或修改 `docker-compose.yml` 端口映射 |
| **Docker 网络问题** | 确保 Docker 可以访问外网，检查 DNS 设置 |
| **MCP 连接失败** | 确认 Python 虚拟环境已激活，依赖已安装 |
| **Playwright 浏览器安装失败** | 使用国内镜像：`PLAYWRIGHT_DOWNLOAD_HOST=https://npmmirror.com/mirrors/playwright playwright install chromium` |

---

## 🧩 技能系统

### 技能概览

| 技能名称 | 位置 | 核心功能 | 适用场景 |
|----------|------|----------|----------|
| **web-search** | `.roo/skills/web-search/` | 网络搜索、结果聚合 | 需要实时信息、查找文档、搜索代码 |
| **web-reader** | `.roo/skills/web-reader/` | 网页内容提取、元数据获取 | 读取文章、提取正文、批量处理 URL |
| **agent-workflow** | `.roo/skills/agent-workflow/` | 全流程闭环执行框架 | 长时任务、多步骤项目、跨会话跟踪 |
| **gsd-workflow** | `.roo/skills/gsd-workflow/` | 规范驱动开发框架 | 生产级项目开发、解决 Context Rot 问题 |
| **task-master** | `.roo/skills/task-master/` | 全流程任务管理专家 | 复杂项目管理、任务规划、进度跟踪 |
| **think-tool** | `.roo/skills/think-tool/` | 智能技能调度器与思考工具 | 复杂决策、多技能协调、结构化思考 |

---

### 🌐 Web Search - 网络搜索技能

**位置**: [`.roo/skills/web-search/`](.roo/skills/web-search/SKILL.md)

通过 SearXNG 提供网络搜索能力：

#### 工具列表

| 工具 | 用途 | 搜索方式 |
|------|------|----------|
| `mcp__searxng-search__web_search` | 通用搜索 | engines: bing, baidu, 360search, sogou |
| `mcp__searxng-search__web_search` | 新闻搜索 | query + "新闻", time_range: day |
| `mcp__searxng-search__code_search` | 代码搜索 | engines: baidu kaifa |
| `mcp__searxng-search__academic_search` | 学术搜索 | categories: science |
| `mcp__searxng-search__image_search` | 图片搜索 | engines: bing images, baidu images |
| `mcp__searxng-search__wechat_search` | 微信文章 | engines: sogou wechat |

#### 高级搜索语法

| 语法 | 说明 | 示例 |
|------|------|------|
| `"精确短语"` | 完全匹配 | `"React hooks"` |
| `-排除词` | 排除特定词 | `python -snake` |
| `site:example.com` | 站内搜索 | `tutorial site:react.dev` |
| `filetype:pdf` | 文件类型筛选 | `guide filetype:pdf` |

#### 使用示例

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

#### 注意事项

- 引擎名称需包含空格，如 `"bing images"` 而非 `"bing_images"`
- 新闻、代码、学术搜索使用 `categories` 参数（单独指定引擎会超时）
- 中国可用的搜索引擎：`baidu, bing, sogou, 360search`

---

### 📖 Web Reader - 网页阅读技能

**位置**: [`.roo/skills/web-reader/`](.roo/skills/web-reader/SKILL.md)

读取网页内容并提取结构化信息：

#### 工具列表

| 工具 | 用途 | 关键参数 |
|------|------|----------|
| `mcp__web-reader__read_url` | 读取单个 URL | `url`, `format`, `use_dynamic` |
| `mcp__web-reader__read_urls` | 批量读取 | `urls`, `format` |
| `mcp__web-reader__check_url` | 检查链接可用性 | `url` |

#### 输出格式

| 格式 | 特点 | 适用场景 |
|------|------|----------|
| **Markdown** | LLM 友好，保留结构 | 文章阅读、文档提取 |
| **Text** | 纯文本 | 简单处理 |
| **JSON** | 结构化数据 | 程序化处理 |

#### 使用示例

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

#### 注意事项

- 静态页面使用 Trafilatura 快速提取
- 动态页面需要 Playwright 渲染
- 默认超时 30 秒，可根据需要调整

---

### 🤖 Agent 工作流技能

**位置**: [`.roo/skills/agent-workflow/`](.roo/skills/agent-workflow/SKILL.md)

全面的 AI 代理工作流管理框架：

#### 核心原则

```
① 保持简单   - 简单可组合模式 > 复杂框架
② 透明规划   - 明确展示每一步计划和进度
③ 精心设计   - 工具接口像 HCI 一样用心
④ 增量交付   - 每次完成一个可验证的小任务
⑤ 波浪并行   - 分析依赖，独立任务并行执行
⑥ 适时思考   - 复杂决策点停下来思考
```

#### 执行模式

| 模式 | 适用场景 | 特点 |
|------|----------|------|
| **完整模式** | 复杂项目、长时任务 | 五阶段完整流程 |
| **快速模式** | 小任务、单一功能 | 简化流程，快速交付 |
| **波浪模式** | 多任务并行 | 依赖分析，分组并行 |

#### 工作流程五阶段

1. **模式匹配** - 选择工作流模式和 Roo 模式
2. **初始化** - 创建状态文件，建立执行环境
3. **增量执行** - 每次专注于一个功能
4. **状态持久化** - 更新状态文件，Git 提交记录
5. **验证闭环** - 确保真正完成

#### 使用示例

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

### 📋 GSD 工作流技能

**位置**: [`.roo/skills/gsd-workflow/`](.roo/skills/gsd-workflow/SKILL.md)

GSD (Get Shit Done) 规范驱动开发框架，解决 Context Rot 问题：

#### 核心解决的问题

**Context Rot（上下文腐烂）**：传统 AI 编程中，随着对话进行，上下文窗口被填满，输出质量逐渐下降。GSD 通过每个任务独立上下文（200K tokens）保持质量始终稳定。

#### 命令列表

| 命令 | 核心输出 |
|------|----------|
| `/gsd:init` | PROJECT.md, REQUIREMENTS.md, ROADMAP.md |
| `/gsd:discuss N` | 阶段偏好、技术选型决策 |
| `/gsd:plan N` | PLAN.md（原子任务计划） |
| `/gsd:execute N` | 原子提交、功能实现 |
| `/gsd:verify N` | 验证报告、状态更新 |
| `/gsd:quick` | 简化流程处理小任务 |

#### 核心文档

- **PROJECT.md** - 项目愿景
- **REQUIREMENTS.md** - 需求清单
- **ROADMAP.md** - 阶段规划
- **PLAN.md** - 原子任务计划
- **STATE.md** - 状态追踪

#### 适用场景

- ✅ 目标明确的项目开发
- ✅ 需要交付生产级代码
- ✅ 跨多个会话的复杂任务
- ✅ 需要 Git 历史清晰可追溯
- ✅ 团队协作项目

---

### 🎯 Task Master - 任务管理专家技能

**位置**: [`.roo/skills/task-master/`](.roo/skills/task-master/SKILL.md)

全流程任务管理专家，整合多种专业方法论：

#### 方法论速查

| 方法 | 核心价值 | 应用阶段 |
|------|----------|----------|
| **WBS** | 层层分解，化繁为简 | 拆解 |
| **MECE** | 不重不漏，全面覆盖 | 拆解 |
| **SMART** | 目标清晰可衡量 | 规划 |
| **诺伊曼思维** | 原子拆解序列执行 | 规划 |
| **验证清单** | 质量把关 | 验证 |
| **金字塔原理** | 结论先行 | 汇报 |
| **SCQA** | 故事框架 | 汇报 |

#### 工作流程四阶段

1. **任务拆解** - WBS 工作分解 + MECE 原则 + RACI 责任分配
2. **规划执行** - SMART 目标设定 + 诺伊曼思维拆解
3. **验证闭环** - 验证清单 + PDCA 循环
4. **汇报表达** - 金字塔原理 + SCQA 框架

#### 使用示例

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

### 💭 Think Tool - 智能技能调度器

**位置**: [`.roo/skills/think-tool/`](.roo/skills/think-tool/SKILL.md)

智能技能调度器与思考工具双重功能：

#### 双重模式

| 模式 | 触发场景 | 核心功能 |
|------|----------|----------|
| **思考模式** | 多工具调用、复杂决策 | 结构化思考、方案权衡 |
| **调度模式** | 技能关键词匹配、调度请求 | 技能发现、匹配、协调执行 |

#### 调度器架构

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

#### 使用示例

```
用户输入："/think-tool 搜索人工智能最新进展"

调度器分析：
1. 提取关键词：搜索、人工智能、最新进展
2. 匹配技能：web-search
3. 调度执行：调用 web-search 技能进行搜索
4. 返回结果：提供搜索结果摘要
```

---

### 技能协作关系

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

#### 典型协作流程

1. **think-tool** 接收用户请求，分析任务类型
2. **task-master** 进行任务拆解和规划（复杂项目）
3. **agent-workflow** 或 **gsd-workflow** 负责执行跟踪
4. **web-search** 和 **web-reader** 提供信息获取能力

---

## 🔍 MCP 服务器详解

### SearXNG Search - 搜索服务

| 工具 | 描述 | 搜索方式 |
|------|------|----------|
| `web_search` | 通用网络搜索 | engines: bing, baidu, 360search, sogou |
| `news_search` | 新闻搜索 | categories: news |
| `image_search` | 图片搜索 | engines: bing images, baidu images, sogou images, quark images |
| `code_search` | 代码搜索 | categories: it |
| `academic_search` | 学术搜索 | categories: science |
| `wechat_search` | 微信文章搜索 | engines: sogou wechat |

#### 搜索语法

| 语法 | 说明 | 示例 |
|------|------|------|
| `"精确短语"` | 完全匹配 | `"React hooks"` |
| `-排除词` | 排除特定词 | `python -snake` |
| `site:example.com` | 站内搜索 | `tutorial site:react.dev` |
| `filetype:pdf` | 文件类型筛选 | `guide filetype:pdf` |

**重要说明**：
- 引擎名称需包含空格，如 `"bing images"` 而非 `"bing_images"`
- 新闻、代码、学术搜索使用 `categories` 参数（单独指定引擎会超时）

### Web Reader - 阅读服务

| 工具 | 描述 | 用途 |
|------|------|------|
| `read_url` | 读取单个 URL | 获取页面内容 |
| `read_urls` | 批量读取 | 同时处理多个 URL |
| `check_url` | 检查链接 | 验证 URL 可用性 |

#### 特性

- **静态页面**：快速提取（Trafilatura）
- **动态页面**：渲染后提取（Playwright）
- **元数据提取**：标题、作者、日期
- **链接提取**：获取页面相关链接

---

## 📄 使用示例

### 完整工作流

```python
# 1. 搜索相关信息
mcp__searxng-search__web_search({
  query: "React hooks 教程",
  max_results: 5
})
# → 返回 5 个相关 URL + 摘要

# 2. 根据摘要选择最相关的 URL

# 3. 阅读完整内容
mcp__web-reader__read_url({
  url: "https://react.dev/learn/hooks"
})
# → 返回完整文章内容

# 或批量读取多个链接
mcp__web-reader__read_urls({
  urls: ["url1", "url2", "url3"]
})
```

### 动态页面处理

对于单页应用（SPA）等动态页面：

```python
mcp__web-reader__read_url({
  url: "https://spa-app.example.com",
  use_dynamic: true,
  wait_selector: ".content-loaded"  # 等待特定元素加载完成
})
```

---

## 📋 版本信息

### 版本号

| 组件 | 当前版本 | 发布日期 |
|------|----------|----------|
| **AI Agent 工具集** | v1.0.0 | 2026-03-14 |
| **web-search 技能** | v1.0.0 | 2026-03-14 |
| **web-reader 技能** | v1.0.0 | 2026-03-14 |
| **agent-workflow 技能** | v1.0.0 | 2026-03-14 |
| **gsd-workflow 技能** | v1.0.0 | 2026-03-14 |
| **task-master 技能** | v1.0.0 | 2026-03-14 |
| **think-tool 技能** | v1.0.0 | 2026-03-14 |

---

### 更新日志

#### [v1.0.0] - 2026-03-14

**新增**
- ✨ 初始版本发布
- ✨ 预装 6 个核心技能（web-search, web-reader, agent-workflow, gsd-workflow, task-master, think-tool）
- ✨ 完整的 MCP 服务器实现（SearXNG Search, Web Reader）
- ✨ Docker Compose 一键部署配置
- ✨ 详细的 README 文档，包含技能系统说明、版本信息、贡献指南

**功能**
- 🌐 网络搜索支持多种类型（通用、新闻、图片、代码、学术、微信文章）
- 📖 网页阅读支持静态和动态页面，多种输出格式
- 🤖 Agent 工作流支持完整模式、快速模式、波浪模式
- 📋 GSD 工作流解决 Context Rot 问题
- 🎯 Task Master 整合 WBS+MECE+SMART 等专业方法论
- 💭 Think Tool 智能技能调度与结构化思考

**文档**
- 📝 完整的技能系统文档，包含技能概览表格和详细说明
- 📝 版本信息和更新日志章节
- 📝 贡献指南，包含开发环境设置、代码规范、提交规范
- 📝 故障排除指南

---

### 兼容性

#### 系统要求

| 组件 | 最低版本 | 推荐版本 |
|------|----------|----------|
| **Docker** | 20.10+ | 24.0+ |
| **Docker Compose** | 1.29+ | 2.20+ |
| **Python** | 3.10 | 3.11+ |
| **Node.js** (Roo Code) | 18.0+ | 20.0+ |

#### MCP 客户端兼容性

| 客户端 | 状态 | 最低版本 |
|--------|------|----------|
| **Roo Code** | ✅ 已验证 | 1.0.0+ |
| **Claude Desktop** | ✅ 兼容 | 0.1.0+ |
| **其他 MCP 客户端** | ⚠️ 未验证 | - |

#### Python 依赖

```python
# MCP 协议
mcp>=1.0.0

# 网页内容提取
trafilatura>=1.6.0

# 浏览器自动化
playwright>=1.40.0

# HTTP 请求
httpx>=0.25.0

# JSON 处理
pydantic>=2.0.0
```

#### 浏览器要求

对于动态页面渲染（Playwright）：

```bash
# 安装 Chromium 浏览器
playwright install chromium

# 或使用国内镜像加速
PLAYWRIGHT_DOWNLOAD_HOST=https://npmmirror.com/mirrors/playwright playwright install chromium
```

---

## 🤝 贡献指南

欢迎参与项目贡献！本指南帮助你快速上手项目开发。

### 开发环境设置

#### 1. 克隆项目

```bash
git clone https://github.com/your-username/ai-agent-toolkit.git
cd ai-agent-toolkit
```

#### 2. 安装依赖

```bash
# 创建 Python 虚拟环境
python3 -m venv .venv

# 激活虚拟环境
# Linux/macOS
source .venv/bin/activate
# Windows
# .venv\Scripts\activate

# 安装开发依赖
pip install -e ./mcp/searxng_mcp
pip install -e ./mcp/web_reader_mcp

# 安装开发工具
pip install pytest pytest-cov black flake8 mypy
```

#### 3. 启动开发服务

```bash
# 启动 Docker 服务
docker-compose up -d

# 验证服务运行
curl http://localhost:8080/search?q=test&format=json
```

#### 4. 运行测试

```bash
# 运行所有测试
pytest

# 运行测试并生成覆盖率报告
pytest --cov=mcp --cov-report=html
```

---

### 代码规范

#### Python 代码规范

本项目遵循以下 Python 代码规范：

- **PEP 8** - Python 官方风格指南
- **Black** - 代码格式化
- **Flake8** - 代码检查
- **MyPy** - 类型检查

```bash
# 格式化代码
black mcp/

# 检查代码
flake8 mcp/

# 类型检查
mypy mcp/
```

#### 代码风格要求

```python
# ✅ 推荐：使用类型注解
def read_url(url: str, use_dynamic: bool = False) -> dict:
    """读取 URL 内容。
    
    Args:
        url: 要读取的 URL 地址
        use_dynamic: 是否使用动态渲染
        
    Returns:
        包含页面内容的字典
    """
    pass

# ✅ 推荐：使用有意义的变量名
def process_search_results(results: list[dict]) -> list[SearchResult]:
    return [SearchResult(**r) for r in results if r.get('url')]

# ❌ 避免：模糊的变量名
def proc(r):
    return [x for x in r if x.get('u')]
```

#### 文档字符串规范

```python
def web_search(
    query: str,
    engines: str | None = None,
    categories: str | None = None,
    language: str = "zh-CN",
    time_range: str | None = None,
    max_results: int = 10
) -> list[SearchResult]:
    """执行网络搜索。
    
    Args:
        query: 搜索关键词，支持高级搜索语法
        engines: 搜索引擎列表，如 "bing,baidu,sogou"
        categories: 搜索类别，如 "general", "images", "news"
        language: 结果语言代码，默认 "zh-CN"
        time_range: 时间范围，可选 "day", "week", "month", "year"
        max_results: 返回结果数量，默认 10
        
    Returns:
        搜索结果列表，每个结果包含标题、URL、摘要、来源
        
    Raises:
        SearchError: 当搜索失败或无结果时
        
    Example:
        >>> results = web_search("React hooks 教程", max_results=5)
        >>> for r in results:
        ...     print(f"{r.title}: {r.url}")
    """
```

---

### 提交规范

本项目采用 [Conventional Commits](https://www.conventionalcommits.org/) 规范：

#### 提交类型

| 类型 | 说明 | 示例 |
|------|------|------|
| `feat` | 新功能 | `feat(web-search): 添加学术搜索功能` |
| `fix` | Bug 修复 | `fix(web-reader): 修复动态页面超时问题` |
| `docs` | 文档更新 | `docs: 更新技能系统说明` |
| `style` | 代码格式 | `style: 使用 Black 格式化代码` |
| `refactor` | 代码重构 | `refactor: 优化搜索结果处理逻辑` |
| `test` | 测试相关 | `test: 添加 web-search 单元测试` |
| `chore` | 构建/工具 | `chore: 更新依赖版本` |

#### 提交格式

```
<type>(<scope>): <subject>

<body>

<footer>
```

#### 提交示例

```bash
# 新功能
git commit -m "feat(web-search): 添加微信公众号文章搜索

- 集成 sogou wechat 引擎
- 支持微信文章高级搜索语法
- 添加相关测试用例

Closes #42"

# Bug 修复
git commit -m "fix(web-reader): 修复 JavaScript 渲染超时问题

- 增加 wait_selector 参数支持
- 优化超时重试逻辑
- 添加超时错误处理

Fixes #38"

# 文档更新
git commit -m "docs: 更新技能系统文档

- 添加技能概览表格
- 补充每个技能的详细说明
- 添加技能协作关系图"
```

---

### 测试要求

#### 单元测试

所有新功能必须包含单元测试：

```python
# tests/test_web_search.py
import pytest
from mcp.searxng_mcp import web_search

class TestWebSearch:
    """Web Search 功能测试"""
    
    def test_basic_search(self):
        """测试基础搜索功能"""
        results = web_search(query="Python 教程", max_results=5)
        assert len(results) <= 5
        assert all(isinstance(r, dict) for r in results)
    
    def test_search_with_engine(self):
        """测试指定搜索引擎"""
        results = web_search(
            query="React hooks",
            engines="bing,baidu",
            max_results=3
        )
        assert len(results) <= 3
    
    def test_empty_query_error(self):
        """测试空查询错误处理"""
        with pytest.raises(ValueError):
            web_search(query="")
```

#### 集成测试

关键功能需要集成测试：

```python
# tests/test_integration.py
class TestSearchReadFlow:
    """搜索 - 阅读集成测试"""
    
    def test_search_then_read(self):
        """测试搜索后阅读的完整流程"""
        # 1. 搜索
        search_results = web_search(query="Python 官方文档", max_results=3)
        assert len(search_results) > 0
        
        # 2. 阅读第一个结果
        if search_results:
            content = read_url(url=search_results[0]['url'])
            assert 'content' in content
            assert len(content['content']) > 0
```

#### 运行测试

```bash
# 运行所有测试
pytest

# 运行特定测试文件
pytest tests/test_web_search.py

# 运行测试并显示覆盖率
pytest --cov=mcp --cov-report=term-missing

# 运行测试并生成 HTML 报告
pytest --cov=mcp --cov-report=html
open htmlcov/index.html
```

---

### 问题反馈

#### 报告 Bug

发现 Bug 时，请在 GitHub Issues 中创建 Issue，并提供以下信息：

```markdown
**问题描述**
简要描述问题现象

**复现步骤**
1. 执行步骤 1
2. 执行步骤 2
3. 观察到错误

**预期行为**
应该发生什么

**实际行为**
实际发生了什么

**环境信息**
- OS: macOS 14.0 / Ubuntu 22.04 / Windows 11
- Python: 3.11.5
- Docker: 24.0.6
- 相关版本号

**日志/截图**
如有错误日志或截图，请附上
```

#### 功能请求

欢迎提出新功能建议！请创建 Feature Request Issue，包含：

```markdown
**功能描述**
清晰描述想要的功能

**使用场景**
这个功能解决什么问题

**实现建议**
如有实现思路，可以提出建议

**替代方案**
是否考虑过其他实现方式
```

#### 联系方式

- 📧 Email: your-email@example.com
- 💬 GitHub Discussions: [项目讨论区](https://github.com/your-username/ai-agent-toolkit/discussions)
- 🐛 Bug 报告：[GitHub Issues](https://github.com/your-username/ai-agent-toolkit/issues)

---

## 🐛 故障排除

### MCP 连接问题

```bash
# 1. 确保已安装 Python 3.10+
python3 --version

# 2. 设置虚拟环境
python3 -m venv .venv
source .venv/bin/activate

# 3. 安装依赖
pip install mcp trafilatura playwright
playwright install chromium
```

### SearXNG 问题

```bash
# 检查服务状态
docker ps | grep searxng

# 检查端口
curl http://localhost:8080

# 重启服务
cd searxng && docker-compose restart

# 查看日志
docker-compose logs searxng
```

### Web Reader 问题

```bash
# 构建镜像
docker build -t web-reader-mcp ./mcp/web_reader_mcp

# 测试运行
docker run -i web-reader-mcp

# 查看日志
docker-compose logs web-reader
```

### 端口冲突

```bash
# 检查 8080 端口占用
sudo lsof -i :8080

# 修改 docker-compose.yml 中的端口映射
# 例如改为 8081:8080
```

### 网络问题

```bash
# 测试 Docker 网络
docker run --rm alpine ping -c 3 google.com

# 配置 Docker DNS
# 编辑 /etc/docker/daemon.json
# {"dns": ["8.8.8.8", "1.1.1.1"]}
```

---

## 📁 项目结构

```
.
├── .roo/                          # Roo Code 配置
│   ├── mcp.json                  # MCP 服务器配置
│   └── skills/                   # 预装技能
│       ├── agent-workflow/       # Agent 工作流管理技能
│       ├── gsd-workflow/         # GSD 规范驱动开发框架
│       ├── task-master/          # 任务规划与跟踪技能
│       ├── think-tool/           # 智能技能调度器与思考工具
│       ├── web-search/           # 网络搜索技能
│       └── web-reader/           # 网页阅读技能
├── mcp/                          # MCP 服务器
│   ├── searxng_mcp/             # SearXNG MCP 服务器（搜索）
│   │   ├── mcp_server.py
│   │   ├── pyproject.toml
│   │   └── README.md
│   └── web_reader_mcp/          # Web Reader MCP 服务器（阅读）
│       ├── mcp_server.py
│       ├── Dockerfile           # 自定义 Docker 镜像
│       ├── pyproject.toml
│       └── README.md
├── searxng/                      # SearXNG 搜索引擎部署
│   ├── docker-compose.yml
│   └── searxng/
│       └── settings.yml
├── docker-compose.yml            # 整合部署配置
└── README.md
```

---

## 📄 许可证

MIT License

---

## 🙏 致谢

- [Roo Code](https://roocode.com/) - AI assistant platform
- [SearXNG](https://searxng.github.io/searxng/) - Privacy-respecting metasearch engine
- [Trafilatura](https://github.com/adbar/trafilatura) - Web content extraction
- [Playwright](https://playwright.dev/) - Browser automation
- [MCP](https://spec.modelcontextprotocol.io/) - Model Context Protocol