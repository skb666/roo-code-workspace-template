# Web Reader MCP Server Dockerfile
# 基于 Python，包含 trafilatura 和 playwright

FROM python:3.11-slim

LABEL maintainer="AI Agent Tools"
LABEL description="Web Reader MCP Server - Trafilatura + Playwright"

# 设置环境变量
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PLAYWRIGHT_BROWSERS_PATH=/ms-playwright

# 使用阿里云 apt 源并安装系统依赖
RUN sed -i 's/deb.debian.org/mirrors.aliyun.com/g' /etc/apt/sources.list.d/debian.sources \
    && apt-get update && apt-get install -y --no-install-recommends \
    # 基础工具
    curl \
    wget \
    # 编译依赖
    build-essential \
    # Playwright 依赖
    libnss3 \
    libnspr4 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libcups2 \
    libdrm2 \
    libxkbcommon0 \
    libxcomposite1 \
    libxdamage1 \
    libxfixes3 \
    libxrandr2 \
    libgbm1 \
    libasound2 \
    libpango-1.0-0 \
    libcairo2 \
    # 字体支持
    fonts-wqy-zenhei \
    fonts-wqy-microhei \
    && rm -rf /var/lib/apt/lists/*

# 设置工作目录
WORKDIR /app

# 安装 Python 依赖（使用清华 pip 源）
COPY pyproject.toml .
RUN pip install --no-cache-dir -i https://pypi.tuna.tsinghua.edu.cn/simple \
    mcp>=1.0.0 trafilatura>=1.6.0 playwright>=1.40.0

# 安装 Playwright 浏览器（使用官方源）
RUN playwright install chromium --with-deps

# 复制 MCP 服务器代码
COPY mcp_server.py .

# 创建非 root 用户
RUN useradd -m -u 1000 appuser && \
    chown -R appuser:appuser /app /ms-playwright

USER appuser

# 默认命令
CMD ["python", "mcp_server.py"]
