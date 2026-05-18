#!/usr/bin/env python3
"""
文本处理大师 v1.0
=================
功能：文本清洗、格式转换、统计分析、批量处理
售价：$11.99
"""

import os
import sys
import re
import json
from datetime import datetime
from collections import Counter


class TextMaster:
    """文本处理大师"""
    
    def __init__(self):
        self.text = ''
        self.lines = []
    
    def load_file(self, file_path: str, encoding: str = 'utf-8') -> str:
        """加载文本文件"""
        with open(file_path, 'r', encoding=encoding, errors='ignore') as f:
            self.text = f.read()
            self.lines = self.text.split('\n')
        print(f"✅ 加载完成: {len(self.text)} 字符, {len(self.lines)} 行")
        return self.text
    
    def load_string(self, text: str) -> str:
        """加载字符串"""
        self.text = text
        self.lines = text.split('\n')
        return text
    
    def clean_text(self, text: str = None) -> str:
        """清洗文本"""
        if text is None:
            text = self.text
        
        # 去除多余空白
        text = re.sub(r'\s+', ' ', text)
        # 去除首尾空白
        text = text.strip()
        # 去除特殊字符
        text = re.sub(r'[^\w\s\u4e00-\u9fa5.,!?;:]', '', text)
        
        return text
    
    def remove_duplicates(self, text: str = None) -> str:
        """去除重复行"""
        if text is None:
            text = self.text
        
        lines = text.split('\n')
        unique_lines = list(dict.fromkeys(lines))
        return '\n'.join(unique_lines)
    
    def sort_lines(self, text: str = None, reverse: bool = False) -> str:
        """排序行"""
        if text is None:
            text = self.text
        
        lines = text.split('\n')
        lines.sort(reverse=reverse)
        return '\n'.join(lines)
    
    def extract_emails(self, text: str = None) -> list:
        """提取邮箱"""
        if text is None:
            text = self.text
        
        pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
        return re.findall(pattern, text)
    
    def extract_urls(self, text: str = None) -> list:
        """提取 URL"""
        if text is None:
            text = self.text
        
        pattern = r'https?://[^\s<>\"{}|\\^`\[\]]+'
        return re.findall(pattern, text)
    
    def extract_phones(self, text: str = None) -> list:
        """提取电话号码"""
        if text is None:
            text = self.text
        
        pattern = r'1[3-9]\d{9}'
        return re.findall(pattern, text)
    
    def extract_chinese(self, text: str = None) -> list:
        """提取中文"""
        if text is None:
            text = self.text
        
        pattern = r'[\u4e00-\u9fa5]+'
        return re.findall(pattern, text)
    
    def count_words(self, text: str = None) -> dict:
        """统计词频"""
        if text is None:
            text = self.text
        
        # 简单分词（按空格和标点）
        words = re.findall(r'\w+', text.lower())
        return dict(Counter(words).most_common(100))
    
    def count_chars(self, text: str = None) -> dict:
        """统计字符频率"""
        if text is None:
            text = self.text
        
        return dict(Counter(text).most_common(100))
    
    def get_statistics(self, text: str = None) -> dict:
        """获取统计信息"""
        if text is None:
            text = self.text
        
        lines = text.split('\n')
        words = re.findall(r'\w+', text)
        chars = len(text)
        
        return {
            'characters': chars,
            'words': len(words),
            'lines': len(lines),
            'sentences': len(re.findall(r'[.!?。！？]', text)),
            'paragraphs': len([l for l in lines if l.strip()]),
        }
    
    def replace_text(self, old: str, new: str, text: str = None) -> str:
        """替换文本"""
        if text is None:
            text = self.text
        
        return text.replace(old, new)
    
    def regex_replace(self, pattern: str, replacement: str, text: str = None) -> str:
        """正则替换"""
        if text is None:
            text = self.text
        
        return re.sub(pattern, replacement, text)
    
    def to_uppercase(self, text: str = None) -> str:
        """转大写"""
        if text is None:
            text = self.text
        return text.upper()
    
    def to_lowercase(self, text: str = None) -> str:
        """转小写"""
        if text is None:
            text = self.text
        return text.lower()
    
    def to_title(self, text: str = None) -> str:
        """转标题"""
        if text is None:
            text = self.text
        return text.title()
    
    def save_file(self, text: str, output_file: str, encoding: str = 'utf-8') -> str:
        """保存文件"""
        with open(output_file, 'w', encoding=encoding) as f:
            f.write(text)
        print(f"✅ 保存完成: {output_file}")
        return output_file
    
    def batch_process(self, input_dir: str, output_dir: str, operation: str = 'clean') -> list:
        """批量处理"""
        os.makedirs(output_dir, exist_ok=True)
        output_files = []
        
        for filename in os.listdir(input_dir):
            if filename.endswith('.txt'):
                input_path = os.path.join(input_dir, filename)
                output_path = os.path.join(output_dir, filename)
                
                with open(input_path, 'r', encoding='utf-8', errors='ignore') as f:
                    text = f.read()
                
                if operation == 'clean':
                    processed = self.clean_text(text)
                elif operation == 'dedup':
                    processed = self.remove_duplicates(text)
                elif operation == 'sort':
                    processed = self.sort_lines(text)
                else:
                    processed = text
                
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(processed)
                
                output_files.append(output_path)
        
        print(f"✅ 批量处理完成: {len(output_files)} 个文件")
        return output_files


def main():
    """主函数"""
    print("=" * 50)
    print("文本处理大师 v1.0")
    print("=" * 50)
    print()
    print("功能:")
    print("  1. 文本清洗")
    print("  2. 去重/排序")
    print("  3. 数据提取")
    print("  4. 统计分析")
    print("  5. 批量处理")
    print("  6. 格式转换")
    print()
    print("使用方法:")
    print("  from text_master import TextMaster")
    print("  master = TextMaster()")
    print("  text = master.load_file('input.txt')")
    print("  cleaned = master.clean_text()")
    print()
    print("价格: $11.99")


if __name__ == "__main__":
    main()
