---
name: web-search
description: 网络搜索技能。通过本地 SearXNG 元搜索引擎搜索网络，返回相关 URL 列表和摘要。配合 web-reader 技能使用，构成 AI Agent 的"搜索+阅读"闭环。
---

# Web Search - 网络搜索技能

## 核心理念

**搜索是 AI Agent 看世界的第一步**。本技能负责找到相关信息，配合 `web-reader` 技能完成内容获取。

```
用户问题 → web-search (搜索) → URL 列表 + 摘要
                                      ↓
                               Agent 选择相关链接
                                      ↓
                               web-reader (阅读) → 完整内容
```

---

## 快速参考

| 工具 | 用途 | 搜索方式 |
|------|------|----------|
| `mcp__searxng-search__web_search` | 通用搜索 | engines: bing, baidu, 360search, sogou |
| `mcp__searxng-search__web_search` | 新闻搜索 | query + "新闻", time_range: day |
| `mcp__searxng-search__web_search` | 代码搜索 | engines: baidu kaifa |
| `mcp__searxng-search__academic_search` | 学术搜索 | categories: science |
| `mcp__searxng-search__image_search` | 图片搜索 | engines: bing images, baidu images, sogou images, quark images |
| `mcp__searxng-search__wechat_search` | 微信文章 | engines: sogou wechat |

---

## 使用场景

**✅ 使用**：
- 需要实时信息（新闻、天气、股价）
- 查找技术文档和 API 资料
- 搜索代码示例和解决方案
- 学术文献查找
- 用户明确要求搜索

**❌ 不使用**：
- 项目代码库内已有答案
- 需要执行本地命令
- 简单常识问题

---

## 工具详解

### `web_search` - 通用搜索

```javascript
mcp__searxng-search__web_search({
  query: "React hooks 教程",
  language: "zh-CN",
  max_results: 5
})
```

**参数**：
| 参数 | 类型 | 说明 |
|------|------|------|
| `query` | string | 搜索关键词（支持高级语法） |
| `engines` | string | 搜索引擎：`bing,baidu,360search,sogou`（名称含空格） |
| `categories` | string | 搜索类别：`general`, `images`, `news`, `it`, `science` |
| `language` | string | 语言代码，默认 `zh-CN` |
| `time_range` | string | 时间范围：`day`/`week`/`month`/`year` |
| `max_results` | number | 结果数量，默认 10 |

### `news_search` - 新闻搜索

```javascript
// 推荐方式：使用 web_search + 新闻关键词
mcp__searxng-search__web_search({
  query: "人工智能 最新动态 新闻",
  language: "zh-CN",
  time_range: "day",
  max_results: 10
})

// 或指定中国可用的搜索引擎
mcp__searxng-search__web_search({
  query: "人工智能最新动态",
  engines: "baidu,bing,sogou",
  time_range: "day",
  max_results: 10
})
```

**重要说明**：
- **不推荐使用 `categories: news`**：该参数会调用 google news, bing news 等在中国不可用的引擎，导致返回空结果
- **推荐方式**：使用 `web_search` 并在查询中添加"新闻"关键词，或使用 `time_range: "day"` 筛选最新内容
- 中国可用的通用搜索引擎：`baidu, bing, sogou, 360search`

### `code_search` - 代码搜索

```javascript
mcp__searxng-search__code_search({
  query: "Python asyncio 并发编程",
  language: "python",
  max_results: 5
})
```

**注意**：使用 `categories: it` 进行搜索。

### `academic_search` - 学术搜索

```javascript
mcp__searxng-search__academic_search({
  query: "machine learning transformer",
  max_results: 10
})
```

**注意**：使用 `categories: science` 进行搜索（arxiv, pubmed 等单独指定会超时）。

---

## 高级搜索语法

### 精确匹配
```
"React hooks" tutorial     # 必须包含 "React hooks"
```

### 排除关键词
```
jaguar -car               # 搜索 jaguar 但排除汽车
python -snake             # 排除蛇相关
```

### 站内搜索
```
site:github.com "react component"
site:stackoverflow.com python error
site:docs.python.org asyncio
```

### 文件类型
```
filetype:pdf "machine learning"
filetype:docx 合同模板
```

### 组合搜索
```
"React hooks" (tutorial OR guide) site:react.dev
Python (error OR exception) -stackoverflow
```

---

## 搜索策略

### 技术问题
```
1. 官方文档优先
   → site:react.dev hooks
   → site:docs.python.org asyncio

2. 问答解决方案
   → site:stackoverflow.com [error message]

3. 示例代码
   → site:github.com [library] example
```

### 新闻时事
```
1. 使用 web_search + 新闻关键词
   → query: "今日热点新闻"
   → time_range: "day"
   
2. 或指定中国可用的引擎
   → engines: "baidu,bing,sogou"
```

### 学术研究
```
1. 使用 academic_search (categories: science)
2. 搜索关键词如 "machine learning", "neural network"
3. 查找引用链
```

---

## 与 web-reader 协作

**完整工作流**：

```
1. 搜索 → 获取 URL 列表 + 摘要
   mcp__searxng-search__web_search({query: "..."})
   
2. 分析 → 根据摘要判断相关性

3. 阅读 → 获取相关 URL 的完整内容
   mcp__web-reader__read_url({url: "..."})
   
4. 整合 → 综合信息回答用户
```

**示例**：
```
用户: "比较 React 和 Vue 的性能差异"

步骤1: web_search({query: "React vs Vue performance comparison"})
       → 返回 5 个相关 URL

步骤2: 分析摘要，选择最相关的 2-3 个 URL

步骤3: read_url({url: "selected_url_1"})
       read_url({url: "selected_url_2"})

步骤4: 整合内容，生成对比报告
```

---

## 注意事项

1. **结果筛选**：提供最相关的 3-5 条，不堆砌
2. **验证来源**：优先权威来源
3. **注意时效**：检查信息发布时间
4. **隐私保护**：不搜索敏感个人信息

---

## 配置

### 前提条件

确保 SearXNG 服务已启动：
```bash
cd searxng
docker-compose up -d
```

### MCP 配置

```json
{
  "mcpServers": {
    "searxng-search": {
      "command": "python",
      "args": ["mcp/searxng_mcp/mcp_server.py"],
      "env": {
        "SEARXNG_BASE_URL": "http://localhost:8080"
      }
    }
  }
}
```

---

## 可用搜索引擎

| 工具 | 搜索方式 | 说明 |
|------|----------|------|
| `web_search` | engines | bing, baidu, 360search, sogou |
| `web_search` | query + "新闻" | **推荐的新闻搜索方式**，配合 time_range |
| `image_search` | engines | bing images, baidu images, sogou images, quark images |
| `academic_search` | categories: science | 学术分类搜索 |
| `wechat_search` | engines: sogou wechat | 微信公众号文章 |

**重要说明**:
- 引擎名称必须包含空格：`"bing images"` 而非 `"bing_images"`
- **新闻搜索**：**不推荐使用 `categories="news"`**，它会调用 google news 等不可用引擎，返回空结果
- **推荐方式**：使用 `web_search` + 查询词含"新闻" + `time_range`

**已知限制**:
- `categories: news` 会调用不可用的新闻引擎，**会导致空结果**
- `categories: it` 部分引擎可能超时，建议使用通用搜索
- arxiv, pubmed → 使用 `categories="science"`
- quark (通用), wikipedia → 已从默认引擎移除（无结果）
