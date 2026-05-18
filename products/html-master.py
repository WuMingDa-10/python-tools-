#!/usr/bin/env python3
"""
HTML 处理大师 v1.0
==================
功能：HTML 解析、提取、转换、生成
售价：$12.99
"""

import os
import sys
import re
import json
from datetime import datetime

try:
    from bs4 import BeautifulSoup
except ImportError:
    import subprocess
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'beautifulsoup4'])
    from bs4 import BeautifulSoup


class HTMLMaster:
    """HTML 处理大师"""
    
    def __init__(self):
        self.soup = None
    
    def load_file(self, file_path: str) -> str:
        """加载 HTML 文件"""
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        self.soup = BeautifulSoup(content, 'html.parser')
        return content
    
    def load_string(self, content: str) -> str:
        """加载字符串"""
        self.soup = BeautifulSoup(content, 'html.parser')
        return content
    
    def extract_text(self, html: str = None) -> str:
        """提取文本"""
        if html:
            soup = BeautifulSoup(html, 'html.parser')
        else:
            soup = self.soup
        
        return soup.get_text(separator='\n', strip=True)
    
    def extract_links(self, html: str = None) -> list:
        """提取链接"""
        if html:
            soup = BeautifulSoup(html, 'html.parser')
        else:
            soup = self.soup
        
        links = []
        for a in soup.find_all('a', href=True):
            links.append({
                'text': a.get_text(strip=True),
                'href': a['href'],
            })
        return links
    
    def extract_images(self, html: str = None) -> list:
        """提取图片"""
        if html:
            soup = BeautifulSoup(html, 'html.parser')
        else:
            soup = self.soup
        
        images = []
        for img in soup.find_all('img', src=True):
            images.append({
                'src': img['src'],
                'alt': img.get('alt', ''),
            })
        return images
    
    def extract_tables(self, html: str = None) -> list:
        """提取表格"""
        if html:
            soup = BeautifulSoup(html, 'html.parser')
        else:
            soup = self.soup
        
        tables = []
        for table in soup.find_all('table'):
            rows = []
            for tr in table.find_all('tr'):
                cells = [td.get_text(strip=True) for td in tr.find_all(['td', 'th'])]
                rows.append(cells)
            tables.append(rows)
        
        return tables
    
    def extract_meta(self, html: str = None) -> dict:
        """提取 Meta 信息"""
        if html:
            soup = BeautifulSoup(html, 'html.parser')
        else:
            soup = self.soup
        
        meta = {}
        for tag in soup.find_all('meta'):
            name = tag.get('name', tag.get('property', ''))
            content = tag.get('content', '')
            if name and content:
                meta[name] = content
        
        return meta
    
    def extract_headings(self, html: str = None) -> list:
        """提取标题"""
        if html:
            soup = BeautifulSoup(html, 'html.parser')
        else:
            soup = self.soup
        
        headings = []
        for i in range(1, 7):
            for heading in soup.find_all(f'h{i}'):
                headings.append({
                    'level': i,
                    'text': heading.get_text(strip=True),
                })
        
        return headings
    
    def clean_html(self, html: str) -> str:
        """清理 HTML"""
        soup = BeautifulSoup(html, 'html.parser')
        
        # 移除脚本和样式
        for tag in soup(['script', 'style']):
            tag.decompose()
        
        return str(soup)
    
    def minify_html(self, html: str) -> str:
        """压缩 HTML"""
        # 移除注释
        html = re.sub(r'<!--.*?-->', '', html, flags=re.DOTALL)
        # 移除多余空白
        html = re.sub(r'\s+', ' ', html)
        # 移除标签间空白
        html = re.sub(r'>\s+<', '><', html)
        
        return html.strip()
    
    def html_to_markdown(self, html: str) -> str:
        """HTML 转 Markdown"""
        soup = BeautifulSoup(html, 'html.parser')
        md = ''
        
        for element in soup.children:
            if element.name == 'h1':
                md += f'# {element.get_text(strip=True)}\n\n'
            elif element.name == 'h2':
                md += f'## {element.get_text(strip=True)}\n\n'
            elif element.name == 'h3':
                md += f'### {element.get_text(strip=True)}\n\n'
            elif element.name == 'p':
                md += f'{element.get_text(strip=True)}\n\n'
            elif element.name == 'a':
                md += f'[{element.get_text(strip=True)}]({element.get("href", "")})\n\n'
            elif element.name == 'img':
                md += f'![{element.get("alt", "")}]({element.get("src", "")})\n\n'
            elif element.name == 'ul':
                for li in element.find_all('li'):
                    md += f'- {li.get_text(strip=True)}\n'
                md += '\n'
            elif element.name == 'ol':
                for i, li in enumerate(element.find_all('li'), 1):
                    md += f'{i}. {li.get_text(strip=True)}\n'
                md += '\n'
        
        return md
    
    def generate_html(self, title: str, content: str, css: str = '') -> str:
        """生成 HTML"""
        html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        {css}
    </style>
</head>
<body>
    {content}
</body>
</html>'''
        return html
    
    def save_file(self, content: str, output_file: str) -> str:
        """保存文件"""
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ 保存完成: {output_file}")
        return output_file


def main():
    """主函数"""
    print("=" * 50)
    print("HTML 处理大师 v1.0")
    print("=" * 50)
    print()
    print("功能:")
    print("  1. 提取文本/链接/图片")
    print("  2. 提取表格/Meta/标题")
    print("  3. 清理/压缩 HTML")
    print("  4. HTML 转 Markdown")
    print("  5. 生成 HTML")
    print("  6. 批量处理")
    print()
    print("使用方法:")
    print("  from html_master import HTMLMaster")
    print("  master = HTMLMaster()")
    print("  text = master.extract_text('<p>Hello</p>')")
    print("  links = master.extract_links(html_content)")
    print()
    print("价格: $12.99")


if __name__ == "__main__":
    main()
