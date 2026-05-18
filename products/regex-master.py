#!/usr/bin/env python3
"""
正则表达式大师 v1.0
===================
功能：正则测试、批量匹配、数据提取、模式生成
售价：$11.99
"""

import os
import sys
import re
import json
from datetime import datetime


class RegexMaster:
    """正则表达式大师"""
    
    def __init__(self):
        self.patterns = []
        self.matches = []
    
    def test_pattern(self, pattern: str, test_string: str) -> dict:
        """测试正则表达式"""
        try:
            match = re.search(pattern, test_string)
            return {
                'pattern': pattern,
                'test_string': test_string,
                'match': bool(match),
                'matched_text': match.group() if match else None,
                'start': match.start() if match else None,
                'end': match.end() if match else None,
            }
        except re.error as e:
            return {'error': str(e)}
    
    def find_all(self, pattern: str, text: str) -> list:
        """查找所有匹配"""
        try:
            matches = re.findall(pattern, text)
            return matches
        except re.error as e:
            return [{'error': str(e)}]
    
    def find_all_with_positions(self, pattern: str, text: str) -> list:
        """查找所有匹配（带位置）"""
        try:
            matches = []
            for match in re.finditer(pattern, text):
                matches.append({
                    'text': match.group(),
                    'start': match.start(),
                    'end': match.end(),
                    'groups': match.groups(),
                })
            return matches
        except re.error as e:
            return [{'error': str(e)}]
    
    def replace(self, pattern: str, replacement: str, text: str) -> str:
        """替换匹配"""
        try:
            return re.sub(pattern, replacement, text)
        except re.error as e:
            return f"错误: {e}"
    
    def extract_emails(self, text: str) -> list:
        """提取邮箱"""
        pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
        return self.find_all(pattern, text)
    
    def extract_phones(self, text: str) -> list:
        """提取电话号码"""
        patterns = [
            r'1[3-9]\d{9}',  # 中国手机号
            r'\d{3}-\d{8}',  # 座机
            r'\d{4}-\d{7}',  # 座机
        ]
        phones = []
        for pattern in phones:
            phones.extend(self.find_all(pattern, text))
        return phones
    
    def extract_urls(self, text: str) -> list:
        """提取 URL"""
        pattern = r'https?://[^\s<>\"{}|\\^`\[\]]+'
        return self.find_all(pattern, text)
    
    def extract_ips(self, text: str) -> list:
        """提取 IP 地址"""
        pattern = r'\b(?:\d{1,3}\.){3}\d{1,3}\b'
        return self.find_all(pattern, text)
    
    def extract_dates(self, text: str) -> list:
        """提取日期"""
        patterns = [
            r'\d{4}-\d{2}-\d{2}',
            r'\d{2}/\d{2}/\d{4}',
            r'\d{2}\.\d{2}\.\d{4}',
        ]
        dates = []
        for pattern in patterns:
            dates.extend(self.find_all(pattern, text))
        return dates
    
    def generate_pattern(self, description: str) -> str:
        """根据描述生成正则表达式"""
        patterns = {
            'email': r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}',
            'phone': r'1[3-9]\d{9}',
            'url': r'https?://[^\s<>\"{}|\\^`\[\]]+',
            'ip': r'\b(?:\d{1,3}\.){3}\d{1,3}\b',
            'date': r'\d{4}-\d{2}-\d{2}',
            'chinese': r'[\u4e00-\u9fa5]+',
            'number': r'-?\d+\.?\d*',
            'html_tag': r'<[^>]+>',
        }
        return patterns.get(description.lower(), f'无法生成: {description}')
    
    def batch_process(self, pattern: str, files: list) -> dict:
        """批量处理文件"""
        results = {}
        for file_path in files:
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                matches = self.find_all(pattern, content)
                results[file_path] = matches
            except Exception as e:
                results[file_path] = {'error': str(e)}
        return results
    
    def export_results(self, results: dict, output_file: str = 'regex_results.json') -> str:
        """导出结果"""
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        print(f"✅ 结果已导出: {output_file}")
        return output_file


def main():
    """主函数"""
    print("=" * 50)
    print("正则表达式大师 v1.0")
    print("=" * 50)
    print()
    print("功能:")
    print("  1. 正则测试")
    print("  2. 批量匹配")
    print("  3. 数据提取")
    print("  4. 模式生成")
    print("  5. 文件处理")
    print("  6. 结果导出")
    print()
    print("使用方法:")
    print("  from regex_master import RegexMaster")
    print("  master = RegexMaster()")
    print("  emails = master.extract_emails('联系我: test@example.com')")
    print()
    print("价格: $11.99")


if __name__ == "__main__":
    main()
