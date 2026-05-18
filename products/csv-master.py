#!/usr/bin/env python3
"""
CSV 处理大师 v1.0
=================
功能：CSV 解析、合并、拆分、统计、转换
售价：$12.99
"""

import os
import sys
import csv
import json
from datetime import datetime
from collections import Counter


class CSVMaster:
    """CSV 处理大师"""
    
    def __init__(self):
        self.data = []
        self.headers = []
    
    def load_file(self, file_path: str, encoding: str = 'utf-8-sig') -> list:
        """加载 CSV 文件"""
        with open(file_path, 'r', encoding=encoding) as f:
            reader = csv.DictReader(f)
            self.headers = reader.fieldnames
            self.data = list(reader)
        print(f"✅ 加载完成: {len(self.data)} 行, {len(self.headers)} 列")
        return self.data
    
    def save_file(self, data: list = None, output_file: str = 'output.csv', 
                  encoding: str = 'utf-8-sig') -> str:
        """保存 CSV 文件"""
        if data is None:
            data = self.data
        
        with open(output_file, 'w', newline='', encoding=encoding) as f:
            writer = csv.DictWriter(f, fieldnames=self.headers)
            writer.writeheader()
            writer.writerows(data)
        
        print(f"✅ 保存完成: {output_file}")
        return output_file
    
    def merge_files(self, files: list, output_file: str) -> str:
        """合并多个 CSV 文件"""
        merged = []
        headers = None
        
        for file_path in files:
            with open(file_path, 'r', encoding='utf-8-sig') as f:
                reader = csv.DictReader(f)
                if headers is None:
                    headers = reader.fieldnames
                merged.extend(list(reader))
        
        with open(output_file, 'w', newline='', encoding='utf-8-sig') as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            writer.writeheader()
            writer.writerows(merged)
        
        print(f"✅ 合并完成: {len(merged)} 行")
        return output_file
    
    def split_file(self, file_path: str, output_dir: str, rows_per_file: int = 1000) -> list:
        """拆分 CSV 文件"""
        os.makedirs(output_dir, exist_ok=True)
        
        with open(file_path, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            headers = reader.fieldnames
            rows = list(reader)
        
        output_files = []
        for i in range(0, len(rows), rows_per_file):
            chunk = rows[i:i + rows_per_file]
            output_file = os.path.join(output_dir, f'part_{i // rows_per_file + 1}.csv')
            
            with open(output_file, 'w', newline='', encoding='utf-8-sig') as f:
                writer = csv.DictWriter(f, fieldnames=headers)
                writer.writeheader()
                writer.writerows(chunk)
            
            output_files.append(output_file)
        
        print(f"✅ 拆分完成: {len(output_files)} 个文件")
        return output_files
    
    def filter_rows(self, data: list = None, column: str = None, 
                   value: str = None, condition: str = 'eq') -> list:
        """过滤行"""
        if data is None:
            data = self.data
        
        if column is None or value is None:
            return data
        
        filtered = []
        for row in data:
            cell = row.get(column, '')
            
            if condition == 'eq' and cell == value:
                filtered.append(row)
            elif condition == 'ne' and cell != value:
                filtered.append(row)
            elif condition == 'contains' and value in cell:
                filtered.append(row)
            elif condition == 'startswith' and cell.startswith(value):
                filtered.append(row)
            elif condition == 'endswith' and cell.endswith(value):
                filtered.append(row)
        
        print(f"✅ 过滤完成: {len(filtered)} 行")
        return filtered
    
    def sort_data(self, data: list = None, column: str = None, 
                  reverse: bool = False) -> list:
        """排序数据"""
        if data is None:
            data = self.data
        
        if column is None:
            return data
        
        return sorted(data, key=lambda x: x.get(column, ''), reverse=reverse)
    
    def get_statistics(self, column: str) -> dict:
        """获取列统计"""
        values = [row.get(column, '') for row in self.data]
        
        # 数值统计
        numeric_values = []
        for v in values:
            try:
                numeric_values.append(float(v))
            except:
                pass
        
        stats = {
            'total': len(values),
            'unique': len(set(values)),
            'empty': sum(1 for v in values if not v),
        }
        
        if numeric_values:
            stats['min'] = min(numeric_values)
            stats['max'] = max(numeric_values)
            stats['sum'] = sum(numeric_values)
            stats['avg'] = sum(numeric_values) / len(numeric_values)
        
        return stats
    
    def deduplicate(self, data: list = None, columns: list = None) -> list:
        """去重"""
        if data is None:
            data = self.data
        
        if columns:
            seen = set()
            unique = []
            for row in data:
                key = tuple(row.get(col, '') for col in columns)
                if key not in seen:
                    seen.add(key)
                    unique.append(row)
        else:
            seen = set()
            unique = []
            for row in data:
                key = tuple(sorted(row.items()))
                if key not in seen:
                    seen.add(key)
                    unique.append(row)
        
        print(f"✅ 去重完成: {len(data)} -> {len(unique)} 行")
        return unique
    
    def to_json(self, data: list = None, output_file: str = 'output.json') -> str:
        """转换为 JSON"""
        if data is None:
            data = self.data
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"✅ 转换完成: {output_file}")
        return output_file
    
    def to_markdown(self, data: list = None, output_file: str = 'output.md') -> str:
        """转换为 Markdown 表格"""
        if data is None:
            data = self.data
        
        if not data:
            return None
        
        headers = list(data[0].keys())
        
        # 表头
        md = '| ' + ' | '.join(headers) + ' |\n'
        md += '| ' + ' | '.join(['---'] * len(headers)) + ' |\n'
        
        # 数据行
        for row in data:
            md += '| ' + ' | '.join(str(row.get(h, '')) for h in headers) + ' |\n'
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(md)
        
        print(f"✅ 转换完成: {output_file}")
        return output_file


def main():
    """主函数"""
    print("=" * 50)
    print("CSV 处理大师 v1.0")
    print("=" * 50)
    print()
    print("功能:")
    print("  1. 加载/保存")
    print("  2. 合并/拆分")
    print("  3. 过滤/排序")
    print("  4. 去重")
    print("  5. 统计")
    print("  6. 转换")
    print()
    print("使用方法:")
    print("  from csv_master import CSVMaster")
    print("  master = CSVMaster()")
    print("  data = master.load_file('data.csv')")
    print("  filtered = master.filter_rows(column='status', value='active')")
    print()
    print("价格: $12.99")


if __name__ == "__main__":
    main()
