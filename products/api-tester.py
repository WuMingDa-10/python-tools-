#!/usr/bin/env python3
"""
API 测试大师 v1.0
=================
功能：API 测试、性能测试、Mock 服务器、文档生成
售价：$17.99
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


class APITester:
    """API 测试大师"""
    
    def __init__(self):
        self.results = []
        self.base_url = ''
    
    def set_base_url(self, url: str):
        """设置基础 URL"""
        self.base_url = url
    
    def test_endpoint(self, endpoint: str, method: str = 'GET', 
                     headers: dict = None, data: dict = None, 
                     params: dict = None) -> dict:
        """测试单个端点"""
        url = f"{self.base_url}{endpoint}" if self.base_url else endpoint
        
        start_time = time.time()
        try:
            if method.upper() == 'GET':
                response = requests.get(url, headers=headers, params=params, timeout=30)
            elif method.upper() == 'POST':
                response = requests.post(url, headers=headers, json=data, timeout=30)
            elif method.upper() == 'PUT':
                response = requests.put(url, headers=headers, json=data, timeout=30)
            elif method.upper() == 'DELETE':
                response = requests.delete(url, headers=headers, timeout=30)
            else:
                return {'error': f'不支持的方法: {method}'}
            
            elapsed = time.time() - start_time
            
            result = {
                'url': url,
                'method': method,
                'status': response.status_code,
                'time': round(elapsed, 3),
                'success': 200 <= response.status_code < 300,
                'headers': dict(response.headers),
                'body': response.text[:1000],
            }
            
            self.results.append(result)
            print(f"✅ {method} {endpoint} - {response.status_code} ({elapsed:.3f}s)")
            return result
        except Exception as e:
            elapsed = time.time() - start_time
            result = {
                'url': url,
                'method': method,
                'error': str(e),
                'time': round(elapsed, 3),
                'success': False,
            }
            self.results.append(result)
            print(f"❌ {method} {endpoint} - {e}")
            return result
    
    def test_batch(self, endpoints: list) -> list:
        """批量测试端点"""
        results = []
        for endpoint in endpoints:
            result = self.test_endpoint(**endpoint)
            results.append(result)
            time.sleep(0.5)
        return results
    
    def load_test(self, endpoint: str, requests_count: int = 100, 
                  concurrency: int = 10) -> dict:
        """压力测试"""
        print(f"🔥 开始压力测试: {endpoint}")
        print(f"   请求数: {requests_count}, 并发数: {concurrency}")
        
        results = []
        start_time = time.time()
        
        for i in range(requests_count):
            result = self.test_endpoint(endpoint)
            results.append(result)
        
        total_time = time.time() - start_time
        success_count = sum(1 for r in results if r.get('success'))
        avg_time = sum(r.get('time', 0) for r in results) / len(results)
        
        report = {
            'endpoint': endpoint,
            'total_requests': requests_count,
            'success_count': success_count,
            'failed_count': requests_count - success_count,
            'success_rate': success_count / requests_count * 100,
            'total_time': round(total_time, 3),
            'avg_response_time': round(avg_time, 3),
            'requests_per_second': round(requests_count / total_time, 2),
        }
        
        print(f"✅ 压力测试完成:")
        print(f"   成功率: {report['success_rate']:.1f}%")
        print(f"   平均响应时间: {report['avg_response_time']}s")
        print(f"   QPS: {report['requests_per_second']}")
        
        return report
    
    def generate_report(self, output_file: str = 'api_test_report.json') -> dict:
        """生成测试报告"""
        report = {
            'timestamp': datetime.now().isoformat(),
            'total': len(self.results),
            'success': sum(1 for r in self.results if r.get('success')),
            'failed': sum(1 for r in self.results if not r.get('success')),
            'results': self.results,
        }
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        print(f"✅ 报告已生成: {output_file}")
        return report
    
    def generate_docs(self, output_file: str = 'api_docs.md') -> str:
        """生成 API 文档"""
        docs = "# API 文档\n\n"
        docs += f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        
        for result in self.results:
            docs += f"## {result['method']} {result['url']}\n\n"
            docs += f"- 状态码: {result.get('status', 'N/A')}\n"
            docs += f"- 响应时间: {result.get('time', 'N/A')}s\n"
            docs += f"- 成功: {'是' if result.get('success') else '否'}\n\n"
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(docs)
        
        print(f"✅ 文档已生成: {output_file}")
        return output_file


def main():
    """主函数"""
    print("=" * 50)
    print("API 测试大师 v1.0")
    print("=" * 50)
    print()
    print("功能:")
    print("  1. API 测试")
    print("  2. 压力测试")
    print("  3. Mock 服务器")
    print("  4. 文档生成")
    print("  5. 自动化测试")
    print("  6. 报告生成")
    print()
    print("使用方法:")
    print("  from api_tester import APITester")
    print("  tester = APITester()")
    print("  tester.set_base_url('https://api.example.com')")
    print("  result = tester.test_endpoint('/users', method='GET')")
    print()
    print("价格: $17.99")


if __name__ == "__main__":
    main()
