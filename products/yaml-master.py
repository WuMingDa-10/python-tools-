#!/usr/bin/env python3
"""
YAML 处理大师 v1.0
==================
功能：YAML 解析、转换、验证、生成
售价：$9.99
"""

import os
import sys
import json
from datetime import datetime

try:
    import yaml
except ImportError:
    import subprocess
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'pyyaml'])
    import yaml


class YAMLMaster:
    """YAML 处理大师"""
    
    def __init__(self):
        self.data = None
    
    def load_file(self, file_path: str) -> dict:
        """加载 YAML 文件"""
        with open(file_path, 'r', encoding='utf-8') as f:
            self.data = yaml.safe_load(f)
        print(f"✅ 加载完成: {file_path}")
        return self.data
    
    def load_string(self, yaml_string: str) -> dict:
        """加载字符串"""
        self.data = yaml.safe_load(yaml_string)
        return self.data
    
    def dump_string(self, data: dict = None) -> str:
        """转为字符串"""
        if data is None:
            data = self.data
        return yaml.dump(data, allow_unicode=True, default_flow_style=False)
    
    def save_file(self, data: dict = None, output_file: str = 'output.yaml') -> str:
        """保存文件"""
        if data is None:
            data = self.data
        
        with open(output_file, 'w', encoding='utf-8') as f:
            yaml.dump(data, f, allow_unicode=True, default_flow_style=False)
        
        print(f"✅ 保存完成: {output_file}")
        return output_file
    
    def yaml_to_json(self, data: dict = None, output_file: str = None) -> str:
        """YAML 转 JSON"""
        if data is None:
            data = self.data
        
        json_str = json.dumps(data, ensure_ascii=False, indent=2)
        
        if output_file:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(json_str)
            print(f"✅ 转换完成: {output_file}")
        
        return json_str
    
    def json_to_yaml(self, json_file: str, output_file: str = None) -> str:
        """JSON 转 YAML"""
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        yaml_str = yaml.dump(data, allow_unicode=True, default_flow_style=False)
        
        if output_file:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(yaml_str)
            print(f"✅ 转换完成: {output_file}")
        
        return yaml_str
    
    def validate_yaml(self, yaml_string: str) -> dict:
        """验证 YAML"""
        try:
            yaml.safe_load(yaml_string)
            return {'valid': True, 'error': None}
        except yaml.YAMLError as e:
            return {'valid': False, 'error': str(e)}
    
    def merge_yaml(self, *files: str) -> dict:
        """合并多个 YAML 文件"""
        merged = {}
        
        for file_path in files:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
                if data:
                    merged.update(data)
        
        return merged
    
    def get_value(self, data: dict, path: str, default=None):
        """获取嵌套值"""
        keys = path.split('.')
        result = data
        
        for key in keys:
            if isinstance(result, dict):
                result = result.get(key, default)
            else:
                return default
        
        return result
    
    def set_value(self, data: dict, path: str, value):
        """设置嵌套值"""
        keys = path.split('.')
        current = data
        
        for key in keys[:-1]:
            if key not in current:
                current[key] = {}
            current = current[key]
        
        current[keys[-1]] = value
    
    def create_config(self, template: dict, values: dict) -> dict:
        """创建配置"""
        import copy
        config = copy.deepcopy(template)
        
        for key, value in values.items():
            self.set_value(config, key, value)
        
        return config
    
    def generate_example(self, schema: dict) -> dict:
        """生成示例数据"""
        example = {}
        
        for key, value_type in schema.items():
            if value_type == 'string':
                example[key] = 'example'
            elif value_type == 'int':
                example[key] = 0
            elif value_type == 'float':
                example[key] = 0.0
            elif value_type == 'bool':
                example[key] = True
            elif value_type == 'list':
                example[key] = []
            elif value_type == 'dict':
                example[key] = {}
        
        return example


def main():
    """主函数"""
    print("=" * 50)
    print("YAML 处理大师 v1.0")
    print("=" * 50)
    print()
    print("功能:")
    print("  1. YAML 解析")
    print("  2. YAML 转 JSON")
    print("  3. YAML 验证")
    print("  4. YAML 生成")
    print("  5. 配置管理")
    print("  6. 合并 YAML")
    print()
    print("使用方法:")
    print("  from yaml_master import YAMLMaster")
    print("  master = YAMLMaster()")
    print("  data = master.load_file('config.yaml')")
    print("  master.save_file(data, 'output.yaml')")
    print()
    print("价格: $9.99")


if __name__ == "__main__":
    main()
