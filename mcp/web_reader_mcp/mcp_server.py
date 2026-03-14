#!/usr/bin/env python3
"""
Web Reader MCP Server - 为 AI Agent 提供网页内容阅读能力
基于 Trafilatura + Playwright 实现
"""

import asyncio
import json
import os
import sys
import re
import urllib.parse
import urllib.request
import urllib.error
from typing import Any, Optional
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor

# MCP SDK imports
try:
    from mcp.server import Server
    from mcp.server.stdio import stdio_server
    from mcp.types import Tool, TextContent
except ImportError:
    print("请安装 mcp: pip install mcp", file=sys.stderr)
    sys.exit(1)

# Trafilatura for content extraction
try:
    import trafilatura
    from trafilatura.settings import use_config
    TRAFILATURA_AVAILABLE = True
except ImportError:
    TRAFILATURA_AVAILABLE = False
    print("警告: trafilatura 未安装，将使用简化模式", file=sys.stderr)

# Playwright for dynamic content (optional)
try:
    from playwright.sync_api import sync_playwright
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False

# 配置
DEFAULT_TIMEOUT = int(os.environ.get("WEB_READER_TIMEOUT", "30"))
DEFAULT_USER_AGENT = os.environ.get(
    "WEB_READER_USER_AGENT",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
)

# 创建 MCP 服务器实例
server = Server("web-reader")

# 线程池用于并行处理
executor = ThreadPoolExecutor(max_workers=5)


def fetch_url_static(url: str, timeout: int = DEFAULT_TIMEOUT) -> dict:
    """
    使用 urllib 获取静态页面内容
    
    Returns:
        dict: {success, html, status_code, headers, error}
    """
    try:
        req = urllib.request.Request(
            url,
            headers={"User-Agent": DEFAULT_USER_AGENT}
        )
        with urllib.request.urlopen(req, timeout=timeout) as response:
            html = response.read().decode("utf-8", errors="ignore")
            return {
                "success": True,
                "html": html,
                "status_code": response.status,
                "headers": dict(response.headers),
                "final_url": response.url,
            }
    except urllib.error.HTTPError as e:
        return {
            "success": False,
            "error": f"HTTP {e.code}: {e.reason}",
            "status_code": e.code,
        }
    except urllib.error.URLError as e:
        return {
            "success": False,
            "error": f"网络错误: {str(e)}",
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"未知错误: {str(e)}",
        }


def fetch_url_dynamic(url: str, timeout: int = DEFAULT_TIMEOUT, wait_selector: str = None) -> dict:
    """
    使用 Playwright 获取动态页面内容
    
    Returns:
        dict: {success, html, status_code, error}
    """
    if not PLAYWRIGHT_AVAILABLE:
        return {
            "success": False,
            "error": "Playwright 未安装，无法处理动态页面",
        }
    
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page(user_agent=DEFAULT_USER_AGENT)
            
            # 设置超时
            page.set_default_timeout(timeout * 1000)
            
            # 访问页面
            response = page.goto(url, wait_until="networkidle")
            
            # 等待特定选择器
            if wait_selector:
                page.wait_for_selector(wait_selector, timeout=timeout * 1000)
            
            # 获取渲染后的 HTML
            html = page.content()
            final_url = page.url
            status = response.status if response else 200
            
            browser.close()
            
            return {
                "success": True,
                "html": html,
                "status_code": status,
                "final_url": final_url,
            }
    except Exception as e:
        return {
            "success": False,
            "error": f"Playwright 错误: {str(e)}",
        }


def extract_content(html: str, url: str, output_format: str = "markdown") -> dict:
    """
    使用 Trafilatura 提取内容
    
    Args:
        html: HTML 内容
        url: 原始 URL
        output_format: 输出格式 (markdown, json, text)
    
    Returns:
        dict: {content, metadata, links}
    """
    if not TRAFILATURA_AVAILABLE:
        # 简化模式：使用正则提取
        return extract_content_simple(html, url)
    
    try:
        # 配置 trafilatura
        config = use_config()
        config.set("DEFAULT", "EXTRACTION_TIMEOUT", "0")  # 无超时限制
        
        # 提取正文
        if output_format == "json":
            content = trafilatura.extract(
                html,
                output_format="json",
                url=url,
                include_comments=False,
                include_tables=True,
                config=config,
            )
            data = json.loads(content) if content else {}
            return {
                "content": data.get("text", ""),
                "metadata": {
                    "title": data.get("title", ""),
                    "author": data.get("author", ""),
                    "date": data.get("date", ""),
                    "url": url,
                },
                "format": "text",
            }
        
        elif output_format == "markdown":
            content = trafilatura.extract(
                html,
                output_format="markdown",
                url=url,
                include_comments=False,
                include_tables=True,
                include_links=True,
                config=config,
            )
            # 提取元数据
            metadata = trafilatura.extract_metadata(html, url=url)
            return {
                "content": content or "",
                "metadata": metadata.asdict() if metadata else {"url": url},
                "format": "markdown",
            }
        
        else:  # text
            content = trafilatura.extract(
                html,
                output_format="txt",
                url=url,
                include_comments=False,
                config=config,
            )
            metadata = trafilatura.extract_metadata(html, url=url)
            return {
                "content": content or "",
                "metadata": metadata.asdict() if metadata else {"url": url},
                "format": "text",
            }
            
    except Exception as e:
        return extract_content_simple(html, url, error=str(e))


def extract_content_simple(html: str, url: str, error: str = None) -> dict:
    """
    简化的内容提取（当 trafilatura 不可用时）
    """
    content = ""
    metadata = {"url": url}
    
    try:
        # 提取标题
        title_match = re.search(r"<title[^>]*>([^<]+)</title>", html, re.IGNORECASE)
        if title_match:
            metadata["title"] = title_match.group(1).strip()
        
        # 简单提取 body 内容
        body_match = re.search(r"<body[^>]*>(.*?)</body>", html, re.DOTALL | re.IGNORECASE)
        if body_match:
            body = body_match.group(1)
            # 移除脚本和样式
            body = re.sub(r"<script[^>]*>.*?</script>", "", body, flags=re.DOTALL | re.IGNORECASE)
            body = re.sub(r"<style[^>]*>.*?</style>", "", body, flags=re.DOTALL | re.IGNORECASE)
            # 移除 HTML 标签
            body = re.sub(r"<[^>]+>", " ", body)
            # 清理空白
            content = re.sub(r"\s+", " ", body).strip()
            # 截取前 5000 字符
            content = content[:5000]
        
        if error:
            metadata["warning"] = f"使用简化模式: {error}"
            
    except Exception as e:
        content = f"内容提取失败: {str(e)}"
    
    return {
        "content": content,
        "metadata": metadata,
        "format": "text",
    }


def extract_links(html: str, base_url: str) -> list:
    """提取页面中的链接"""
    links = []
    try:
        # 提取所有 href
        hrefs = re.findall(r'href=["\']([^"\']+)["\']', html, re.IGNORECASE)
        for href in hrefs:
            # 过滤有效链接
            if href.startswith("http"):
                links.append(href)
            elif href.startswith("/") and base_url:
                # 转换为绝对路径
                parsed = urllib.parse.urlparse(base_url)
                links.append(f"{parsed.scheme}://{parsed.netloc}{href}")
        
        # 去重
        links = list(set(links))[:50]  # 最多返回 50 个链接
    except Exception:
        pass
    
    return links


def read_single_url(
    url: str,
    output_format: str = "markdown",
    use_dynamic: bool = False,
    wait_selector: str = None,
    include_links: bool = False,
    timeout: int = DEFAULT_TIMEOUT,
) -> dict:
    """
    读取单个 URL 的内容
    
    Args:
        url: 目标 URL
        output_format: 输出格式 (markdown, json, text)
        use_dynamic: 是否使用动态渲染
        wait_selector: 等待的选择器
        include_links: 是否包含链接提取
        timeout: 超时时间（秒）
    
    Returns:
        dict: {success, content, metadata, links, error}
    """
    # 获取 HTML
    if use_dynamic:
        fetch_result = fetch_url_dynamic(url, timeout, wait_selector)
    else:
        fetch_result = fetch_url_static(url, timeout)
    
    if not fetch_result.get("success"):
        return {
            "success": False,
            "url": url,
            "error": fetch_result.get("error", "获取失败"),
        }
    
    html = fetch_result["html"]
    final_url = fetch_result.get("final_url", url)
    
    # 提取内容
    extract_result = extract_content(html, final_url, output_format)
    
    result = {
        "success": True,
        "url": final_url,
        "original_url": url,
        "content": extract_result["content"],
        "metadata": extract_result["metadata"],
        "format": extract_result["format"],
        "status_code": fetch_result.get("status_code"),
    }
    
    # 提取链接
    if include_links:
        result["links"] = extract_links(html, final_url)
    
    return result


def read_multiple_urls(
    urls: list,
    output_format: str = "markdown",
    use_dynamic: bool = False,
    include_links: bool = False,
    timeout: int = DEFAULT_TIMEOUT,
) -> dict:
    """
    批量读取多个 URL
    
    Returns:
        dict: {success, results: [{url, content, metadata, ...}], summary}
    """
    results = []
    success_count = 0
    
    for url in urls:
        result = read_single_url(
            url,
            output_format=output_format,
            use_dynamic=use_dynamic,
            include_links=include_links,
            timeout=timeout,
        )
        results.append(result)
        if result.get("success"):
            success_count += 1
    
    return {
        "success": success_count > 0,
        "results": results,
        "summary": {
            "total": len(urls),
            "success": success_count,
            "failed": len(urls) - success_count,
        },
    }


def format_output(result: dict, brief: bool = False) -> str:
    """格式化输出为可读文本"""
    if not result.get("success"):
        return f"❌ 读取失败: {result.get('url', 'unknown')}\n错误: {result.get('error', '未知错误')}"
    
    output = []
    metadata = result.get("metadata", {})
    
    # 标题
    if title := metadata.get("title"):
        output.append(f"# {title}")
        output.append("")
    
    # 元信息
    output.append(f"**URL**: {result.get('url', '')}")
    if author := metadata.get("author"):
        output.append(f"**作者**: {author}")
    if date := metadata.get("date"):
        output.append(f"**日期**: {date}")
    output.append("")
    
    # 内容
    content = result.get("content", "")
    if brief and len(content) > 2000:
        content = content[:2000] + "\n\n... (内容已截断)"
    output.append("---")
    output.append("")
    output.append(content)
    
    # 链接
    if links := result.get("links"):
        output.append("")
        output.append("---")
        output.append("")
        output.append("## 相关链接")
        for i, link in enumerate(links[:10], 1):
            output.append(f"{i}. {link}")
    
    return "\n".join(output)


def format_batch_output(result: dict) -> str:
    """格式化批量读取输出"""
    output = []
    
    summary = result.get("summary", {})
    output.append(f"## 批量读取结果")
    output.append(f"总数: {summary.get('total', 0)} | 成功: {summary.get('success', 0)} | 失败: {summary.get('failed', 0)}")
    output.append("")
    
    for i, item in enumerate(result.get("results", []), 1):
        if item.get("success"):
            metadata = item.get("metadata", {})
            output.append(f"### [{i}] {metadata.get('title', item.get('url', 'unknown'))}")
            output.append(f"**URL**: {item.get('url', '')}")
            # 显示内容摘要
            content = item.get("content", "")
            if len(content) > 500:
                content = content[:500] + "..."
            output.append(f"**内容摘要**:\n{content}")
            output.append("")
        else:
            output.append(f"### [{i}] ❌ 读取失败: {item.get('url', 'unknown')}")
            output.append(f"**错误**: {item.get('error', '未知错误')}")
            output.append("")
    
    return "\n".join(output)


@server.list_tools()
async def list_tools() -> list[Tool]:
    """列出可用的 MCP 工具"""
    return [
        Tool(
            name="read_url",
            description="""读取单个 URL 的内容，提取正文和元数据。

适用于:
- 获取文章/博客内容
- 阅读技术文档
- 提取网页信息

输出格式:
- markdown: LLM 友好的 Markdown 格式（默认）
- text: 纯文本格式
- json: JSON 格式（结构化数据）

示例:
- 读取文章: read_url(url="https://example.com/article")
- 动态页面: read_url(url="https://spa.example.com", use_dynamic=true)
- 获取链接: read_url(url="...", include_links=true)""",
            inputSchema={
                "type": "object",
                "properties": {
                    "url": {
                        "type": "string",
                        "description": "要读取的 URL 地址",
                    },
                    "format": {
                        "type": "string",
                        "description": "输出格式: markdown, text, json",
                        "enum": ["markdown", "text", "json"],
                        "default": "markdown",
                    },
                    "use_dynamic": {
                        "type": "boolean",
                        "description": "是否使用动态渲染（用于 SPA 页面）",
                        "default": False,
                    },
                    "wait_selector": {
                        "type": "string",
                        "description": "等待特定 CSS 选择器出现后再提取内容",
                    },
                    "include_links": {
                        "type": "boolean",
                        "description": "是否提取页面中的链接",
                        "default": False,
                    },
                    "brief": {
                        "type": "boolean",
                        "description": "是否返回简化版本（内容截断）",
                        "default": False,
                    },
                    "timeout": {
                        "type": "integer",
                        "description": "超时时间（秒），默认 30",
                        "default": 30,
                    },
                },
                "required": ["url"],
            },
        ),
        Tool(
            name="read_urls",
            description="""批量读取多个 URL 的内容。

适用于:
- 同时获取多个页面的内容
- 对比多个来源的信息
- 高效收集信息

示例:
- 批量读取: read_urls(urls=["url1", "url2", "url3"])""",
            inputSchema={
                "type": "object",
                "properties": {
                    "urls": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "要读取的 URL 列表",
                    },
                    "format": {
                        "type": "string",
                        "description": "输出格式",
                        "enum": ["markdown", "text", "json"],
                        "default": "markdown",
                    },
                    "use_dynamic": {
                        "type": "boolean",
                        "description": "是否使用动态渲染",
                        "default": False,
                    },
                    "include_links": {
                        "type": "boolean",
                        "description": "是否提取链接",
                        "default": False,
                    },
                },
                "required": ["urls"],
            },
        ),
        Tool(
            name="check_url",
            description="""快速检查 URL 是否可访问，返回状态信息。

适用于:
- 验证链接有效性
- 获取页面基本信息（不提取内容）
- 快速预检""",
            inputSchema={
                "type": "object",
                "properties": {
                    "url": {
                        "type": "string",
                        "description": "要检查的 URL",
                    },
                },
                "required": ["url"],
            },
        ),
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict[str, Any]) -> list[TextContent]:
    """执行工具调用"""
    
    if name == "read_url":
        # 在线程池中执行同步操作
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(
            executor,
            read_single_url,
            arguments.get("url"),
            arguments.get("format", "markdown"),
            arguments.get("use_dynamic", False),
            arguments.get("wait_selector"),
            arguments.get("include_links", False),
            arguments.get("timeout", 30),
        )
        formatted = format_output(result, brief=arguments.get("brief", False))
        return [TextContent(type="text", text=formatted)]
    
    elif name == "read_urls":
        urls = arguments.get("urls", [])
        if not urls:
            return [TextContent(type="text", text="错误: 未提供 URL 列表")]
        
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(
            executor,
            read_multiple_urls,
            urls,
            arguments.get("format", "markdown"),
            arguments.get("use_dynamic", False),
            arguments.get("include_links", False),
            30,  # timeout
        )
        formatted = format_batch_output(result)
        return [TextContent(type="text", text=formatted)]
    
    elif name == "check_url":
        url = arguments.get("url")
        # 快速检查
        fetch_result = fetch_url_static(url, timeout=10)
        
        if fetch_result.get("success"):
            output = [
                f"✅ URL 可访问",
                f"**URL**: {fetch_result.get('final_url', url)}",
                f"**状态码**: {fetch_result.get('status_code')}",
                f"**内容长度**: {len(fetch_result.get('html', ''))} 字符",
            ]
        else:
            output = [
                f"❌ URL 不可访问",
                f"**URL**: {url}",
                f"**错误**: {fetch_result.get('error', '未知错误')}",
            ]
        
        return [TextContent(type="text", text="\n".join(output))]
    
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
    # 检查依赖
    if not TRAFILATURA_AVAILABLE:
        print("提示: 安装 trafilatura 以获得更好的内容提取效果", file=sys.stderr)
        print("  pip install trafilatura", file=sys.stderr)
    
    asyncio.run(run_server())
