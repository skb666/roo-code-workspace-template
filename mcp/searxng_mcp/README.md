# Roo Code SearXNG 集成

为 Roo Code 提供 SearXNG 元搜索引擎集成，实现联网搜索能力。

## 目录结构

```
./
├── mcp/
│   └── searxng_mcp/          # MCP 服务器
│       ├── mcp_server.py     # MCP 服务器主程序
│       ├── pyproject.toml    # Python 项目配置
│       └── mcp_config.json   # MCP 配置（Roo Code 使用）
│
├── .roo/
│   └── skills/
│       └── web-search/       # 搜索技能
│           └── SKILL.md      # 技能定义文件
│
└── searxng/                  # SearXNG 部署
    ├── docker-compose.yml
    └── searxng/
        └── settings.yml
```

## 安装步骤

### 1. 安装 MCP 依赖

```bash
pip3 install mcp
```

### 2. 在 Roo Code 中配置 MCP

在 Roo Code 设置中添加 MCP 服务器配置：

```json
{
  "mcpServers": {
    "searxng-search": {
      "command": "python3",
      "args": ["${workspaceFolder}/mcp/searxng_mcp/mcp_server.py"],
      "env": {
        "SEARXNG_BASE_URL": "http://localhost:8080"
      }
    }
  }
}
```

### 3. 确保 SearXNG 运行

```bash
cd searxng
docker-compose up -d
```

验证 SearXNG 运行状态：
```bash
curl http://localhost:8080/search?q=test&format=json
```

## 可用工具

MCP 服务器提供以下搜索工具：

| 工具名 | 用途 | 默认引擎 |
|--------|------|----------|
| `web_search` | 通用网络搜索 | bing, baidu, 360search, sogou, quark, wikipedia |
| `news_search` | 新闻搜索 | bing_news, qwant |
| `image_search` | 图片搜索 | bing_images, baidu_images, sogou_images, quark_images |
| `code_search` | 代码/技术搜索 | bing, baidu, github, stackoverflow |
| `academic_search` | 学术文献搜索 | bing, arxiv, pubmed |
| `wechat_search` | 微信公众号文章 | sogou_wechat |

## 高级搜索语法

支持 Google 风格的高级搜索：

- `"精确短语"` - 完全匹配
- `-排除词` - 排除包含该词的结果
- `site:example.com` - 站内搜索
- `filetype:pdf` - 文件类型
- `intitle:关键词` - 标题搜索
- `time_range` - 时间范围

## 故障排除

### MCP 连接失败
1. 检查 Python 环境是否安装 `mcp` 包
2. 检查文件路径是否正确
3. 查看 Roo Code 日志

### 搜索无结果
1. 确认 SearXNG 正在运行
2. 检查 `http://localhost:8080` 是否可访问
3. 查看搜索参数是否正确
