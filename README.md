# DinoxAI Notes Skill for OpenClaw

📝 **与 DinoxAI 笔记系统深度集成的 OpenClaw Skill**

支持创建、查询、更新笔记，以及基于笔记库的 AI 问答功能。

## 📋 功能清单

| 功能模块 | 接口 | 状态 |
|---------|------|------|
| 📝 创建笔记 | Markdown 创建 | ✅ |
| 📝 创建笔记 | 带标题标签创建 | ✅ |
| 🎙️ 创建笔记 | 语音转文字 | ✅ |
| 🔍 查询笔记 | 卡片盒列表 | ✅ |
| 🔍 查询笔记 | 关键词搜索 | ✅ |
| 🔍 查询笔记 | 按 ID 查询 | ✅ |
| 🤖 AI 问答 | 文本问答 | ✅ |
| 🤖 AI 问答 | 语音问答 | ✅ |
| ✏️ 更新笔记 | 内容/标题/标签 | ✅ |

## 🚀 快速开始

### 1. 获取 API Token

登录 DinoxAI 笔记应用，在设置中找到 API Token。

### 2. 安装技能

```bash
# 克隆到 OpenClaw skills 目录
cd ~/.openclaw/skills
git clone https://github.com/irene-green/dinoxai-notes-skill.git dinoxai-notes

# 进入目录
cd dinoxai-notes

# 安装依赖
pip install -r requirements.txt
```

### 3. 配置

复制示例配置文件：
```bash
cp config/settings.example.json config/settings.json
```

编辑 `config/settings.json`，填入你的 API Token：
```json
{
  "api_token": "your-actual-api-token",
  "base_url": "https://aisdk.chatgo.pro"
}
```

或使用环境变量：
```bash
export DINOXAI_API_TOKEN="your-api-token"
export DINOXAI_BASE_URL="https://aisdk.chatgo.pro"
```

## 💻 使用方法

### 命令行使用

```bash
# 创建 Markdown 笔记
python scripts/dinoxai_notes.py create-md --content "# 今天\n\n学到了..."

# 创建带标题标签的笔记
python scripts/dinoxai_notes.py create-note \
  --title "项目想法" \
  --content "这是一个很棒的想法..." \
  --tags 工作 想法

# 搜索笔记
python scripts/dinoxai_notes.py search "关键词"

# 获取笔记详情
python scripts/dinoxai_notes.py get --id "note-id"

# AI 问答
python scripts/dinoxai_notes.py ask "我在笔记中记录过哪些 Python 内容？"

# 更新笔记
python scripts/dinoxai_notes.py update \
  --id "note-id" \
  --title "新标题" \
  --content "新内容" \
  --tags 标签1 标签2

# 获取卡片盒列表
python scripts/dinoxai_notes.py boxes
```

### 在 OpenClaw 中使用

激活 skill 后，可以直接使用自然语言：

```
用户: 帮我在 DinoxAI 创建一条笔记，内容是今天学习了 Python 的装饰器
AI: 已创建笔记，ID: xxx

用户: 搜索我笔记中关于 Python 的内容
AI: 找到 5 条相关笔记...

用户: 问一下 AI，我上周记录的项目想法有哪些？
AI: 根据您的笔记，上周记录的项目想法包括：...
```

## 🔧 API 文档

### 认证方式

所有请求需要在 Header 中携带 `Authorization`：
```http
Authorization: your-api-token
```

### 响应格式

统一响应格式：
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

### 核心端点

#### 创建笔记

**Markdown 创建**（推荐，与 flomo 兼容）
```http
POST /api/openapi/markdown/import/{token}
Content-Type: application/json

{
  "content": "# 标题\n\n正文内容"
}
```

**完整笔记创建**
```http
POST /api/openapi/createNote
Authorization: {token}
Content-Type: application/json

{
  "title": "笔记标题",
  "content": "笔记正文",
  "tags": ["标签1", "标签2"],
  "zettelboxIds": ["卡片盒ID"]
}
```

#### 查询笔记

**获取卡片盒列表**
```http
GET /api/openapi/zettelboxes
Authorization: {token}
```

**关键词搜索**
```http
POST /api/openapi/searchNotes
Authorization: {token}
Content-Type: application/json

{
  "code": "000000",
  "msg": "success",
  "content": "搜索关键词"
}
```

**按 ID 查询**
```http
GET /api/openapi/note/{noteId}
Authorization: {token}
```

#### AI 问答

**文本问答**
```http
POST /api/openapi/askai
Authorization: {token}
Content-Type: application/json

{
  "question": "问题内容"
}
```

**语音问答**
```http
POST /api/openapi/askai/audio
Authorization: {token}
Content-Type: multipart/form-data

file: [音频文件]
```

#### 更新笔记

```http
POST /api/openapi/updateNote
Authorization: {token}
Content-Type: application/json

{
  "noteId": "笔记ID",
  "contentMd": "新的 Markdown 内容",
  "tags": ["新标签1", "新标签2"],
  "title": "新标题"
}
```

## 📁 项目结构

```
dinoxai-notes-skill/
├── SKILL.md                      # 技能说明
├── README.md                     # 本文件
├── requirements.txt              # Python 依赖
├── config/
│   ├── schema.json              # 配置参数定义
│   └── settings.example.json    # 配置示例
└── scripts/
    └── dinoxai_notes.py         # API 客户端
```

## ⚙️ 配置选项

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| `api_token` | string | ✅ | - | API Token |
| `base_url` | string | ❌ | `https://aisdk.chatgo.pro` | API 基础 URL |
| `default_zettelbox_id` | string | ❌ | `""` | 默认卡片盒 ID |
| `auto_tag` | boolean | ❌ | `false` | 自动标签 |
| `response_format` | string | ❌ | `json` | 响应格式 |
| `timeout` | integer | ❌ | `30` | 超时时间（秒） |
| `language` | string | ❌ | `zh-CN` | 默认语言 |

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 许可证

MIT License

## 👤 作者

Irene Green

---

**Enjoy note-taking with AI!** 🎉
