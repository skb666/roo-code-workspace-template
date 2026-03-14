# Web Reader MCP Server

为 AI Agent 提供网页内容阅读能力的 MCP 服务器。

## 功能

- **读取网页内容**：提取正文、元数据（标题、作者、日期等）
- **多格式输出**：Markdown、纯文本、JSON
- **动态页面支持**：使用 Playwright 处理 JavaScript 渲染的页面
- **批量读取**：同时处理多个 URL
- **链接提取**：提取页面中的相关链接

## 技术栈

- **Trafilatura**：高质量内容提取，基准测试最佳
- **Playwright**：动态页面渲染（可选）
- **MCP SDK**：Model Context Protocol 支持

## 安装

### 方式一：Docker（推荐）

```bash
# 构建镜像
docker build -t web-reader-mcp .

# 运行容器
docker run -i web-reader-mcp
```

### 方式二：本地安装

```bash
# 基础安装
pip install mcp trafilatura

# 动态页面支持（可选）
pip install playwright
playwright install chromium
```

## 配置 MCP 客户端

在 MCP 客户端配置中添加：

```json
{
  "mcpServers": {
    "web-reader": {
      "command": "docker",
      "args": ["run", "-i", "web-reader-mcp"]
    }
  }
}
```

或使用本地 Python：

```json
{
  "mcpServers": {
    "web-reader": {
      "command": "python",
      "args": ["/path/to/mcp_server.py"]
    }
  }
}
```

## 可用工具

### `read_url`

读取单个 URL 的内容。

**参数**：
- `url` (必需): URL 地址
- `format`: 输出格式 (markdown/text/json)，默认 markdown
- `use_dynamic`: 是否使用动态渲染，默认 false
- `wait_selector`: 等待的 CSS 选择器
- `include_links`: 是否提取链接，默认 false
- `brief`: 是否返回简化版本，默认 false
- `timeout`: 超时时间（秒），默认 30

### `read_urls`

批量读取多个 URL。

**参数**：
- `urls` (必需): URL 列表
- `format`: 输出格式
- `use_dynamic`: 是否使用动态渲染
- `include_links`: 是否提取链接

### `check_url`

快速检查 URL 是否可访问。

**参数**：
- `url` (必需): URL 地址

## 使用示例

```python
# 读取文章
read_url(url="https://example.com/article")

# 动态页面
read_url(url="https://spa.example.com", use_dynamic=true)

# 等待特定元素
read_url(url="...", wait_selector=".content")

# 批量读取
read_urls(urls=["url1", "url2", "url3"])
```

## 环境变量

- `WEB_READER_TIMEOUT`: 默认超时时间（秒），默认 30
- `WEB_READER_USER_AGENT`: 自定义 User-Agent

## 依赖说明

| 依赖 | 用途 | 必需 |
|------|------|------|
| mcp | MCP 协议支持 | ✅ |
| trafilatura | 内容提取 | ✅ |
| playwright | 动态页面渲染 | ❌ 可选 |

## 故障排除

### Trafilatura 未安装

如果 trafilatura 未安装，会自动使用简化模式（正则提取），内容质量会降低。

### Playwright 未安装

动态页面渲染需要 playwright。如果未安装，动态页面将无法正确处理。

安装：
```bash
pip install playwright
playwright install chromium
```

## 许可证

MIT License
