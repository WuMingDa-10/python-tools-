#!/usr/bin/env python3
"""
文件哈希大师 v1.0
=================
功能：哈希计算、文件校验、批量计算、哈希比较
售价：$8.99
"""

import os
import sys
import hashlib
import json
from datetime import datetime


class HashMaster:
    """文件哈希大师"""
    
    def __init__(self):
        self.results = []
    
    def hash_string(self, text: str, algorithm: str = 'sha256') -> str:
        """计算字符串哈希"""
        hasher = hashlib.new(algorithm)
        hasher.update(text.encode('utf-8'))
        return hasher.hexdigest()
    
    def hash_file(self, file_path: str, algorithm: str = 'sha256') -> str:
        """计算文件哈希"""
        hasher = hashlib.new(algorithm)
        
        with open(file_path, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b''):
                hasher.update(chunk)
        
        return hasher.hexdigest()
    
    def hash_file_multiple(self, file_path: str) -> dict:
        """计算文件多种哈希"""
        algorithms = ['md5', 'sha1', 'sha256', 'sha512']
        results = {}
        
        for algorithm in algorithms:
            results[algorithm] = self.hash_file(file_path, algorithm)
        
        return results
    
    def batch_hash(self, input_dir: str, algorithm: str = 'sha256') -> list:
        """批量计算哈希"""
        results = []
        
        for filename in os.listdir(input_dir):
            file_path = os.path.join(input_dir, filename)
            if os.path.isfile(file_path):
                hash_value = self.hash_file(file_path, algorithm)
                results.append({
                    'filename': filename,
                    'hash': hash_value,
                    'algorithm': algorithm,
                })
        
        self.results.extend(results)
        print(f"✅ 批量计算完成: {len(results)} 个文件")
        return results
    
    def verify_hash(self, file_path: str, expected_hash: str, 
                    algorithm: str = 'sha256') -> dict:
        """校验哈希"""
        actual_hash = self.hash_file(file_path, algorithm)
        
        return {
            'file': file_path,
            'expected': expected_hash,
            'actual': actual_hash,
            'match': actual_hash == expected_hash,
        }
    
    def compare_files(self, file1: str, file2: str) -> dict:
        """比较两个文件"""
        hash1 = self.hash_file(file1)
        hash2 = self.hash_file(file2)
        
        return {
            'file1': file1,
            'file2': file2,
            'hash1': hash1,
            'hash2': hash2,
            'identical': hash1 == hash2,
        }
    
    def find_duplicates(self, input_dir: str) -> dict:
        """查找重复文件"""
        hash_map = {}
        
        for filename in os.listdir(input_dir):
            file_path = os.path.join(input_dir, filename)
            if os.path.isfile(file_path):
                hash_value = self.hash_file(file_path)
                
                if hash_value not in hash_map:
                    hash_map[hash_value] = []
                hash_map[hash_value].append(file_path)
        
        # 过滤出重复的
        duplicates = {k: v for k, v in hash_map.items() if len(v) > 1}
        
        print(f"✅ 查找完成: 发现 {len(duplicates)} 组重复文件")
        return duplicates
    
    def generate_checksum_file(self, input_dir: str, output_file: str, 
                               algorithm: str = 'sha256') -> str:
        """生成校验文件"""
        results = self.batch_hash(input_dir, algorithm)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            for result in results:
                f.write(f"{result['hash']}  {result['filename']}\n")
        
        print(f"✅ 校验文件已生成: {output_file}")
        return output_file
    
    def verify_checksum_file(self, checksum_file: str, input_dir: str) -> list:
        """校验校验文件"""
        results = []
        
        with open(checksum_file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                
                parts = line.split('  ')
                if len(parts) == 2:
                    expected_hash, filename = parts
                    file_path = os.path.join(input_dir, filename)
                    
                    if os.path.exists(file_path):
                        actual_hash = self.hash_file(file_path)
                        results.append({
                            'filename': filename,
                            'expected': expected_hash,
                            'actual': actual_hash,
                            'match': actual_hash == expected_hash,
                        })
                    else:
                        results.append({
                            'filename': filename,
                            'error': '文件不存在',
                        })
        
        print(f"✅ 校验完成: {len(results)} 个文件")
        return results
    
    def export_results(self, output_file: str = 'hash_results.json') -> str:
        """导出结果"""
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, ensure_ascii=False, indent=2)
        
        print(f"✅ 结果已导出: {output_file}")
        return output_file


def main():
    """主函数"""
    print("=" * 50)
    print("文件哈希大师 v1.0")
    print("=" * 50)
    print()
    print("功能:")
    print("  1. 计算哈希")
    print("  2. 批量计算")
    print("  3. 校验哈希")
    print("  4. 比较文件")
    print("  5. 查找重复")
    print("  6. 生成校验文件")
    print()
    print("使用方法:")
    print("  from hash_master import HashMaster")
    print("  master = HashMaster()")
    print("  hash_value = master.hash_file('file.txt')")
    print("  result = master.verify_hash('file.txt', 'expected_hash')")
    print()
    print("价格: $8.99")


if __name__ == "__main__":
    main()
