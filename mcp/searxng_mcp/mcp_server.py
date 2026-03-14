#!/usr/bin/env python3
"""
SearXNG MCP Server - 为 Roo Code 提供联网搜索能力
基于 Model Context Protocol (MCP) 实现
"""

import asyncio
import json
import os
import sys
import urllib.parse
import urllib.request
import urllib.error
from typing import Any, Optional
from datetime import datetime

# MCP SDK imports
try:
    from mcp.server import Server
    from mcp.server.stdio import stdio_server
    from mcp.types import Tool, TextContent, ImageContent, EmbeddedResource
    import mcp.server as mcp_server
except ImportError:
    print("请安装 mcp: pip install mcp", file=sys.stderr)
    sys.exit(1)

# SearXNG 配置
SEARXNG_BASE_URL = os.environ.get("SEARXNG_BASE_URL", "http://localhost:8080")
DEFAULT_FORMAT = "json"

# 已启用的搜索引擎 (根据实际测试结果配置)
# 注意：引擎名称中的空格是必需的，不要使用下划线
# 某些引擎需要通过 categories 参数调用，而不是直接指定 engines
ENGINES_GENERAL = ["bing", "baidu", "360search", "sogou"]  # 移除了 quark, wikipedia (无结果)
ENGINES_IMAGES = ["bing images", "baidu images", "sogou images", "quark images"]  # quark images 可用
# 新闻、代码、学术搜索使用 categories 而不是 engines，因为单独指定引擎会超时或无结果

# 创建 MCP 服务器实例
server = Server("searxng-search")


def search_searxng(
    query: str,
    engines: Optional[str] = None,
    categories: Optional[str] = None,
    language: str = "zh-CN",
    page: int = 1,
    time_range: Optional[str] = None,
    safesearch: int = 0,
) -> dict:
    """
    执行 SearXNG 搜索请求
    
    Args:
        query: 搜索关键词
        engines: 指定搜索引擎，逗号分隔 (如: google,bing)
        categories: 搜索类别 (general, images, news, videos, etc.)
        language: 语言代码
        page: 页码
        time_range: 时间范围 (day, week, month, year)
        safesearch: 安全搜索级别 (0=关闭, 1=中等, 2=严格)
    
    Returns:
        搜索结果字典
    """
    params = {
        "q": query,
        "format": DEFAULT_FORMAT,
        "language": language,
        "pageno": page,
        "safesearch": safesearch,
    }
    
    if engines:
        params["engines"] = engines
    if categories:
        params["categories"] = categories
    if time_range:
        params["time_range"] = time_range
    
    # 构建请求 URL
    query_string = urllib.parse.urlencode(params)
    url = f"{SEARXNG_BASE_URL}/search?{query_string}"
    
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "RooCode-MCP/1.0"})
        with urllib.request.urlopen(req, timeout=30) as response:
            data = json.loads(response.read().decode("utf-8"))
            return {
                "success": True,
                "data": data,
                "query": query,
                "timestamp": datetime.now().isoformat(),
            }
    except urllib.error.URLError as e:
        return {
            "success": False,
            "error": f"网络错误: {str(e)}",
            "query": query,
        }
    except json.JSONDecodeError as e:
        return {
            "success": False,
            "error": f"JSON 解析错误: {str(e)}",
            "query": query,
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"未知错误: {str(e)}",
            "query": query,
        }


def format_search_results(results: dict, max_results: int = 10) -> str:
    """格式化搜索结果为可读文本"""
    if not results.get("success"):
        return f"搜索失败: {results.get('error', '未知错误')}"
    
    data = results.get("data", {})
    output = []
    
    # 搜索元信息
    output.append(f"## 搜索结果: {results.get('query', '')}")
    output.append(f"引擎: {', '.join(data.get('engines', []))}")
    output.append(f"结果数: {len(data.get('results', []))}")
    output.append("")
    
    # 搜索结果
    for i, item in enumerate(data.get("results", [])[:max_results], 1):
        title = item.get("title", "无标题")
        url = item.get("url", "")
        snippet = item.get("content", "无摘要")
        engine = item.get("engine", "unknown")
        
        output.append(f"### [{i}] {title}")
        output.append(f"**链接**: {url}")
        output.append(f"**摘要**: {snippet}")
        output.append(f"**来源**: {engine}")
        output.append("")
    
    # 相关搜索建议
    if data.get("suggestions"):
        output.append("## 相关搜索建议")
        for suggestion in data.get("suggestions", []):
            output.append(f"- {suggestion}")
    
    return "\n".join(output)


@server.list_tools()
async def list_tools() -> list[Tool]:
    """列出可用的 MCP 工具"""
    return [
        Tool(
            name="web_search",
            description="""执行网络搜索，返回相关结果。
            
支持高级搜索技巧:
- 精确匹配: 用引号包围短语 "exact phrase"
- 排除词: 使用减号 -exclude
- 站内搜索: site:example.com
- 文件类型: filetype:pdf
- 标题搜索: intitle:关键词
- 组合搜索: 使用 AND, OR, NOT

示例:
- 'Python 教程 site:docs.python.org'
- '"machine learning" filetype:pdf'
- 'React hooks -redux'""",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "搜索关键词，支持高级搜索语法",
                    },
                    "engines": {
                        "type": "string",
                        "description": "指定搜索引擎，逗号分隔 (默认: bing,baidu,360search,sogou)。注意：引擎名称包含空格，如 'bing images'",
                    },
                    "categories": {
                        "type": "string",
                        "description": "搜索类别: general, images, news, videos, it, science",
                    },
                    "language": {
                        "type": "string",
                        "description": "语言代码，默认 zh-CN",
                        "default": "zh-CN",
                    },
                    "time_range": {
                        "type": "string",
                        "description": "时间范围: day, week, month, year",
                        "enum": ["day", "week", "month", "year"],
                    },
                    "max_results": {
                        "type": "integer",
                        "description": "返回结果数量上限，默认 10",
                        "default": 10,
                    },
                },
                "required": ["query"],
            },
        ),
        Tool(
            name="news_search",
            description="""搜索新闻内容，专注于时事新闻和媒体报道。

适用于:
- 最新新闻动态
- 时事热点追踪
- 媒体报道查询""",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "新闻搜索关键词",
                    },
                    "time_range": {
                        "type": "string",
                        "description": "时间范围: day, week, month",
                        "enum": ["day", "week", "month"],
                        "default": "week",
                    },
                    "language": {
                        "type": "string",
                        "description": "语言代码",
                        "default": "zh-CN",
                    },
                    "max_results": {
                        "type": "integer",
                        "description": "返回结果数量",
                        "default": 10,
                    },
                },
                "required": ["query"],
            },
        ),
        Tool(
            name="image_search",
            description="""搜索图片内容。

适用于:
- 图片素材查找
- 视觉参考搜索
- 图片信息获取""",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "图片搜索关键词",
                    },
                    "engines": {
                        "type": "string",
                        "description": "图片搜索引擎 (默认: bing images,baidu images,sogou images,quark images)",
                        "default": "bing images,baidu images,sogou images,quark images",
                    },
                    "max_results": {
                        "type": "integer",
                        "description": "返回结果数量",
                        "default": 10,
                    },
                },
                "required": ["query"],
            },
        ),
        Tool(
            name="code_search",
            description="""搜索代码和技术文档。

专门用于:
- 编程问题解答
- 技术文档查找
- API 使用示例
- 开源项目搜索""",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "代码或技术相关搜索关键词",
                    },
                    "language": {
                        "type": "string",
                        "description": "编程语言 (python, javascript, rust, etc.)",
                    },
                    "max_results": {
                        "type": "integer",
                        "description": "返回结果数量",
                        "default": 10,
                    },
                },
                "required": ["query"],
            },
        ),
        Tool(
            name="academic_search",
            description="""搜索学术文献和研究资料。

适用于:
- 学术论文查找
- 研究资料收集
- 引用文献检索

注意: 使用 science 分类进行搜索，涵盖多个学术搜索引擎""",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "学术搜索关键词",
                    },
                    "max_results": {
                        "type": "integer",
                        "description": "返回结果数量",
                        "default": 10,
                    },
                },
                "required": ["query"],
            },
        ),
        Tool(
            name="wechat_search",
            description="""搜索微信公众号文章。

适用于:
- 微信公众号内容搜索
- 中文资讯文章查找
- 热点文章追踪""",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "微信文章搜索关键词",
                    },
                    "max_results": {
                        "type": "integer",
                        "description": "返回结果数量",
                        "default": 10,
                    },
                },
                "required": ["query"],
            },
        ),
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict[str, Any]) -> list[TextContent]:
    """执行工具调用"""
    
    if name == "web_search":
        results = search_searxng(
            query=arguments.get("query"),
            engines=arguments.get("engines"),
            categories=arguments.get("categories"),
            language=arguments.get("language", "zh-CN"),
            time_range=arguments.get("time_range"),
        )
        formatted = format_search_results(results, arguments.get("max_results", 10))
        return [TextContent(type="text", text=formatted)]
    
    elif name == "news_search":
        # 不使用 categories="news"，因为它会调用不可用的新闻引擎
        # 改用通用搜索引擎 + 新闻关键词 + 时间范围
        query = arguments.get("query")
        time_range = arguments.get("time_range", "day")
        
        # 如果查询中不包含新闻相关词汇，添加提示
        news_keywords = ["新闻", "news", "资讯", "热点", "头条", "报道"]
        has_news_keyword = any(kw in query.lower() for kw in news_keywords)
        if not has_news_keyword:
            query = f"{query} 新闻"
        
        results = search_searxng(
            query=query,
            engines="baidu,bing,sogou,360search",  # 使用中国可用的搜索引擎
            language=arguments.get("language", "zh-CN"),
            time_range=time_range,
        )
        formatted = format_search_results(results, arguments.get("max_results", 10))
        return [TextContent(type="text", text=formatted)]
    
    elif name == "image_search":
        results = search_searxng(
            query=arguments.get("query"),
            engines=arguments.get("engines", "bing images,baidu images,sogou images,quark images"),
            categories="images",
        )
        formatted = format_search_results(results, arguments.get("max_results", 10))
        return [TextContent(type="text", text=formatted)]
    
    elif name == "code_search":
        # 构造代码相关搜索
        query = arguments.get("query")
        if language := arguments.get("language"):
            query = f"{query} {language} programming"
        
        # 使用 IT 分类，不指定 engines 以避免冲突
        results = search_searxng(
            query=query,
            categories="it",
        )
        formatted = format_search_results(results, arguments.get("max_results", 10))
        return [TextContent(type="text", text=formatted)]
    
    elif name == "academic_search":
        results = search_searxng(
            query=arguments.get("query"),
            categories="science",
        )
        formatted = format_search_results(results, arguments.get("max_results", 10))
        return [TextContent(type="text", text=formatted)]
    
    elif name == "wechat_search":
        results = search_searxng(
            query=arguments.get("query"),
            engines="sogou wechat",
            language="zh-CN",
        )
        formatted = format_search_results(results, arguments.get("max_results", 10))
        return [TextContent(type="text", text=formatted)]
    
    else:
        return [TextContent(type="text", text=f"未知工具: {name}")]


async def run_server():
    """运行 MCP 服务器"""
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options(),
        )


if __name__ == "__main__":
    asyncio.run(run_server())
