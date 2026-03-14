# SearXNG MCP Server Dockerfile
# 轻量级镜像，仅需要 mcp 依赖

FROM python:3.11-slim

LABEL maintainer="AI Agent Tools"
LABEL description="SearXNG MCP Server - Web Search"

# 设置环境变量
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 使用阿里云 apt 源
RUN sed -i 's/deb.debian.org/mirrors.aliyun.com/g' /etc/apt/sources.list.d/debian.sources \
    && apt-get update

# 设置工作目录
WORKDIR /app

# 安装 Python 依赖（使用清华 pip 源）
COPY pyproject.toml .
RUN pip install --no-cache-dir -i https://pypi.tuna.tsinghua.edu.cn/simple mcp>=1.0.0

# 复制 MCP 服务器代码
COPY mcp_server.py .

# 创建非 root 用户
RUN useradd -m -u 1000 appuser && \
    chown -R appuser:appuser /app

USER appuser

# 环境变量（可通过 docker-compose 覆盖）
ENV SEARXNG_BASE_URL=http://searxng:8080

# 默认命令
CMD ["python", "mcp_server.py"]
