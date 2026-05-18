#!/usr/bin/env python3
"""
Markdown 处理大师 v1.0
======================
功能：Markdown 解析、转换、生成、美化
售价：$11.99
"""

import os
import sys
import re
import json
from datetime import datetime


class MarkdownMaster:
    """Markdown 处理大师"""
    
    def __init__(self):
        self.content = ''
    
    def load_file(self, file_path: str) -> str:
        """加载 Markdown 文件"""
        with open(file_path, 'r', encoding='utf-8') as f:
            self.content = f.read()
        print(f"✅ 加载完成: {len(self.content)} 字符")
        return self.content
    
    def load_string(self, content: str) -> str:
        """加载字符串"""
        self.content = content
        return content
    
    def to_html(self, content: str = None) -> str:
        """转换为 HTML"""
        if content is None:
            content = self.content
        
        # 简单的 Markdown 转 HTML
        html = content
        
        # 标题
        html = re.sub(r'^### (.*$)', r'<h3>\1</h3>', html, flags=re.MULTILINE)
        html = re.sub(r'^## (.*$)', r'<h2>\1</h2>', html, flags=re.MULTILINE)
        html = re.sub(r'^# (.*$)', r'<h1>\1</h1>', html, flags=re.MULTILINE)
        
        # 粗体和斜体
        html = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', html)
        html = re.sub(r'\*(.*?)\*', r'<em>\1</em>', html)
        
        # 链接
        html = re.sub(r'\[(.*?)\]\((.*?)\)', r'<a href="\2">\1</a>', html)
        
        # 图片
        html = re.sub(r'!\[(.*?)\]\((.*?)\)', r'<img src="\2" alt="\1">', html)
        
        # 代码块
        html = re.sub(r'```(.*?)```', r'<pre><code>\1</code></pre>', html, flags=re.DOTALL)
        
        # 行内代码
        html = re.sub(r'`(.*?)`', r'<code>\1</code>', html)
        
        # 列表
        html = re.sub(r'^- (.*$)', r'<li>\1</li>', html, flags=re.MULTILINE)
        html = re.sub(r'^(\d+)\. (.*$)', r'<li>\2</li>', html, flags=re.MULTILINE)
        
        # 段落
        html = re.sub(r'\n\n', r'</p><p>', html)
        html = f'<p>{html}</p>'
        
        return html
    
    def to_plain_text(self, content: str = None) -> str:
        """转换为纯文本"""
        if content is None:
            content = self.content
        
        # 移除 Markdown 语法
        text = content
        text = re.sub(r'^#{1,6} ', '', text, flags=re.MULTILINE)
        text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)
        text = re.sub(r'\*(.*?)\*', r'\1', text)
        text = re.sub(r'\[(.*?)\]\(.*?\)', r'\1', text)
        text = re.sub(r'!\[(.*?)\]\(.*?\)', r'\1', text)
        text = re.sub(r'```.*?```', '', text, flags=re.DOTALL)
        text = re.sub(r'`(.*?)`', r'\1', text)
        
        return text
    
    def extract_headings(self, content: str = None) -> list:
        """提取标题"""
        if content is None:
            content = self.content
        
        headings = []
        for match in re.finditer(r'^(#{1,6}) (.*$)', content, re.MULTILINE):
            level = len(match.group(1))
            title = match.group(2)
            headings.append({'level': level, 'title': title})
        
        return headings
    
    def extract_links(self, content: str = None) -> list:
        """提取链接"""
        if content is None:
            content = self.content
        
        links = []
        for match in re.finditer(r'\[(.*?)\]\((.*?)\)', content):
            links.append({'text': match.group(1), 'url': match.group(2)})
        
        return links
    
    def extract_images(self, content: str = None) -> list:
        """提取图片"""
        if content is None:
            content = self.content
        
        images = []
        for match in re.finditer(r'!\[(.*?)\]\((.*?)\)', content):
            images.append({'alt': match.group(1), 'src': match.group(2)})
        
        return images
    
    def generate_toc(self, content: str = None) -> str:
        """生成目录"""
        if content is None:
            content = self.content
        
        headings = self.extract_headings(content)
        toc = []
        
        for heading in headings:
            indent = '  ' * (heading['level'] - 1)
            toc.append(f"{indent}- {heading['title']}")
        
        return '\n'.join(toc)
    
    def add_frontmatter(self, content: str = None, metadata: dict = None) -> str:
        """添加 frontmatter"""
        if content is None:
            content = self.content
        
        if metadata is None:
            metadata = {
                'title': 'Untitled',
                'date': datetime.now().strftime('%Y-%m-%d'),
                'author': 'Unknown',
            }
        
        frontmatter = '---\n'
        for key, value in metadata.items():
            frontmatter += f'{key}: {value}\n'
        frontmatter += '---\n\n'
        
        return frontmatter + content
    
    def generate_readme(self, project_name: str, description: str = '',
                       features: list = None, installation: str = '',
                       usage: str = '') -> str:
        """生成 README"""
        readme = f'# {project_name}\n\n'
        
        if description:
            readme += f'{description}\n\n'
        
        if features:
            readme += '## 功能特点\n\n'
            for feature in features:
                readme += f'- {feature}\n'
            readme += '\n'
        
        if installation:
            readme += '## 安装\n\n'
            readme += f'```bash\n{installation}\n```\n\n'
        
        if usage:
            readme += '## 使用方法\n\n'
            readme += f'```python\n{usage}\n```\n\n'
        
        return readme
    
    def generate_changelog(self, versions: list) -> str:
        """生成更新日志"""
        changelog = '# 更新日志\n\n'
        
        for version in versions:
            changelog += f'## {version["version"]} - {version["date"]}\n\n'
            for change in version.get('changes', []):
                changelog += f'- {change}\n'
            changelog += '\n'
        
        return changelog
    
    def save_file(self, content: str, output_file: str) -> str:
        """保存文件"""
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ 保存完成: {output_file}")
        return output_file
    
    def to_json(self, content: str = None) -> dict:
        """转换为 JSON 结构"""
        if content is None:
            content = self.content
        
        return {
            'content': content,
            'headings': self.extract_headings(content),
            'links': self.extract_links(content),
            'images': self.extract_images(content),
            'word_count': len(content.split()),
            'char_count': len(content),
        }


def main():
    """主函数"""
    print("=" * 50)
    print("Markdown 处理大师 v1.0")
    print("=" * 50)
    print()
    print("功能:")
    print("  1. Markdown 转 HTML")
    print("  2. 提取标题/链接/图片")
    print("  3. 生成目录")
    print("  4. 生成 README")
    print("  5. 生成更新日志")
    print("  6. 添加 frontmatter")
    print()
    print("使用方法:")
    print("  from markdown_master import MarkdownMaster")
    print("  master = MarkdownMaster()")
    print("  html = master.to_html('# Hello World')")
    print("  toc = master.generate_toc(content)")
    print()
    print("价格: $11.99")


if __name__ == "__main__":
    main()
