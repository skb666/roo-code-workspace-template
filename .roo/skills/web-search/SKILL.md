---
name: web-search
description: 网络搜索技能。通过本地 SearXNG 元搜索引擎实现联网搜索，支持网页、新闻、图片、代码、学术等多类型搜索。当需要实时信息、技术文档、代码示例时使用。
---

# Web Search - 网络搜索技能

## 快速参考

| 场景 | MCP 工具 | 关键参数 |
|------|----------|----------|
| 通用搜索 | `mcp__searxng-search__web_search` | `query`, `max_results` |
| 新闻搜索 | `mcp__searxng-search__news_search` | `query`, `time_range` |
| 代码搜索 | `mcp__searxng-search__code_search` | `query`, `language` |
| 学术搜索 | `mcp__searxng-search__academic_search` | `query` |
| 图片搜索 | `mcp__searxng-search__image_search` | `query` |
| 微信文章 | `mcp__searxng-search__wechat_search` | `query` |

## 使用场景

**✅ 使用此技能**：
- 需要实时信息（新闻、天气、股价）
- 查找技术文档和 API 资料
- 搜索代码示例和解决方案
- 学术文献和论文查找
- 用户明确要求搜索网络

**❌ 不使用此技能**：
- 项目代码库内已有答案
- 需要执行本地命令
- 简单的常识性问题

## 可用搜索引擎

| 类别 | 搜索引擎 |
|------|----------|
| 通用 | bing, baidu, 360search, sogou, quark, wikipedia |
| 图片 | bing_images, baidu_images, sogou_images |
| 新闻 | bing_news, qwant |
| 微信 | sogou_wechat |
| IT | baidu_kaifa, github, stackoverflow |

---

## MCP 工具详解

### 1. `mcp__searxng-search__web_search`

通用网络搜索，支持高级语法。

**参数**：

| 参数 | 类型 | 必需 | 说明 |
|------|------|------|------|
| `query` | string | ✅ | 搜索关键词 |
| `engines` | string | | 搜索引擎，如 `google,bing` |
| `language` | string | | 语言代码，默认 `zh-CN` |
| `time_range` | string | | 时间范围：`day`/`week`/`month`/`year` |
| `max_results` | number | | 结果数量，默认 10 |

**调用示例**：
```javascript
mcp__searxng-search__web_search({
  query: "React hooks 教程",
  language: "zh-CN",
  max_results: 5
})
```

### 2. `mcp__searxng-search__news_search`

新闻专用搜索，快速获取时事动态。

**参数**：

| 参数 | 类型 | 必需 | 说明 |
|------|------|------|------|
| `query` | string | ✅ | 新闻关键词 |
| `time_range` | string | | 时间范围，默认 `week` |
| `language` | string | | 语言代码 |
| `max_results` | number | | 结果数量 |

**调用示例**：
```javascript
mcp__searxng-search__news_search({
  query: "人工智能",
  time_range: "day",
  max_results: 10
})
```

### 3. `mcp__searxng-search__code_search`

代码和技术文档搜索。

**调用示例**：
```javascript
mcp__searxng-search__code_search({
  query: "Python asyncio tutorial",
  language: "python",
  max_results: 5
})
```

### 4. `mcp__searxng-search__academic_search`

学术文献搜索。

**调用示例**：
```javascript
mcp__searxng-search__academic_search({
  query: "deep learning survey",
  max_results: 10
})
```

### 5. `mcp__searxng-search__wechat_search`

微信公众号文章搜索。

**调用示例**：
```javascript
mcp__searxng-search__wechat_search({
  query: "前端性能优化",
  max_results: 5
})
```

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

### 时间范围
```
# 使用 time_range 参数
time_range: "day"    # 过去一天
time_range: "week"   # 过去一周
time_range: "month"  # 过去一月
```

### 组合搜索
```
"React hooks" (tutorial OR guide) site:react.dev
Python (error OR exception) -stackoverflow
```

---

## 搜索策略

### 技术问题搜索
```
1. 优先搜索官方文档
   → site:react.dev hooks
   → site:docs.python.org asyncio

2. 查找问答解决方案
   → site:stackoverflow.com [error message]

3. 查找示例代码
   → site:github.com [library] example
```

### 新闻时事搜索
```
1. 使用 news_search 工具
2. 设置 time_range: "day"
3. 对比多个新闻来源
```

### 学术研究搜索
```
1. 使用 academic_search 工具
2. 搜索 Google Scholar
3. 查找论文引用链
```

### 信息核实策略
```
1. 先进行通用搜索
2. 查找官方来源（官网、文档）
3. 查找权威媒体或专家观点
4. 多来源交叉验证
```

---

## 搜索工作流

```
1. 分析需求 → 提取关键词
2. 构造查询 → 应用高级语法
3. 选择工具 → web/news/code/academic
4. 执行搜索 → 调用 MCP 工具
5. 筛选结果 → 取最相关的 3-5 条
6. 呈现信息 → 总结关键点
```

### 迭代优化

如果初次搜索结果不理想：
```
1. 调整关键词（同义词、相关词）
2. 添加/移除限定词
3. 尝试不同搜索引擎
4. 调整时间范围
```

---

## 与其他技能的协作

| 技能 | 协作场景 |
|------|----------|
| `agent-workflow` | 长时任务中需要外部信息 |
| `task-master` | 项目规划时收集资料 |
| `code-review-expert` | 查找最佳实践和规范 |

---

## 注意事项

1. **尊重隐私**：不搜索敏感个人信息
2. **验证来源**：优先使用权威来源
3. **注意时效**：检查信息发布时间
4. **结果筛选**：提供最相关的 3-5 条，不堆砌
5. **语言适配**：根据问题选择语言参数

---

## 配置说明

确保 MCP 服务器已正确配置：
- SearXNG 地址：`http://localhost:8080`
- Python 环境：使用虚拟环境（避免破坏系统依赖）

### 设置虚拟环境

```bash
# 创建虚拟环境（使用 .venv 目录名）
python3 -m venv .venv
# 或者安装 uv（如果未安装）
# curl -LsSf https://astral.sh/uv/install.sh | sh
# uv venv

# 激活虚拟环境
source .venv/bin/activate  # Linux/macOS
# .venv\Scripts\activate   # Windows
```

> **注意**：在 Ubuntu 等系统中，直接使用全局 `pip install` 可能破坏系统依赖，建议始终使用虚拟环境。

### 配置 MCP 服务器

配置文件中的 Python 路径统一为：
```json
{
  "mcpServers": {
    "searxng-search": {
      "command": "${workspaceFolder}/.venv/bin/python",
      "args": ["${workspaceFolder}/mcp/searxng_mcp/mcp_server.py"],
      "env": {
        "SEARXNG_BASE_URL": "http://localhost:8080"
      }
    }
  }
}
```
