#!/usr/bin/env python3
"""
网络请求大师 v1.0
=================
功能：HTTP 请求、批量下载、爬虫、API 测试
售价：$14.99
"""

import os
import sys
import json
import time
from datetime import datetime

try:
    import requests
except ImportError:
    import subprocess
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'requests'])
    import requests


class HTTPMaster:
    """网络请求大师"""
    
    def __init__(self, proxy: str = None):
        self.session = requests.Session()
        self.proxy = proxy
        
        if proxy:
            self.session.proxies = {'http': proxy, 'https': proxy}
    
    def get(self, url: str, params: dict = None, headers: dict = None) -> dict:
        """GET 请求"""
        try:
            response = self.session.get(url, params=params, headers=headers, timeout=30)
            return {
                'status': response.status_code,
                'headers': dict(response.headers),
                'content': response.text,
                'json': response.json() if 'json' in response.headers.get('content-type', '') else None,
            }
        except Exception as e:
            return {'error': str(e)}
    
    def post(self, url: str, data: dict = None, json_data: dict = None, 
             headers: dict = None) -> dict:
        """POST 请求"""
        try:
            response = self.session.post(url, data=data, json=json_data, 
                                        headers=headers, timeout=30)
            return {
                'status': response.status_code,
                'headers': dict(response.headers),
                'content': response.text,
                'json': response.json() if 'json' in response.headers.get('content-type', '') else None,
            }
        except Exception as e:
            return {'error': str(e)}
    
    def download_file(self, url: str, output_file: str) -> str:
        """下载文件"""
        try:
            response = self.session.get(url, stream=True, timeout=60)
            response.raise_for_status()
            
            with open(output_file, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            file_size = os.path.getsize(output_file)
            print(f"✅ 下载完成: {output_file} ({file_size / 1024:.1f} KB)")
            return output_file
        except Exception as e:
            print(f"❌ 下载失败: {e}")
            return None
    
    def batch_download(self, urls: list, output_dir: str) -> list:
        """批量下载"""
        os.makedirs(output_dir, exist_ok=True)
        output_files = []
        
        for url in urls:
            filename = os.path.basename(url)
            output_file = os.path.join(output_dir, filename)
            result = self.download_file(url, output_file)
            if result:
                output_files.append(result)
        
        print(f"✅ 批量下载完成: {len(output_files)} 个文件")
        return output_files
    
    def check_url(self, url: str) -> dict:
        """检查 URL 状态"""
        try:
            response = self.session.head(url, timeout=10)
            return {
                'url': url,
                'status': response.status_code,
                'content_type': response.headers.get('content-type'),
                'content_length': response.headers.get('content-length'),
            }
        except Exception as e:
            return {'url': url, 'error': str(e)}
    
    def get_headers(self, url: str) -> dict:
        """获取响应头"""
        try:
            response = self.session.head(url, timeout=10)
            return dict(response.headers)
        except Exception as e:
            return {'error': str(e)}
    
    def test_speed(self, url: str, size: int = 1024*1024) -> dict:
        """测试下载速度"""
        try:
            start_time = time.time()
            response = self.session.get(url, timeout=60)
            elapsed = time.time() - start_time
            
            content_length = len(response.content)
            speed = content_length / elapsed / 1024  # KB/s
            
            return {
                'url': url,
                'size': content_length,
                'time': elapsed,
                'speed_kbps': speed,
            }
        except Exception as e:
            return {'error': str(e)}


def main():
    """主函数"""
    print("=" * 50)
    print("网络请求大师 v1.0")
    print("=" * 50)
    print()
    print("功能:")
    print("  1. HTTP 请求")
    print("  2. 文件下载")
    print("  3. 批量下载")
    print("  4. URL 检查")
    print("  5. 速度测试")
    print("  6. 代理支持")
    print()
    print("使用方法:")
    print("  from http_master import HTTPMaster")
    print("  master = HTTPMaster(proxy='http://127.0.0.1:7897')")
    print("  result = master.get('https://api.github.com')")
    print()
    print("价格: $14.99")


if __name__ == "__main__":
    main()
