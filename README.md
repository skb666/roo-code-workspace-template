# Roo 代码工作区模板

![GitHub](https://img.shields.io/badge/GitHub-模板仓库-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![Roo Code](https://img.shields.io/badge/Roo_Code-已启用-orange)

> **模板仓库**：此仓库是一个模板，用户可以使用相同的目录结构和文件生成新仓库。[了解更多关于模板仓库的信息](https://docs.github.com/cn/repositories/creating-and-managing-repositories/creating-a-template-repository)。

这是一个为 Roo Code AI 助手开发预配置的工作区模板，包含 MCP 服务器集成、即用型技能和本地搜索引擎部署。

## 🚀 功能特性

- **MCP 服务器集成**：内置 SearXNG MCP 服务器，提供联网搜索能力
- **预装技能**：Agent 工作流、任务管理、网络搜索等技能
- **本地搜索引擎**：基于 Docker 的 SearXNG 部署，支持私有化、可定制搜索
- **Roo Code 就绪**：预配置的 `.roo/mcp.json` 和技能目录
- **模板结构**：为 AI 开发项目优化的目录布局

## 📁 项目结构

```
.
├── .roo/                          # Roo Code 配置
│   ├── mcp.json                  # MCP 服务器配置
│   └── skills/                   # 预装技能
│       ├── agent-workflow/       # Agent 工作流管理技能
│       ├── task-master/          # 任务规划与跟踪技能
│       └── web-search/           # 网络搜索集成技能
├── mcp/                          # MCP 服务器
│   └── searxng_mcp/             # SearXNG MCP 服务器实现
│       ├── mcp_server.py        # MCP 服务器 Python 脚本
│       ├── pyproject.toml       # Python 依赖配置
│       ├── mcp_config.json      # MCP 配置
│       └── README.md            # MCP 服务器文档
├── searxng/                      # SearXNG 搜索引擎部署
│   ├── docker-compose.yml       # SearXNG Docker Compose 配置
│   └── searxng/
│       └── settings.yml         # SearXNG 配置
└── .gitignore                   # Git 忽略规则
```

## 🏁 快速开始

### 使用此模板

1. **生成新仓库**
   - 在 GitHub 上点击 "Use this template"（使用此模板）按钮
   - 创建新仓库并指定名称
   - 将新仓库克隆到本地

2. **克隆与设置**
   ```bash
   git clone https://github.com/你的用户名/你的新仓库.git
   cd 你的新仓库
   ```

3. **初始化 Roo Code**
   - 在 VS Code 中打开项目（确保已安装 Roo Code 扩展）
   - 工作区将自动检测配置

### 启动搜索引擎

1. **启动 SearXNG**
   ```bash
   cd searxng
   docker-compose up -d
   ```

2. **验证安装**
   ```bash
   curl http://localhost:8080/search?q=test&format=json
   ```

3. **配置 Roo Code**
   - `.roo/mcp.json` 已配置为使用本地 SearXNG 实例
   - 重启 Roo Code 或重新加载工作区以激活 MCP 服务器

## 🔧 技能概览

### 🤖 Agent 工作流技能
**位置**: `.roo/skills/agent-workflow/`

全面的 AI 代理工作流管理，包括：
- 任务分解与执行跟踪
- 跨会话状态持久化
- 验证清单和进度报告
- 基于模板的工作流初始化

### 📋 任务管理专家技能
**位置**: `.roo/skills/task-master/`

采用专业方法论的高级任务管理：
- WBS（工作分解结构）+ MECE 任务分解
- SMART 目标设定与跟踪
- 诺依曼问题重构
- 金字塔原理汇报表达

### 🌐 网络搜索技能
**位置**: `.roo/skills/web-search/`

与 SearXNG MCP 服务器集成，提供：
- 多搜索引擎网络搜索
- 新闻、图片、代码、学术搜索
- 中文搜索支持（微信公众号文章）
- 高级搜索语法支持

## 🔍 MCP 服务器：SearXNG 搜索

MCP 服务器为 AI 助手提供实时网络搜索能力：

### 可用工具
| 工具 | 描述 | 默认搜索引擎 |
|------|------|--------------|
| `web_search` | 通用网络搜索 | bing, baidu, 360search, sogou, quark, wikipedia |
| `news_search` | 新闻文章搜索 | bing_news, qwant |
| `image_search` | 图片搜索 | bing_images, baidu_images, sogou_images, quark_images |
| `code_search` | 代码与技术搜索 | bing, baidu, github, stackoverflow |
| `academic_search` | 学术文献搜索 | bing, arxiv, pubmed |
| `wechat_search` | 微信公众号文章搜索 | sogou_wechat |

### 搜索语法
- `"精确短语"` - 完全匹配
- `-排除词` - 排除包含该词的结果
- `site:example.com` - 站内搜索
- `filetype:pdf` - 文件类型筛选
- `intitle:关键词` - 标题搜索
- `time_range` - 时间范围筛选

## 🐛 故障排除

### MCP 连接问题
1. 确保已安装 Python 3.8+
2. **设置 Python 虚拟环境（推荐）**：
   
   为避免破坏 Ubuntu 系统依赖，建议使用虚拟环境隔离 Python 包。提供两种方法：
   
   **方法一：使用 venv（Python 内置）**
   ```bash
   # 创建虚拟环境（使用 .venv 目录名）
   python3 -m venv .venv
   
   # 激活虚拟环境
   source .venv/bin/activate  # Linux/macOS
   # .venv\Scripts\activate   # Windows
   
   # 安装依赖
   pip install mcp
   ```
   
   **方法二：使用 uv（推荐，更快）**
   ```bash
   # 安装 uv（如果未安装）
   curl -LsSf https://astral.sh/uv/install.sh | sh
   
   # 创建虚拟环境（默认使用 .venv 目录名）
   uv venv
   
   # 安装依赖
   uv pip install mcp
   ```
   
   **两种方法对比**：
   | 特性 | venv | uv |
   |------|------|-----|
   | 安装 | Python 内置，无需额外安装 | 需要安装 uv |
   | 速度 | 较慢 | 快（Rust 实现）|
   | 包管理 | pip | uv pip |
   | 锁文件 | 不支持 | 支持 uv.lock |
   | 推荐场景 | 简单项目、无额外依赖 | 现代项目、需要快速安装 |
   
3. 验证 SearXNG 是否运行：
   ```bash
   docker ps | grep searxng
   ```

### 搜索不工作
1. 检查 SearXNG 可访问性：
   ```bash
   curl http://localhost:8080
   ```
2. 如果 SearXNG 运行在不同端口，更新 `.roo/mcp.json`
3. 更改配置后重启 Roo Code

### Docker 问题
1. 确保已安装 Docker 和 Docker Compose
2. 检查 8080 端口是否被占用：
   ```bash
   sudo lsof -i :8080
   ```

## 📝 自定义

### 添加新技能
1. 在 `.roo/skills/` 中创建新目录
2. 添加 `SKILL.md` 文件定义技能
3. 更新相关配置文件

### 修改 MCP 配置
编辑 `.roo/mcp.json` 以：
- 更改 SearXNG URL 或端口
- 添加新的 MCP 服务器
- 修改工具权限

### 扩展 SearXNG 配置
修改 `searxng/searxng/settings.yml` 以：
- 添加或删除搜索引擎
- 配置隐私设置
- 自定义搜索偏好

## 🤝 贡献

欢迎改进此模板！建议和拉取请求均可。

1. 复刻仓库
2. 创建功能分支
3. 进行更改
4. 提交拉取请求

## 📄 许可证

This template is licensed under the MIT License. See the LICENSE file for details.

## 🙏 Acknowledgements

- [Roo Code](https://roocode.com/) - AI assistant development platform
- [SearXNG](https://searxng.github.io/searxng/) - Privacy-respecting metasearch engine
- [MCP (Model Context Protocol)](https://spec.modelcontextprotocol.io/) - Standard for AI tool integration

---

**Template Repository**: Use this template to quickly bootstrap AI assistant projects with Roo Code. All configurations are pre-tested and ready for immediate use.