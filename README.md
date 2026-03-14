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
    - [🌐 Web Search - 网络搜索技能](#-web-search---网络搜索技能)
    - [📖 Web Reader - 网页阅读技能](#-web-reader---网页阅读技能)
    - [🤖 Agent 工作流技能](#-agent-工作流技能)
    - [📋 任务管理专家技能](#-任务管理专家技能)
  - [🔍 MCP 服务器详解](#-mcp-服务器详解)
    - [SearXNG Search - 搜索服务](#searxng-search---搜索服务)
      - [搜索语法](#搜索语法)
    - [Web Reader - 阅读服务](#web-reader---阅读服务)
      - [特性](#特性)
  - [📄 使用示例](#-使用示例)
    - [完整工作流](#完整工作流)
    - [动态页面处理](#动态页面处理)
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

### 🌐 Web Search - 网络搜索技能

**位置**: `.roo/skills/web-search/`

通过 SearXNG 提供网络搜索能力：
- 通用搜索、新闻搜索、图片搜索
- 代码搜索、学术搜索
- 微信公众号文章搜索
- 高级搜索语法支持

### 📖 Web Reader - 网页阅读技能

**位置**: `.roo/skills/web-reader/`

读取网页内容并提取结构化信息：
- 高质量正文提取（Trafilatura）
- 动态页面渲染（Playwright）
- 多种输出格式（Markdown/Text/JSON）
- 批量 URL 处理

### 🤖 Agent 工作流技能

**位置**: `.roo/skills/agent-workflow/`

全面的 AI 代理工作流管理：
- 任务分解与执行跟踪
- 跨会话状态持久化
- 验证清单和进度报告

### 📋 任务管理专家技能

**位置**: `.roo/skills/task-master/`

采用专业方法论的高级任务管理：
- WBS（工作分解结构）+ MECE 任务分解
- SMART 目标设定与跟踪

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
│       ├── task-master/          # 任务规划与跟踪技能
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