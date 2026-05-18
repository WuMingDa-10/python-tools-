#!/usr/bin/env python3
"""
JSON 处理大师 v1.0
==================
功能：JSON 解析、格式化、转换、验证、查询
售价：$10.99
"""

import os
import sys
import json
from datetime import datetime


class JSONMaster:
    """JSON 处理大师"""
    
    def __init__(self):
        self.data = None
    
    def load_file(self, file_path: str) -> dict:
        """加载 JSON 文件"""
        with open(file_path, 'r', encoding='utf-8') as f:
            self.data = json.load(f)
        print(f"✅ 加载完成: {file_path}")
        return self.data
    
    def load_string(self, json_string: str) -> dict:
        """加载 JSON 字符串"""
        self.data = json.loads(json_string)
        return self.data
    
    def format_json(self, data: dict = None, indent: int = 2) -> str:
        """格式化 JSON"""
        if data is None:
            data = self.data
        return json.dumps(data, indent=indent, ensure_ascii=False)
    
    def minify_json(self, data: dict = None) -> str:
        """压缩 JSON"""
        if data is None:
            data = self.data
        return json.dumps(data, separators=(',', ':'), ensure_ascii=False)
    
    def validate_json(self, json_string: str) -> dict:
        """验证 JSON"""
        try:
            json.loads(json_string)
            return {'valid': True, 'error': None}
        except json.JSONDecodeError as e:
            return {'valid': False, 'error': str(e)}
    
    def query_json(self, data: dict, path: str) -> any:
        """查询 JSON（类似 jq）"""
        keys = path.split('.')
        result = data
        
        for key in keys:
            if isinstance(result, dict):
                result = result.get(key)
            elif isinstance(result, list) and key.isdigit():
                result = result[int(key)]
            else:
                return None
        
        return result
    
    def merge_json(self, *files: str) -> dict:
        """合并多个 JSON 文件"""
        merged = {}
        for file_path in files:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                merged.update(data)
        return merged
    
    def json_to_csv(self, data: list, output_file: str) -> str:
        """JSON 转 CSV"""
        import csv
        
        if not data:
            return None
        
        keys = data[0].keys()
        with open(output_file, 'w', newline='', encoding='utf-8-sig') as f:
            writer = csv.DictWriter(f, fieldnames=keys)
            writer.writeheader()
            writer.writerows(data)
        
        print(f"✅ 转换完成: {output_file}")
        return output_file
    
    def csv_to_json(self, csv_file: str, output_file: str) -> str:
        """CSV 转 JSON"""
        import csv
        
        with open(csv_file, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            data = list(reader)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"✅ 转换完成: {output_file}")
        return output_file
    
    def extract_keys(self, data: dict = None, prefix: str = '') -> list:
        """提取所有键"""
        if data is None:
            data = self.data
        
        keys = []
        if isinstance(data, dict):
            for key, value in data.items():
                full_key = f"{prefix}.{key}" if prefix else key
                keys.append(full_key)
                if isinstance(value, (dict, list)):
                    keys.extend(self.extract_keys(value, full_key))
        elif isinstance(data, list):
            for i, item in enumerate(data):
                full_key = f"{prefix}[{i}]"
                keys.extend(self.extract_keys(item, full_key))
        
        return keys
    
    def filter_json(self, data: dict, key: str, value: any) -> list:
        """过滤 JSON"""
        results = []
        if isinstance(data, list):
            for item in data:
                if isinstance(item, dict) and item.get(key) == value:
                    results.append(item)
        elif isinstance(data, dict):
            if data.get(key) == value:
                results.append(data)
        return results
    
    def save_file(self, data: dict = None, output_file: str = 'output.json') -> str:
        """保存 JSON 文件"""
        if data is None:
            data = self.data
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"✅ 保存完成: {output_file}")
        return output_file


def main():
    """主函数"""
    print("=" * 50)
    print("JSON 处理大师 v1.0")
    print("=" * 50)
    print()
    print("功能:")
    print("  1. JSON 解析")
    print("  2. 格式化/压缩")
    print("  3. 验证")
    print("  4. 查询")
    print("  5. 转换")
    print("  6. 合并")
    print()
    print("使用方法:")
    print("  from json_master import JSONMaster")
    print("  master = JSONMaster()")
    print("  data = master.load_file('data.json')")
    print("  formatted = master.format_json()")
    print()
    print("价格: $10.99")


if __name__ == "__main__":
    main()
