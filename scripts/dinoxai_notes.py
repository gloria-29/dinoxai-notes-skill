#!/usr/bin/env python3
"""
DinoxAI Notes API Client
与 DinoxAI 笔记系统集成的 Python 客户端
"""

import requests
import json
import os
from typing import Optional, List, Dict, Any
from pathlib import Path


class DinoxAINotesClient:
    """DinoxAI 笔记 API 客户端"""
    
    def __init__(self, api_token: Optional[str] = None, base_url: Optional[str] = None):
        """
        初始化客户端
        
        Args:
            api_token: API Token，如果不提供则从环境变量或配置文件读取
            base_url: API 基础 URL
        """
        config = self._load_config()
        self.api_token = api_token or config.get('api_token', '')
        self.base_url = base_url or os.getenv('DINOXAI_BASE_URL') or config.get('base_url', 'https://aisdk.chatgo.pro')
        self.headers = {
            'Authorization': self.api_token,
            'Content-Type': 'application/json'
        }
    
    def _load_config(self) -> dict:
        """从配置文件加载配置"""
        config_path = Path(__file__).parent.parent / 'config' / 'settings.json'
        if config_path.exists():
            with open(config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}
    
    def _request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        """
        发送 HTTP 请求
        
        Args:
            method: HTTP 方法
            endpoint: API 端点
            **kwargs: 请求参数
            
        Returns:
            API 响应数据
        """
        url = f"{self.base_url}{endpoint}"
        
        if 'headers' not in kwargs:
            kwargs['headers'] = self.headers
        
        try:
            response = requests.request(method, url, **kwargs)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {
                "code": "ERROR",
                "msg": f"请求失败: {str(e)}",
                "data": None
            }
    
    # ==================== 创建笔记 ====================
    
    def create_markdown_note(self, content: str) -> Dict[str, Any]:
        """
        使用 Markdown 创建笔记（与 flomo 兼容）
        
        Args:
            content: Markdown 格式的笔记内容
            
        Returns:
            包含 noteId 的响应
        """
        endpoint = f"/api/openapi/markdown/import/{self.api_token}"
        data = {"content": content}
        return self._request('POST', endpoint, json=data)
    
    def create_note(self, title: str, content: str, tags: List[str], 
                    zettelbox_ids: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        创建带标题和标签的笔记
        
        Args:
            title: 笔记标题
            content: 笔记正文
            tags: 标签列表
            zettelbox_ids: 卡片盒 ID 列表（可选）
            
        Returns:
            API 响应
        """
        endpoint = "/api/openapi/createNote"
        data = {
            "title": title,
            "content": content,
            "tags": tags,
            "zettelboxIds": zettelbox_ids or []
        }
        return self._request('POST', endpoint, json=data)
    
    def create_text_note(self, content: str) -> Dict[str, Any]:
        """
        创建纯文本笔记（老版本接口）
        
        Args:
            content: 笔记内容
            
        Returns:
            API 响应
        """
        endpoint = "/api/openapi/text/input"
        headers = {
            'Authorization': self.api_token,
            'Content-Type': 'application/json'
        }
        data = {"content": content}
        return self._request('POST', endpoint, json=data, headers=headers)
    
    def create_voice_note(self, audio_file_path: str) -> Dict[str, Any]:
        """
        使用语音创建笔记
        
        Args:
            audio_file_path: 音频文件路径
            
        Returns:
            API 响应
        """
        endpoint = "/voice/input"
        headers = {'Authorization': self.api_token}
        
        with open(audio_file_path, 'rb') as f:
            files = {'audio': f}
            return self._request('POST', endpoint, files=files, headers=headers)
    
    # ==================== 查询笔记 ====================
    
    def get_zettelboxes(self) -> Dict[str, Any]:
        """
        获取卡片盒列表
        
        Returns:
            卡片盒列表
        """
        endpoint = "/api/openapi/zettelboxes"
        return self._request('GET', endpoint)
    
    def search_notes(self, keyword: str) -> Dict[str, Any]:
        """
        根据关键词搜索笔记
        
        Args:
            keyword: 搜索关键词
            
        Returns:
            搜索结果
        """
        endpoint = "/api/openapi/searchNotes"
        data = {
            "code": "000000",
            "msg": "success",
            "content": keyword
        }
        return self._request('POST', endpoint, json=data)
    
    def get_note_by_id(self, note_id: str) -> Dict[str, Any]:
        """
        根据 ID 获取笔记详情
        
        Args:
            note_id: 笔记 ID
            
        Returns:
            笔记详情
        """
        endpoint = f"/api/openapi/note/{note_id}"
        return self._request('GET', endpoint)
    
    # ==================== AI 问答 ====================
    
    def ask_ai(self, question: str) -> Dict[str, Any]:
        """
        AI 文本问答
        
        Args:
            question: 问题文本
            
        Returns:
            AI 回答
        """
        endpoint = "/api/openapi/askai"
        data = {"question": question}
        return self._request('POST', endpoint, json=data)
    
    def ask_ai_voice(self, audio_file_path: str) -> Dict[str, Any]:
        """
        AI 语音问答
        
        Args:
            audio_file_path: 语音文件路径
            
        Returns:
            AI 回答
        """
        endpoint = "/api/openapi/askai/audio"
        headers = {'Authorization': self.api_token}
        
        with open(audio_file_path, 'rb') as f:
            files = {'file': f}
            return self._request('POST', endpoint, files=files, headers=headers)
    
    # ==================== 更新笔记 ====================
    
    def update_note(self, note_id: str, content_md: str, 
                    tags: List[str], title: str) -> Dict[str, Any]:
        """
        更新笔记
        
        Args:
            note_id: 笔记 ID
            content_md: Markdown 内容
            tags: 标签列表
            title: 标题
            
        Returns:
            API 响应
        """
        endpoint = "/api/openapi/updateNote"
        data = {
            "noteId": note_id,
            "contentMd": content_md,
            "tags": tags,
            "title": title
        }
        return self._request('POST', endpoint, json=data)


# ==================== CLI 接口 ====================

def main():
    """命令行入口"""
    import argparse
    
    parser = argparse.ArgumentParser(description='DinoxAI 笔记 CLI')
    subparsers = parser.add_subparsers(dest='command', help='可用命令')
    
    # 创建 Markdown 笔记
    create_md = subparsers.add_parser('create-md', help='创建 Markdown 笔记')
    create_md.add_argument('--content', '-c', required=True, help='笔记内容')
    create_md.add_argument('--tags', '-t', nargs='+', help='标签列表')
    
    # 创建完整笔记
    create_note = subparsers.add_parser('create-note', help='创建带标题的笔记')
    create_note.add_argument('--title', required=True, help='标题')
    create_note.add_argument('--content', '-c', required=True, help='内容')
    create_note.add_argument('--tags', '-t', nargs='+', default=[], help='标签')
    
    # 搜索
    search = subparsers.add_parser('search', help='搜索笔记')
    search.add_argument('keyword', help='关键词')
    
    # 获取笔记
    get = subparsers.add_parser('get', help='获取笔记详情')
    get.add_argument('--id', required=True, help='笔记 ID')
    
    # 卡片盒列表
    subparsers.add_parser('boxes', help='获取卡片盒列表')
    
    # AI 问答
    ask = subparsers.add_parser('ask', help='AI 问答')
    ask.add_argument('question', help='问题')
    
    # 更新笔记
    update = subparsers.add_parser('update', help='更新笔记')
    update.add_argument('--id', required=True, help='笔记 ID')
    update.add_argument('--content', '-c', required=True, help='新内容')
    update.add_argument('--title', required=True, help='新标题')
    update.add_argument('--tags', '-t', nargs='+', default=[], help='新标签')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    client = DinoxAINotesClient()
    
    # 执行命令
    if args.command == 'create-md':
        content = args.content
        if args.tags:
            tags_str = ' '.join([f'#{tag}' for tag in args.tags])
            content = f"{content}\n\n{tags_str}"
        result = client.create_markdown_note(content)
        print(json.dumps(result, indent=2, ensure_ascii=False))
    
    elif args.command == 'create-note':
        result = client.create_note(args.title, args.content, args.tags)
        print(json.dumps(result, indent=2, ensure_ascii=False))
    
    elif args.command == 'search':
        result = client.search_notes(args.keyword)
        print(json.dumps(result, indent=2, ensure_ascii=False))
    
    elif args.command == 'get':
        result = client.get_note_by_id(args.id)
        print(json.dumps(result, indent=2, ensure_ascii=False))
    
    elif args.command == 'boxes':
        result = client.get_zettelboxes()
        print(json.dumps(result, indent=2, ensure_ascii=False))
    
    elif args.command == 'ask':
        result = client.ask_ai(args.question)
        print(json.dumps(result, indent=2, ensure_ascii=False))
    
    elif args.command == 'update':
        result = client.update_note(args.id, args.content, args.tags, args.title)
        print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == '__main__':
    main()
