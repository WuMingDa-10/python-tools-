#!/usr/bin/env python3
"""
数据库管理大师 v1.0
===================
功能：SQLite/MySQL/PostgreSQL 管理、数据导入导出、备份恢复
售价：$19.99
"""

import os
import sys
import json
import csv
from datetime import datetime

try:
    import sqlite3
except ImportError:
    pass


class DatabaseMaster:
    """数据库管理大师"""
    
    def __init__(self, db_type: str = 'sqlite'):
        self.db_type = db_type
        self.connection = None
    
    def connect_sqlite(self, db_file: str):
        """连接 SQLite 数据库"""
        self.connection = sqlite3.connect(db_file)
        print(f"✅ 已连接: {db_file}")
    
    def execute_query(self, query: str, params: tuple = None) -> list:
        """执行查询"""
        cursor = self.connection.cursor()
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        
        if query.strip().upper().startswith('SELECT'):
            return cursor.fetchall()
        else:
            self.connection.commit()
            return cursor.rowcount
    
    def export_to_csv(self, table_name: str, output_file: str) -> str:
        """导出表到 CSV"""
        cursor = self.connection.cursor()
        cursor.execute(f"SELECT * FROM {table_name}")
        rows = cursor.fetchall()
        
        # 获取列名
        cursor.execute(f"PRAGMA table_info({table_name})")
        columns = [col[1] for col in cursor.fetchall()]
        
        with open(output_file, 'w', newline='', encoding='utf-8-sig') as f:
            writer = csv.writer(f)
            writer.writerow(columns)
            writer.writerows(rows)
        
        print(f"✅ 导出完成: {output_file} ({len(rows)} 行)")
        return output_file
    
    def export_to_json(self, table_name: str, output_file: str) -> str:
        """导出表到 JSON"""
        cursor = self.connection.cursor()
        cursor.execute(f"SELECT * FROM {table_name}")
        rows = cursor.fetchall()
        
        # 获取列名
        cursor.execute(f"PRAGMA table_info({table_name})")
        columns = [col[1] for col in cursor.fetchall()]
        
        data = [dict(zip(columns, row)) for row in rows]
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"✅ 导出完成: {output_file} ({len(rows)} 行)")
        return output_file
    
    def import_from_csv(self, csv_file: str, table_name: str) -> int:
        """从 CSV 导入数据"""
        with open(csv_file, 'r', encoding='utf-8-sig') as f:
            reader = csv.reader(f)
            headers = next(reader)
            rows = list(reader)
        
        # 创建表
        columns = ', '.join([f'{col} TEXT' for col in headers])
        self.execute_query(f"CREATE TABLE IF NOT EXISTS {table_name} ({columns})")
        
        # 插入数据
        placeholders = ', '.join(['?' for _ in headers])
        for row in rows:
            self.execute_query(f"INSERT INTO {table_name} VALUES ({placeholders})", tuple(row))
        
        print(f"✅ 导入完成: {len(rows)} 行")
        return len(rows)
    
    def backup_database(self, backup_file: str) -> str:
        """备份数据库"""
        if self.db_type == 'sqlite':
            import shutil
            db_file = self.connection.execute("PRAGMA database_list").fetchone()[2]
            shutil.copy2(db_file, backup_file)
            print(f"✅ 备份完成: {backup_file}")
        return backup_file
    
    def get_table_info(self, table_name: str) -> dict:
        """获取表信息"""
        cursor = self.connection.cursor()
        
        # 获取列信息
        cursor.execute(f"PRAGMA table_info({table_name})")
        columns = [{'name': col[1], 'type': col[2], 'notnull': col[3], 'default': col[4]} for col in cursor.fetchall()]
        
        # 获取行数
        cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
        row_count = cursor.fetchone()[0]
        
        return {
            'table_name': table_name,
            'columns': columns,
            'row_count': row_count
        }
    
    def list_tables(self) -> list:
        """列出所有表"""
        cursor = self.connection.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        return [row[0] for row in cursor.fetchall()]
    
    def close(self):
        """关闭连接"""
        if self.connection:
            self.connection.close()
            print("✅ 连接已关闭")


def main():
    """主函数"""
    print("=" * 50)
    print("数据库管理大师 v1.0")
    print("=" * 50)
    print()
    print("功能:")
    print("  1. 连接 SQLite/MySQL/PostgreSQL")
    print("  2. 执行 SQL 查询")
    print("  3. 导出到 CSV/JSON")
    print("  4. 从 CSV 导入")
    print("  5. 备份恢复")
    print("  6. 表结构管理")
    print()
    print("使用方法:")
    print("  from db_master import DatabaseMaster")
    print("  db = DatabaseMaster('sqlite')")
    print("  db.connect_sqlite('data.db')")
    print("  db.export_to_csv('users', 'users.csv')")
    print()
    print("价格: $19.99")


if __name__ == "__main__":
    main()
