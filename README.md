# AI Agent 工具集

[![Docker Compose](https://img.shields.io/badge/Docker%20Compose-3.8-blue)](https://docs.docker.com/compose/)
[![MCP](https://img.shields.io/badge/MCP-1.0-green)](https://modelcontextprotocol.io)
[![SearXNG](https://img.shields.io/badge/SearXNG-latest-orange)](https://searxng.org)

为 Roo Code AI 智能体提供完整的本地工具生态系统，包含搜索引擎、网页阅读器、向量数据库和自动化工作流技能。

## 🎯 项目愿景

**让 AI 智能体拥有自主获取信息、处理任务的能力**。本项目通过本地部署的 SearXNG 元搜索引擎和 MCP (Model Context Protocol) 服务器，为 AI 智能体提供：

- 🔍 **实时网络搜索** - 无需依赖外部 API，保护隐私
- 📖 **智能网页阅读** - 自动提取正文内容，支持动态页面
- 🧠 **向量存储** - 持久化记忆和语义搜索
- 🔧 **工作流技能** - 复杂任务拆解与执行框架

## 🏗️ 核心架构

```
├── docker-compose.yml          # 服务编排
├── searxng/                    # SearXNG 配置文件
├── mcp/                        # MCP 服务器
│   ├── searxng_mcp/            # 搜索 MCP 服务器
│   └── web_reader_mcp/         # 网页阅读 MCP 服务器
└── .roo/                       # Roo Code 配置
    ├── mcp.json                # MCP 服务器配置
    └── skills/                 # AI 智能体技能库
```

### 服务组件

| 服务 | 端口 | 用途 |
|------|------|------|
| **searxng** | 8080 | 元搜索引擎界面 |
| **searxng-mcp** | - | 搜索 MCP 服务器 |
| **web-reader-mcp** | - | 网页阅读 MCP 服务器 |
| **qdrant** | 6333 | 向量数据库 |
| **valkey** | 6379 | 缓存数据库 |

## 🚀 快速开始

### 前置要求
- Docker 24+ 和 Docker Compose
- 至少 4GB 可用内存
- Linux/macOS/WSL2 环境

### 一键启动
```bash
# 克隆仓库（如果尚未克隆）
git clone <repository-url>
cd ai_work

# 启动所有服务
docker-compose up -d

# 验证服务状态
docker-compose ps
```

### 配置 Roo Code
确保 Roo Code 配置正确加载 `.roo/mcp.json` 文件。该文件已预配置好两个 MCP 服务器：

- `searxng-search`: 提供 `web_search`, `news_search`, `image_search`, `academic_search`, `wechat_search` 等工具
- `web-reader`: 提供 `read_url`, `read_urls`, `check_url` 等工具

### 测试搜索功能
在 Roo Code 中尝试以下命令：
```javascript
// 通用搜索
mcp__searxng-search__web_search({
  query: "人工智能最新进展",
  language: "zh-CN",
  max_results: 5
})

// 网页阅读
mcp__web-reader__read_url({
  url: "https://example.com/article",
  format: "markdown"
})
```

## 🔧 技能系统

本项目包含丰富的 AI 智能体技能，位于 `.roo/skills/` 目录：

| 技能 | 用途 | 关键能力 |
|------|------|----------|
| **web-search** | 网络搜索 | 整合 SearXNG 搜索，支持多种搜索引擎和分类 |
| **web-reader** | 网页阅读 | 内容提取，支持静态/动态页面，Markdown 转换 |
| **agent-workflow** | 智能体工作流 | 长时任务管理，状态持久化，增量执行 |
| **gsd-workflow** | 规范驱动开发 | 项目规划，原子任务拆解，波浪式执行 |
| **task-master** | 任务管理 | WBS+MECE 任务分解，SMART 目标设定 |
| **think-tool** | 智能调度器 | 技能匹配，复杂决策支持，多步骤推理 |

### 技能使用示例
```javascript
// 使用 task-master 技能规划项目
skill("task-master", {
  action: "plan",
  goal: "开发一个待办事项应用",
  scope: "前端 + 后端 + 数据库"
})

// 使用 think-tool 分析复杂问题
skill("think-tool", {
  problem: "如何优化网站加载速度",
  context: "当前加载时间 5s，目标 2s"
})
```

## ⚙️ 配置详解

### SearXNG 配置
- 配置文件: `searxng/settings.yml`
- 默认语言: 中文 (zh-CN)
- 搜索引擎: bing, baidu, 360search, sogou 等
- 安全搜索: 关闭（可调整）

### MCP 服务器配置
- **searxng-mcp**: 连接 SearXNG 实例，提供搜索工具
- **web-reader-mcp**: 基于 trafilatura + playwright 的内容提取

### 环境变量
创建 `.env` 文件（可选）：
```bash
SEARXNG_SECRET=your-secret-key
WEB_READER_TIMEOUT=30
```

## 📊 性能优化

### 资源分配
```yaml
# 在 docker-compose.yml 中调整
services:
  searxng:
    deploy:
      resources:
        limits:
          memory: 1G
          cpus: '0.5'
```

### 缓存策略
- Valkey 缓存搜索结果
- Qdrant 向量存储用于语义搜索
- 本地文件缓存网页内容

## 🔍 搜索技巧

### 高级搜索语法
```javascript
// 精确匹配
mcp__searxng-search__web_search({
  query: '"深度学习框架" site:github.com',
  language: "zh-CN"
})

// 时间范围筛选
mcp__searxng-search__web_search({
  query: "AI 新闻",
  time_range: "week"
})

// 多引擎搜索
mcp__searxng-search__web_search({
  query: "Python 教程",
  engines: "bing,baidu,sogou"
})
```

### 特定类型搜索
| 搜索类型 | 推荐参数 | 说明 |
|----------|----------|------|
| **新闻搜索** | `query + "新闻"`, `time_range: "day"` | 避免使用 `categories: news` |
| **代码搜索** | `engines: "baidu kaifa"` | 百度开发者搜索 |
| **学术搜索** | `categories: "science"` | 学术文献 |
| **图片搜索** | `engines: "bing images,baidu images"` | 图片素材 |
| **微信搜索** | `engines: "sogou wechat"` | 微信公众号文章 |

## 🛠️ 开发与扩展

### 添加新的 MCP 服务器
1. 在 `mcp/` 目录下创建新服务
2. 编写 `Dockerfile` 和 `mcp_server.py`
3. 在 `docker-compose.yml` 中添加服务定义
4. 在 `.roo/mcp.json` 中注册服务器

### 创建新技能
参考现有技能模板：
```bash
.roo/skills/
  your-skill/
    SKILL.md          # 技能文档
    examples/         # 使用示例
    templates/        # 模板文件
    references/       # 参考文档
```

### 调试技巧
```bash
# 查看 MCP 服务器日志
docker-compose logs -f searxng-mcp

# 测试 SearXNG 接口
curl "http://localhost:8080/search?q=test&format=json"

# 进入容器调试
docker-compose exec searxng-mcp /bin/bash
```

## 🤝 贡献指南

欢迎提交 Issue 和 Pull Request 来改进本项目！

1. **报告问题**: 在 Issues 中描述问题，包括复现步骤和日志
2. **功能建议**: 说明使用场景和预期行为
3. **代码贡献**: 遵循现有代码风格，添加适当测试
4. **文档改进**: 更新相关文档和示例

## 📄 许可证

本项目基于 MIT 许可证开源。

## 🙏 致谢

- [SearXNG](https://searxng.org) - 优秀的元搜索引擎
- [Model Context Protocol](https://modelcontextprotocol.io) - AI 工具集成标准
- [Roo Code](https://github.com/rooveterinary/roo-code) - 强大的 AI 智能体框架

## 📞 支持与反馈

- **问题反馈**: GitHub Issues
- **功能请求**: 通过 Issues 提交
- **紧急问题**: 提供完整的日志和环境信息

---

**提示**: 首次启动后，请等待 1-2 分钟让所有服务完全初始化。访问 http://localhost:8080 确认 SearXNG 正常运行。