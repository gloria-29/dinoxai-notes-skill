---
name: dinoxai-notes
description: DinoxAI 笔记集成 - 创建、查询、更新笔记，支持 AI 问答和语音输入
version: 1.0.0
author: Irene Green
tags: [dinoxai, notes, notebook, ai, markdown, zettelkasten]
---

# DinoxAI 笔记技能

与 DinoxAI 笔记系统深度集成，支持创建、查询、更新笔记，以及 AI 问答功能。

## 功能特性

| 功能 | 描述 |
|------|------|
| 📝 **创建笔记** | 支持 Markdown、纯文本、带标题标签的完整笔记 |
| 🎙️ **语音笔记** | 录音转文字创建笔记 |
| 🔍 **查询笔记** | 关键词搜索、按 ID 查询、获取卡片盒列表 |
| 🤖 **AI 问答** | 基于笔记库的 AI 问答（文本/语音） |
| ✏️ **更新笔记** | 修改已有笔记内容、标题、标签 |
| 📦 **卡片盒** | 支持 Zettelkasten 卡片盒管理 |

## 安装

1. 克隆仓库到本地 skills 目录：
```bash
cd ~/.openclaw/skills
git clone https://github.com/irene-green/dinoxai-notes-skill.git dinoxai-notes
```

2. 安装依赖：
```bash
cd dinoxai-notes
pip install -r requirements.txt
```

3. 配置 API Token：
在 `config/settings.json` 中添加你的 DinoxAI API Token：
```json
{
  "api_token": "your-api-token-here",
  "base_url": "https://api.dinox.ai"
}
```

## 使用方法

### 创建笔记

```bash
# 使用 Markdown 创建笔记（推荐，与 flomo 兼容）
dinoxai-notes create --content "# 今天\n\n学到了..." --tags ["日记", "学习"]

# 创建带标题的完整笔记
dinoxai-notes create-note --title "项目想法" --content "内容..." --tags ["工作", "想法"]

# 语音转文字创建笔记
dinoxai-notes voice --audio /path/to/audio.mp3
```

### 查询笔记

```bash
# 关键词搜索
dinoxai-notes search "关键词"

# 按 ID 获取笔记详情
dinoxai-notes get --id "note-id"

# 列出所有卡片盒
dinoxai-notes boxes
```

### AI 问答

```bash
# 文本问答
dinoxai-notes ask "我在笔记中记录过哪些关于 Python 的内容？"

# 语音问答
dinoxai-notes ask-voice --audio /path/to/question.mp3
```

### 更新笔记

```bash
# 更新笔记内容
dinoxai-notes update --id "note-id" --content "新内容" --tags ["标签1", "标签2"]
```

## API 端点

| 端点 | 方法 | 功能 |
|------|------|------|
| `/api/openapi/markdown/import/{token}` | POST | Markdown 创建笔记 |
| `/api/openapi/createNote` | POST | 创建带标题标签的笔记 |
| `/voice/input` | POST | 语音创建笔记 |
| `/api/openapi/zettelboxes` | GET | 获取卡片盒列表 |
| `/api/openapi/searchNotes` | POST | 关键词搜索 |
| `/api/openapi/note/{id}` | GET | 按 ID 查询笔记 |
| `/api/openapi/askai` | POST | AI 文本问答 |
| `/api/openapi/askai/audio` | POST | AI 语音问答 |
| `/api/openapi/updateNote` | POST | 更新笔记 |

## 配置选项

在 `config/settings.json` 中：

```json
{
  "api_token": "your-token",
  "base_url": "https://api.dinox.ai",
  "default_zettelbox_id": "",
  "auto_tag": false,
  "response_format": "json"
}
```

## 环境变量

```bash
export DINOXAI_API_TOKEN="your-api-token"
export DINOXAI_BASE_URL="https://api.dinox.ai"
```

## 响应格式

所有 API 返回统一格式：

```json
{
  "code": "000000",
  "msg": "success",
  "data": { ... }
}
```

- `code`: "000000" 表示成功
- `msg`: 状态描述
- `data`: 实际数据

## 许可证

MIT License
