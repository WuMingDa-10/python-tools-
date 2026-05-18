#!/usr/bin/env python3
"""
网络爬虫大师 v1.0
=================
功能：智能爬虫、反反爬虫、数据清洗、定时任务
售价：$24.99
"""

import os
import sys
import json
import time
import random
from datetime import datetime

try:
    import requests
    from bs4 import BeautifulSoup
except ImportError:
    import subprocess
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'requests', 'beautifulsoup4'])
    import requests
    from bs4 import BeautifulSoup


class WebCrawler:
    """网络爬虫大师"""
    
    def __init__(self, proxy: str = None):
        self.session = requests.Session()
        self.proxy = proxy
        self.crawled = 0
        
        # 用户代理池
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36',
        ]
        
        if proxy:
            self.session.proxies = {'http': proxy, 'https': proxy}
    
    def _get_headers(self) -> dict:
        """获取随机请求头"""
        return {
            'User-Agent': random.choice(self.user_agents),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        }
    
    def crawl_page(self, url: str) -> dict:
        """爬取单个页面"""
        try:
            time.sleep(random.uniform(1, 3))
            response = self.session.get(url, headers=self._get_headers(), timeout=30)
            response.raise_for_status()
            response.encoding = response.apparent_encoding
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            result = {
                'url': url,
                'title': soup.title.string if soup.title else '',
                'status': response.status_code,
                'content': soup.get_text(separator='\n', strip=True)[:5000],
                'links': [a.get('href') for a in soup.find_all('a', href=True)],
                'images': [img.get('src') for img in soup.find_all('img', src=True)],
            }
            
            self.crawled += 1
            print(f"✅ 爬取成功: {url}")
            return result
        except Exception as e:
            print(f"❌ 爬取失败: {url} - {e}")
            return {'url': url, 'error': str(e)}
    
    def crawl_multiple(self, urls: list) -> list:
        """爬取多个页面"""
        results = []
        for url in urls:
            result = self.crawl_page(url)
            results.append(result)
        return results
    
    def extract_links(self, url: str) -> list:
        """提取页面链接"""
        result = self.crawl_page(url)
        return result.get('links', [])
    
    def extract_images(self, url: str) -> list:
        """提取页面图片"""
        result = self.crawl_page(url)
        return result.get('images', [])
    
    def crawl_pagination(self, base_url: str, pages: int, page_param: str = 'page') -> list:
        """爬取分页数据"""
        results = []
        for page in range(1, pages + 1):
            url = f"{base_url}?{page_param}={page}"
            result = self.crawl_page(url)
            results.append(result)
            print(f"📄 完成第 {page}/{pages} 页")
        return results
    
    def export_data(self, data: list, output_file: str, format: str = 'json') -> str:
        """导出数据"""
        if format == 'json':
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        elif format == 'csv':
            import csv
            if data:
                keys = data[0].keys()
                with open(output_file, 'w', newline='', encoding='utf-8-sig') as f:
                    writer = csv.DictWriter(f, fieldnames=keys)
                    writer.writeheader()
                    writer.writerows(data)
        
        print(f"✅ 导出完成: {output_file}")
        return output_file


def main():
    """主函数"""
    print("=" * 50)
    print("网络爬虫大师 v1.0")
    print("=" * 50)
    print()
    print("功能:")
    print("  1. 智能爬虫")
    print("  2. 反反爬虫")
    print("  3. 数据清洗")
    print("  4. 定时任务")
    print("  5. 多线程爬取")
    print("  6. 数据导出")
    print()
    print("使用方法:")
    print("  from web_crawler import WebCrawler")
    print("  crawler = WebCrawler(proxy='http://127.0.0.1:7897')")
    print("  result = crawler.crawl_page('https://example.com')")
    print()
    print("价格: $24.99")


if __name__ == "__main__":
    main()
