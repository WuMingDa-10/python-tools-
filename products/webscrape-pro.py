#!/usr/bin/env python3
"""
WebScrape Pro - 高级网页抓取工具
================================
功能：
1. 智能反反爬虫
2. 动态页面渲染
3. 数据清洗导出
4. 定时抓取任务

定价：$24.99
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
import time
import random
from typing import List, Dict, Optional
from urllib.parse import urljoin, urlparse
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class WebScrapePro:
    """高级网页抓取工具"""
    
    def __init__(self, proxy: str = None, headless: bool = True):
        self.session = requests.Session()
        self.proxy = proxy
        self.headless = headless
        
        # 用户代理池
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101',
        ]
        
        if proxy:
            self.session.proxies = {'http': proxy, 'https': proxy}
    
    def _get_headers(self) -> Dict:
        """获取随机请求头"""
        return {
            'User-Agent': random.choice(self.user_agents),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
        }
    
    def scrape_page(self, url: str, selector: str = None) -> Dict:
        """抓取单个页面"""
        try:
            time.sleep(random.uniform(1, 3))  # 随机延迟
            response = self.session.get(url, headers=self._get_headers(), timeout=30)
            response.raise_for_status()
            response.encoding = response.apparent_encoding
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            result = {
                'url': url,
                'title': soup.title.string if soup.title else '',
                'status': response.status_code,
                'content': soup.get_text(separator='\n', strip=True)[:5000],
            }
            
            if selector:
                elements = soup.select(selector)
                result['selected'] = [el.get_text(strip=True) for el in elements]
            
            return result
        except Exception as e:
            logger.error(f"抓取失败 {url}: {e}")
            return {'url': url, 'error': str(e)}
    
    def scrape_links(self, url: str, filter_domain: bool = True) -> List[str]:
        """抓取页面中的所有链接"""
        try:
            response = self.session.get(url, headers=self._get_headers(), timeout=30)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            links = []
            for a in soup.find_all('a', href=True):
                link = urljoin(url, a['href'])
                if filter_domain:
                    if urlparse(link).netloc == urlparse(url).netloc:
                        links.append(link)
                else:
                    links.append(link)
            
            return list(set(links))
        except Exception as e:
            logger.error(f"抓取链接失败: {e}")
            return []
    
    def scrape_table(self, url: str, table_index: int = 0) -> pd.DataFrame:
        """抓取网页表格"""
        try:
            tables = pd.read_html(url)
            if table_index < len(tables):
                return tables[table_index]
            return pd.DataFrame()
        except Exception as e:
            logger.error(f"抓取表格失败: {e}")
            return pd.DataFrame()
    
    def scrape_pagination(self, base_url: str, pages: int, 
                          page_param: str = 'page') -> List[Dict]:
        """抓取分页数据"""
        results = []
        for page in range(1, pages + 1):
            url = f"{base_url}?{page_param}={page}"
            result = self.scrape_page(url)
            results.append(result)
            logger.info(f"完成第 {page}/{pages} 页")
        return results
    
    def scrape_with_selenium(self, url: str, wait_time: int = 5) -> Dict:
        """使用 Selenium 抓取动态页面"""
        try:
            from selenium import webdriver
            from selenium.webdriver.chrome.options import Options
            from selenium.webdriver.common.by import By
            
            options = Options()
            if self.headless:
                options.add_argument('--headless')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            
            if self.proxy:
                options.add_argument(f'--proxy-server={self.proxy}')
            
            driver = webdriver.Chrome(options=options)
            driver.get(url)
            time.sleep(wait_time)
            
            result = {
                'url': url,
                'title': driver.title,
                'content': driver.page_source,
            }
            
            driver.quit()
            return result
        except ImportError:
            logger.warning("Selenium 未安装，使用普通请求")
            return self.scrape_page(url)
        except Exception as e:
            logger.error(f"Selenium 抓取失败: {e}")
            return {'url': url, 'error': str(e)}
    
    def export_data(self, data: List[Dict], output_file: str, 
                    format: str = 'csv') -> str:
        """导出数据"""
        df = pd.DataFrame(data)
        
        if format == 'csv':
            df.to_csv(output_file, index=False, encoding='utf-8-sig')
        elif format == 'excel':
            df.to_excel(output_file, index=False)
        elif format == 'json':
            df.to_json(output_file, orient='records', force_ascii=False, indent=2)
        
        logger.info(f"数据已导出: {output_file}")
        return output_file


def scrape_ecommerce(url: str, proxy: str = None) -> List[Dict]:
    """抓取电商商品数据"""
    scraper = WebScrapePro(proxy=proxy)
    result = scraper.scrape_page(url, selector='.product-item')
    return result.get('selected', [])


def scrape_news(url: str, proxy: str = None) -> List[Dict]:
    """抓取新闻数据"""
    scraper = WebScrapePro(proxy=proxy)
    result = scraper.scrape_page(url, selector='.news-item, .article-item')
    return result.get('selected', [])


if __name__ == "__main__":
    print("WebScrape Pro - 高级网页抓取工具")
    print("=" * 40)
    print("使用方法:")
    print("  from webscrape import WebScrapePro")
    print("  scraper = WebScrapePro(proxy='http://127.0.0.1:7897')")
    print("  result = scraper.scrape_page('https://example.com')")
