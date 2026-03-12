# 项目初始化状态模板

## 使用说明

在开始一个复杂项目时，创建以下文件结构来支持增量执行和状态恢复。

---

## 目录结构

```
.roo/
├── project-state/
│   ├── context.md           # 项目上下文摘要
│   ├── decisions.md         # 架构决策记录
│   ├── feature-status.json  # 功能完成状态
│   └── session-log.md       # 会话日志
```

---

## context.md 模板

```markdown
# 项目上下文

## 项目概览

- **项目名称**：[项目名]
- **开始时间**：[日期]
- **目标**：[一句话描述项目目标]

## 技术栈

- 前端：[技术]
- 后端：[技术]
- 数据库：[技术]
- 其他：[技术]

## 项目结构

```
[项目根目录]/
├── src/           # 源代码
├── tests/         # 测试
├── docs/          # 文档
└── .roo/          # Roo 状态文件
```

## 核心约束

1. [约束1]
2. [约束2]
3. [约束3]

## 关键依赖

| 依赖 | 版本 | 用途 |
|------|------|------|
| xxx | x.x.x | xxx |

## 快速启动

```bash
# 安装依赖
[命令]

# 启动开发服务器
[命令]

# 运行测试
[命令]
```

## 已完成工作摘要

### [日期]
- 完成了什么
- 关键决策

### [日期]
- 完成了什么
- 关键决策

## 当前状态

- **进度**：[百分比或阶段]
- **下一步**：[下一个任务]
- **阻塞**：[当前阻塞项，如果有]
```

---

## decisions.md 模板

```markdown
# 架构决策记录 (ADR)

## ADR-001: [决策标题]

**日期**：[日期]
**状态**：[提议/已采纳/已废弃/已替代]

### 背景

[描述背景和问题]

### 决策

[描述决策]

### 理由

[为什么做这个决策]

### 替代方案

[考虑过但未采用的方案]

### 后果

[决策的影响]

---

## ADR-002: [决策标题]

...

---

## 决策索引

| ID | 标题 | 状态 | 日期 |
|----|------|------|------|
| ADR-001 | xxx | 已采纳 | 2026-03-11 |
```

---

## feature-status.json 模板

```json
{
  "project": "项目名称",
  "version": "1.0.0",
  "last_updated": "2026-03-11T00:00:00Z",
  "summary": {
    "total": 0,
    "completed": 0,
    "in_progress": 0,
    "pending": 0,
    "blocked": 0
  },
  "features": [
    {
      "id": "F001",
      "priority": "high",
      "category": "core",
      "description": "功能描述",
      "details": "详细说明",
      "steps": [
        "验证步骤1",
        "验证步骤2",
        "验证步骤3"
      ],
      "passes": false,
      "verified_by": null,
      "verified_at": null,
      "notes": "",
      "dependencies": [],
      "blocked_by": null
    }
  ],
  "categories": {
    "core": "核心功能",
    "api": "API 相关",
    "ui": "用户界面",
    "auth": "认证授权",
    "data": "数据处理",
    "infra": "基础设施"
  },
  "priorities": {
    "critical": "必须完成，阻塞其他功能",
    "high": "重要功能",
    "medium": "常规功能",
    "low": "可选功能"
  }
}
```

---

## session-log.md 模板

```markdown
# 会话日志

## 项目信息

- **项目名称**：[项目名]
- **开始时间**：[日期]
- **目标**：[项目目标]

---

## 会话记录

### Session #1 - [日期] [时间]

**目标**：[本次会话目标]

**完成情况**：
- [x] 已完成项
- [x] 已完成项
- [ ] 未完成项

**关键决策**：
- 决策1
- 决策2

**遇到的问题**：
1. 问题1 → 解决方案1
2. 问题2 → 解决方案2

**下一步**：
- 下一个任务1
- 下一个任务2

**Git 提交**：
- `commit_type(scope): 描述` (commit_hash)

---

### Session #0 - [日期] [时间]

**目标**：项目初始化

**完成情况**：
- [x] 创建项目结构
- [x] 初始化状态文件

**关键决策**：
- 初始化项目状态管理结构

---

## 统计

- 总会话数：1
- 总提交数：0
- 已完成功能：0
- 待完成功能：0
```

---

## 初始化脚本模板 (init.sh)

```bash
#!/bin/bash

# 项目初始化脚本
# 用于在新会话中快速恢复项目状态

set -e

echo "=== 项目初始化 ==="

# 1. 检查依赖
echo "检查依赖..."
# [依赖检查命令]

# 2. 安装依赖
echo "安装依赖..."
# [安装命令]

# 3. 启动服务
echo "启动开发服务器..."
# [启动命令]

# 4. 运行基本测试
echo "运行基本测试..."
# [测试命令]

echo "=== 初始化完成 ==="
```

---

## 快速初始化命令

在开始一个新项目时，运行以下命令创建状态文件：

```bash
# 创建目录结构
mkdir -p .roo/project-state

# 创建初始文件
touch .roo/project-state/context.md
touch .roo/project-state/decisions.md
touch .roo/project-state/feature-status.json
touch .roo/project-state/session-log.md

# 设置权限（如果需要）
chmod +x init.sh
```

---

## 注意事项

1. **feature-status.json 使用 JSON 格式**
   - 模型对 JSON 格式的误改风险较低
   - 便于程序化处理

2. **每次会话结束更新所有文件**
   - context.md 更新已完成工作
   - decisions.md 记录新决策
   - feature-status.json 更新功能状态
   - session-log.md 添加会话记录

3. **Git 提交包含状态文件**
   - 每次提交都应该包含更新的状态文件
   - 便于追溯历史

4. **使用清晰的 ID 命名**
   - 功能：F001, F002, ...
   - 决策：ADR-001, ADR-002, ...
   - 便于交叉引用
