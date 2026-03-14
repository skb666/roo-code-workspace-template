# 🤝 贡献指南

欢迎参与项目贡献！本指南帮助你快速上手项目开发。

## 📋 目录

- [开发环境设置](#开发环境设置)
- [代码规范](#代码规范)
- [提交规范](#提交规范)
- [测试要求](#测试要求)
- [问题反馈](#问题反馈)
- [联系方式](#联系方式)

---

## 🛠️ 开发环境设置

### 1. 克隆项目

```bash
git clone https://github.com/your-username/ai-agent-toolkit.git
cd ai-agent-toolkit
```

### 2. 安装依赖

```bash
# 创建 Python 虚拟环境
python3 -m venv .venv

# 激活虚拟环境
# Linux/macOS
source .venv/bin/activate
# Windows
# .venv\Scripts\activate

# 安装开发依赖
pip install -e ./mcp/searxng_mcp
pip install -e ./mcp/web_reader_mcp

# 安装开发工具
pip install pytest pytest-cov black flake8 mypy
```

### 3. 启动开发服务

```bash
# 启动 Docker 服务
docker-compose up -d

# 验证服务运行
curl http://localhost:8080/search?q=test&format=json
```

### 4. 运行测试

```bash
# 运行所有测试
pytest

# 运行测试并生成覆盖率报告
pytest --cov=mcp --cov-report=html
```

---

## 📝 代码规范

### Python 代码规范

本项目遵循以下 Python 代码规范：

- **PEP 8** - Python 官方风格指南
- **Black** - 代码格式化
- **Flake8** - 代码检查
- **MyPy** - 类型检查

```bash
# 格式化代码
black mcp/

# 检查代码
flake8 mcp/

# 类型检查
mypy mcp/
```

### 代码风格要求

```python
# ✅ 推荐：使用类型注解
def read_url(url: str, use_dynamic: bool = False) -> dict:
    """读取 URL 内容。
    
    Args:
        url: 要读取的 URL 地址
        use_dynamic: 是否使用动态渲染
        
    Returns:
        包含页面内容的字典
    """
    pass

# ✅ 推荐：使用有意义的变量名
def process_search_results(results: list[dict]) -> list[SearchResult]:
    return [SearchResult(**r) for r in results if r.get('url')]

# ❌ 避免：模糊的变量名
def proc(r):
    return [x for x in r if x.get('u')]
```

### 文档字符串规范

```python
def web_search(
    query: str,
    engines: str | None = None,
    categories: str | None = None,
    language: str = "zh-CN",
    time_range: str | None = None,
    max_results: int = 10
) -> list[SearchResult]:
    """执行网络搜索。
    
    Args:
        query: 搜索关键词，支持高级搜索语法
        engines: 搜索引擎列表，如 "bing,baidu,sogou"
        categories: 搜索类别，如 "general", "images", "news"
        language: 结果语言代码，默认 "zh-CN"
        time_range: 时间范围，可选 "day", "week", "month", "year"
        max_results: 返回结果数量，默认 10
        
    Returns:
        搜索结果列表，每个结果包含标题、URL、摘要、来源
        
    Raises:
        SearchError: 当搜索失败或无结果时
        
    Example:
        >>> results = web_search("React hooks 教程", max_results=5)
        >>> for r in results:
        ...     print(f"{r.title}: {r.url}")
    """
```

---

## 🔄 提交规范

本项目采用 [Conventional Commits](https://www.conventionalcommits.org/) 规范：

### 提交类型

| 类型 | 说明 | 示例 |
|------|------|------|
| `feat` | 新功能 | `feat(web-search): 添加学术搜索功能` |
| `fix` | Bug 修复 | `fix(web-reader): 修复动态页面超时问题` |
| `docs` | 文档更新 | `docs: 更新技能系统说明` |
| `style` | 代码格式 | `style: 使用 Black 格式化代码` |
| `refactor` | 代码重构 | `refactor: 优化搜索结果处理逻辑` |
| `test` | 测试相关 | `test: 添加 web-search 单元测试` |
| `chore` | 构建/工具 | `chore: 更新依赖版本` |

### 提交格式

```
<type>(<scope>): <subject>

<body>

<footer>
```

### 提交示例

```bash
# 新功能
git commit -m "feat(web-search): 添加微信公众号文章搜索

- 集成 sogou wechat 引擎
- 支持微信文章高级搜索语法
- 添加相关测试用例

Closes #42"

# Bug 修复
git commit -m "fix(web-reader): 修复 JavaScript 渲染超时问题

- 增加 wait_selector 参数支持
- 优化超时重试逻辑
- 添加超时错误处理

Fixes #38"

# 文档更新
git commit -m "docs: 更新技能系统文档

- 添加技能概览表格
- 补充每个技能的详细说明
- 添加技能协作关系图"
```

---

## 🧪 测试要求

### 单元测试

所有新功能必须包含单元测试：

```python
# tests/test_web_search.py
import pytest
from mcp.searxng_mcp import web_search

class TestWebSearch:
    """Web Search 功能测试"""
    
    def test_basic_search(self):
        """测试基础搜索功能"""
        results = web_search(query="Python 教程", max_results=5)
        assert len(results) <= 5
        assert all(isinstance(r, dict) for r in results)
    
    def test_search_with_engine(self):
        """测试指定搜索引擎"""
        results = web_search(
            query="React hooks",
            engines="bing,baidu",
            max_results=3
        )
        assert len(results) <= 3
    
    def test_empty_query_error(self):
        """测试空查询错误处理"""
        with pytest.raises(ValueError):
            web_search(query="")
```

### 集成测试

关键功能需要集成测试：

```python
# tests/test_integration.py
class TestSearchReadFlow:
    """搜索 - 阅读集成测试"""
    
    def test_search_then_read(self):
        """测试搜索后阅读的完整流程"""
        # 1. 搜索
        search_results = web_search(query="Python 官方文档", max_results=3)
        assert len(search_results) > 0
        
        # 2. 阅读第一个结果
        if search_results:
            content = read_url(url=search_results[0]['url'])
            assert 'content' in content
            assert len(content['content']) > 0
```

### 运行测试

```bash
# 运行所有测试
pytest

# 运行特定测试文件
pytest tests/test_web_search.py

# 运行测试并显示覆盖率
pytest --cov=mcp --cov-report=term-missing

# 运行测试并生成 HTML 报告
pytest --cov=mcp --cov-report=html
open htmlcov/index.html
```

---

## 🐛 问题反馈

### 报告 Bug

发现 Bug 时，请在 GitHub Issues 中创建 Issue，并提供以下信息：

```markdown
**问题描述**
简要描述问题现象

**复现步骤**
1. 执行步骤 1
2. 执行步骤 2
3. 观察到错误

**预期行为**
应该发生什么

**实际行为**
实际发生了什么

**环境信息**
- OS: macOS 14.0 / Ubuntu 22.04 / Windows 11
- Python: 3.11.5
- Docker: 24.0.6
- 相关版本号

**日志/截图**
如有错误日志或截图，请附上
```

### 功能请求

欢迎提出新功能建议！请创建 Feature Request Issue，包含：

```markdown
**功能描述**
清晰描述想要的功能

**使用场景**
这个功能解决什么问题

**实现建议**
如有实现思路，可以提出建议

**替代方案**
是否考虑过其他实现方式
```

### 联系方式

- 📧 Email: your-email@example.com
- 💬 GitHub Discussions: [项目讨论区](https://github.com/your-username/ai-agent-toolkit/discussions)
- 🐛 Bug 报告: [GitHub Issues](https://github.com/your-username/ai-agent-toolkit/issues)

---

## 🔗 相关文档

- [返回 README.md](../README.md) - 项目主文档
- [SKILLS.md](../SKILLS.md) - 技能系统详细文档
- [.roo/skills/](.roo/skills/) - 技能源代码目录

---
> **提示**：在提交 Pull Request 前，请确保：
> 1. ✅ 所有测试通过
> 2. ✅ 代码符合规范
> 3. ✅ 已添加相关测试
> 4. ✅ 已更新文档