#!/usr/bin/env python3
"""
DinoxAI Notes Skill - OpenClaw Integration
支持自然语言和 /dinox 命令调用
"""

import sys
import json
import os

# 添加脚本目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from dinoxai_notes import DinoxAINotesClient


def handle_command(args):
    """处理命令行参数"""
    if not args or args[0] in ['help', '--help', '-h']:
        show_help()
        return
    
    command = args[0]
    client = DinoxAINotesClient()
    
    try:
        if command == 'create-md':
            # /dinox create-md "内容" --tags 标签1 标签2
            content = args[1] if len(args) > 1 else ""
            tags = []
            if '--tags' in args:
                tag_idx = args.index('--tags')
                tags = args[tag_idx + 1:]
            if tags:
                content += "\n\n" + " ".join([f"#{tag}" for tag in tags])
            result = client.create_markdown_note(content)
            print(f"✅ 笔记已创建，ID: {result.get('data', {}).get('noteId', 'N/A')}")
            
        elif command == 'create':
            # /dinox create "标题" "内容" --tags 标签1 标签2
            title = args[1] if len(args) > 1 else "无标题"
            content = args[2] if len(args) > 2 else ""
            tags = []
            if '--tags' in args:
                tag_idx = args.index('--tags')
                tags = args[tag_idx + 1:]
            result = client.create_note(title, content, tags)
            print(f"✅ 笔记已创建: {title}")
            
        elif command == 'search':
            # /dinox search "关键词"
            keyword = args[1] if len(args) > 1 else ""
            result = client.search_notes(keyword)
            notes = result.get('data', [])
            print(f"🔍 找到 {len(notes)} 条相关笔记:\n")
            for note in notes[:5]:  # 只显示前5条
                print(f"  📄 {note.get('title', '无标题')} ({note.get('id', '')[:8]}...)")
            if len(notes) > 5:
                print(f"  ... 还有 {len(notes) - 5} 条")
                
        elif command == 'get':
            # /dinox get <笔记ID>
            note_id = args[1] if len(args) > 1 else ""
            result = client.get_note_by_id(note_id)
            note = result.get('data', {})
            print(f"📄 {note.get('title', '无标题')}\n")
            print(note.get('content', '无内容')[:500] + "..." if len(note.get('content', '')) > 500 else note.get('content', '无内容'))
            
        elif command == 'boxes':
            # /dinox boxes
            result = client.get_zettelboxes()
            boxes = result.get('data', [])
            print(f"📦 共有 {len(boxes)} 个卡片盒:\n")
            for box in boxes:
                print(f"  📁 {box.get('name', '未命名')} ({box.get('id', '')[:8]}...)")
                
        elif command == 'ask':
            # /dinox ask "问题"
            question = " ".join(args[1:]) if len(args) > 1 else ""
            result = client.ask_ai(question)
            answer = result.get('data', {}).get('answer', '无回答')
            print(f"🤖 AI 回答:\n{answer}")
            
        elif command == 'update':
            # /dinox update <ID> <标题> <内容> --tags 标签
            note_id = args[1] if len(args) > 1 else ""
            title = args[2] if len(args) > 2 else ""
            content = args[3] if len(args) > 3 else ""
            tags = []
            if '--tags' in args:
                tag_idx = args.index('--tags')
                tags = args[tag_idx + 1:]
            result = client.update_note(note_id, content, tags, title)
            print(f"✅ 笔记已更新: {title}")
            
        else:
            print(f"❌ 未知命令: {command}")
            show_help()
            
    except Exception as e:
        print(f"❌ 错误: {str(e)}")


def show_help():
    """显示帮助信息"""
    print("""📝 DinoxAI Notes Skill

用法: /dinox <命令> [参数]

可用命令:
  create-md <内容> [--tags 标签...]  创建 Markdown 笔记
  create <标题> <内容> [--tags ...] 创建带标题的笔记  
  search <关键词>                    搜索笔记
  get <笔记ID>                       获取笔记详情
  boxes                              列出所有卡片盒
  ask <问题>                         AI 问答
  update <ID> <标题> <内容>         更新笔记

示例:
  /dinox create-md "今天学习了 Python" --tags 学习 Python
  /dinox search "睡眠"
  /dinox ask "我记录过哪些关于减肥的方法？"
  /dinox boxes
""")


if __name__ == '__main__':
    handle_command(sys.argv[1:])
