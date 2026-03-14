---
name: web-reader
description: 网页阅读技能。读取 URL 内容并提取结构化信息，支持静态和动态页面。配合 web-search 技能使用，构成 AI Agent 的"搜索+阅读"闭环。
---

# Web Reader - 网页阅读技能

## 核心理念

**阅读是 AI Agent 看世界的第二步**。本技能负责提取网页内容，配合 `web-search` 技能完成信息获取闭环。

```
web-search → URL 列表 + 摘要
                  ↓
            Agent 选择相关链接
                  ↓
web-reader → 完整内容 + 元数据
```

---

## 快速参考

| 工具 | 用途 | 关键参数 |
|------|------|----------|
| `mcp__web-reader__read_url` | 读取单个 URL | `url`, `format` |
| `mcp__web-reader__read_urls` | 批量读取 | `urls` |
| `mcp__web-reader__check_url` | 检查链接可用性 | `url` |

---

## 使用场景

**✅ 使用**：
- web-search 返回了相关 URL，需要获取详细内容
- 用户提供了具体的 URL
- 需要提取文章/文档内容
- 需要获取页面元数据（标题、作者、日期）

**❌ 不使用**：
- 只需要 URL 列表和摘要（使用 web-search）
- 项目代码库内已有内容
- 需要与网页交互（登录、填写表单等）

---

## 工具详解

### `read_url` - 读取单个 URL

**参数**：

| 参数 | 类型 | 必需 | 说明 |
|------|------|------|------|
| `url` | string | ✅ | URL 地址 |
| `format` | string | | 输出格式：`markdown`(默认)/`text`/`json` |
| `use_dynamic` | boolean | | 是否使用动态渲染，默认 `false` |
| `wait_selector` | string | | 等待的 CSS 选择器 |
| `include_links` | boolean | | 是否提取页面链接，默认 `false` |
| `brief` | boolean | | 是否返回简化版本，默认 `false` |
| `timeout` | integer | | 超时时间（秒），默认 30 |

**调用示例**：

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

// 等待特定元素
mcp__web-reader__read_url({
  url: "https://example.com",
  wait_selector: ".content-loaded",
  use_dynamic: true
})

// 获取链接
mcp__web-reader__read_url({
  url: "https://example.com",
  include_links: true
})

// JSON 格式输出
mcp__web-reader__read_url({
  url: "https://example.com",
  format: "json"
})
```

**输出示例**：

```markdown
# 文章标题

**URL**: https://example.com/article
**作者**: 张三
**日期**: 2024-01-15

---

## 正文内容

这里是提取的正文内容...
```

---

### `read_urls` - 批量读取

**参数**：

| 参数 | 类型 | 必需 | 说明 |
|------|------|------|------|
| `urls` | array | ✅ | URL 列表 |
| `format` | string | | 输出格式 |
| `use_dynamic` | boolean | | 是否动态渲染 |
| `include_links` | boolean | | 是否提取链接 |

**调用示例**：

```javascript
mcp__web-reader__read_urls({
  urls: [
    "https://example.com/article1",
    "https://example.com/article2",
    "https://example.com/article3"
  ],
  format: "markdown"
})
```

**输出示例**：

```markdown
## 批量读取结果
总数: 3 | 成功: 3 | 失败: 0

### [1] 文章标题1
**URL**: https://example.com/article1
**内容摘要**:
第一篇文章的内容摘要...

### [2] 文章标题2
**URL**: https://example.com/article2
**内容摘要**:
第二篇文章的内容摘要...

### [3] 文章标题3
...
```

---

### `check_url` - 快速检查

**用途**：验证链接有效性，不提取内容。

**参数**：

| 参数 | 类型 | 必需 | 说明 |
|------|------|------|------|
| `url` | string | ✅ | URL 地址 |

**调用示例**：

```javascript
mcp__web-reader__check_url({
  url: "https://example.com"
})
```

**输出**：
```
✅ URL 可访问
**URL**: https://example.com
**状态码**: 200
**内容长度**: 12345 字符
```

---

## 输出格式

### Markdown（默认）
- LLM 友好
- 保留文章结构
- 包含元数据

### Text
- 纯文本
- 适合简单处理

### JSON
- 结构化数据
- 适合程序处理

---

## 静态 vs 动态页面

### 静态页面（默认）
- 大多数网站
- 快速、轻量
- 使用 `trafilatura` 提取

### 动态页面
- SPA 应用（React、Vue 等）
- 需要设置 `use_dynamic: true`
- 使用 `playwright` 渲染
- 耗时较长

**何时使用动态模式**：
- 页面内容通过 JavaScript 加载
- 搜索结果页是空白骨架
- 页面需要交互才能显示内容

---

## 与 web-search 协作

**标准工作流**：

```
1. 用户提问
   "比较 React 和 Vue 的性能"

2. 搜索获取列表
   web_search({query: "React vs Vue performance"})
   → 返回 5 个相关 URL + 摘要

3. 分析相关性
   根据标题和摘要判断哪些值得深入阅读

4. 选择性阅读
   read_url({url: "most_relevant_url_1"})
   read_url({url: "most_relevant_url_2"})
   
   或批量：
   read_urls({urls: ["url1", "url2", "url3"]})

5. 整合信息
   综合阅读结果，生成答案
```

**最佳实践**：

1. **先搜索后阅读**：不要盲目读取每个 URL
2. **根据摘要筛选**：选择最相关的 2-3 个 URL
3. **合理使用批量**：3 个以上 URL 用 `read_urls`
4. **动态页面谨慎**：只在必要时使用动态模式

---

## 常见问题

### Q: 内容提取不完整？

A: 可能是动态页面，尝试：
```javascript
read_url({
  url: "...",
  use_dynamic: true,
  wait_selector: ".content"
})
```

### Q: 页面超时？

A: 增加超时时间：
```javascript
read_url({
  url: "...",
  timeout: 60
})
```

### Q: 需要特定区域内容？

A: 使用 `wait_selector` 等待目标元素：
```javascript
read_url({
  url: "...",
  use_dynamic: true,
  wait_selector: "#main-content"
})
```

### Q: 提取链接用于后续探索？

A: 设置 `include_links: true`：
```javascript
read_url({
  url: "...",
  include_links: true
})
```

---

## 配置

### Docker 部署（推荐）

```bash
cd mcp/web_reader_mcp
docker build -t web-reader-mcp .
```

### MCP 配置

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

### 本地安装

```bash
pip install mcp trafilatura playwright
playwright install chromium
```

```json
{
  "mcpServers": {
    "web-reader": {
      "command": "python",
      "args": ["mcp/web_reader_mcp/mcp_server.py"]
    }
  }
}
```

---

## 技术栈

| 组件 | 用途 | 必需 |
|------|------|------|
| Trafilatura | 内容提取 | ✅ |
| Playwright | 动态渲染 | ❌ 可选 |
| MCP SDK | 协议支持 | ✅ |

---

## 性能说明

| 模式 | 平均耗时 | 适用场景 |
|------|----------|----------|
| 静态 | 1-3 秒 | 大多数页面 |
| 动态 | 5-15 秒 | SPA、动态加载 |

**建议**：优先使用静态模式，仅在必要时切换动态模式。
