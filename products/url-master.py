#!/usr/bin/env python3
"""
URL 处理大师 v1.0
=================
功能：URL 编码/解码、解析、验证、批量处理
售价：$7.99
"""

import os
import sys
import re
import json
from datetime import datetime
from urllib.parse import quote, unquote, urlparse, parse_qs, urlencode


class URLMaster:
    """URL 处理大师"""
    
    def __init__(self):
        self.processed = 0
    
    def encode_url(self, url: str) -> str:
        """编码 URL"""
        return quote(url, safe='')
    
    def decode_url(self, encoded: str) -> str:
        """解码 URL"""
        return unquote(encoded)
    
    def encode_component(self, component: str) -> str:
        """编码 URL 组件"""
        return quote(component, safe='')
    
    def decode_component(self, encoded: str) -> str:
        """解码 URL 组件"""
        return unquote(encoded)
    
    def parse_url(self, url: str) -> dict:
        """解析 URL"""
        parsed = urlparse(url)
        
        return {
            'scheme': parsed.scheme,
            'netloc': parsed.netloc,
            'path': parsed.path,
            'params': parsed.params,
            'query': parsed.query,
            'fragment': parsed.fragment,
            'hostname': parsed.hostname,
            'port': parsed.port,
        }
    
    def parse_query_string(self, query: str) -> dict:
        """解析查询字符串"""
        return parse_qs(query)
    
    def build_url(self, base: str, path: str = '', params: dict = None) -> str:
        """构建 URL"""
        url = base.rstrip('/')
        
        if path:
            url += '/' + path.lstrip('/')
        
        if params:
            url += '?' + urlencode(params)
        
        return url
    
    def validate_url(self, url: str) -> dict:
        """验证 URL"""
        try:
            result = urlparse(url)
            valid = all([result.scheme, result.netloc])
            return {
                'url': url,
                'valid': valid,
                'scheme': result.scheme,
                'netloc': result.netloc,
            }
        except Exception as e:
            return {'url': url, 'valid': False, 'error': str(e)}
    
    def extract_urls(self, text: str) -> list:
        """从文本中提取 URL"""
        pattern = r'https?://[^\s<>\"{}|\\^`\[\]]+'
        return re.findall(pattern, text)
    
    def normalize_url(self, url: str) -> str:
        """规范化 URL"""
        parsed = urlparse(url)
        
        # 确保有 scheme
        if not parsed.scheme:
            url = 'https://' + url
            parsed = urlparse(url)
        
        # 移除默认端口
        netloc = parsed.netloc
        if ':80' in netloc and parsed.scheme == 'http':
            netloc = netloc.replace(':80', '')
        elif ':443' in netloc and parsed.scheme == 'https':
            netloc = netloc.replace(':443', '')
        
        # 移除尾部斜杠
        path = parsed.path.rstrip('/')
        if not path:
            path = '/'
        
        return f"{parsed.scheme}://{netloc}{path}"
    
    def add_params(self, url: str, params: dict) -> str:
        """添加查询参数"""
        parsed = urlparse(url)
        existing_params = parse_qs(parsed.query)
        existing_params.update(params)
        
        new_query = urlencode(existing_params, doseq=True)
        return f"{parsed.scheme}://{parsed.netloc}{parsed.path}?{new_query}"
    
    def remove_params(self, url: str, params: list) -> str:
        """移除查询参数"""
        parsed = urlparse(url)
        existing_params = parse_qs(parsed.query)
        
        for param in params:
            existing_params.pop(param, None)
        
        new_query = urlencode(existing_params, doseq=True)
        return f"{parsed.scheme}://{parsed.netloc}{parsed.path}?{new_query}"
    
    def batch_process(self, urls: list, operation: str = 'validate') -> list:
        """批量处理"""
        results = []
        
        for url in urls:
            if operation == 'validate':
                result = self.validate_url(url)
            elif operation == 'parse':
                result = self.parse_url(url)
            elif operation == 'normalize':
                result = {'url': url, 'normalized': self.normalize_url(url)}
            elif operation == 'encode':
                result = {'url': url, 'encoded': self.encode_url(url)}
            else:
                result = {'url': url, 'error': f'未知操作: {operation}'}
            
            results.append(result)
            self.processed += 1
        
        print(f"✅ 批量处理完成: {len(results)} 个 URL")
        return results
    
    def export_results(self, results: list, output_file: str = 'url_results.json') -> str:
        """导出结果"""
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        
        print(f"✅ 结果已导出: {output_file}")
        return output_file


def main():
    """主函数"""
    print("=" * 50)
    print("URL 处理大师 v1.0")
    print("=" * 50)
    print()
    print("功能:")
    print("  1. URL 编码/解码")
    print("  2. URL 解析")
    print("  3. URL 验证")
    print("  4. URL 构建")
    print("  5. 提取 URL")
    print("  6. 批量处理")
    print()
    print("使用方法:")
    print("  from url_master import URLMaster")
    print("  master = URLMaster()")
    print("  parsed = master.parse_url('https://example.com/path?param=value')")
    print("  encoded = master.encode_url('https://example.com/路径')")
    print()
    print("价格: $7.99")


if __name__ == "__main__":
    main()
