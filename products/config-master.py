#!/usr/bin/env python3
"""
配置管理大师 v1.0
=================
功能：配置文件处理、环境变量、配置合并、配置验证
售价：$10.99
"""

import os
import sys
import json
import yaml
from datetime import datetime


class ConfigMaster:
    """配置管理大师"""
    
    def __init__(self):
        self.config = {}
        self.sources = []
    
    def load_json(self, file_path: str) -> dict:
        """加载 JSON 配置"""
        with open(file_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        self.config.update(config)
        self.sources.append(('json', file_path))
        print(f"✅ 加载完成: {file_path}")
        return config
    
    def load_yaml(self, file_path: str) -> dict:
        """加载 YAML 配置"""
        with open(file_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        
        if config:
            self.config.update(config)
            self.sources.append(('yaml', file_path))
            print(f"✅ 加载完成: {file_path}")
        
        return config
    
    def load_env(self, prefix: str = '') -> dict:
        """加载环境变量"""
        env_config = {}
        
        for key, value in os.environ.items():
            if prefix and not key.startswith(prefix):
                continue
            
            # 移除前缀
            config_key = key[len(prefix):] if prefix else key
            
            # 转换为小写
            config_key = config_key.lower()
            
            # 尝试转换类型
            if value.lower() in ('true', 'yes', '1'):
                env_config[config_key] = True
            elif value.lower() in ('false', 'no', '0'):
                env_config[config_key] = False
            elif value.isdigit():
                env_config[config_key] = int(value)
            else:
                try:
                    env_config[config_key] = float(value)
                except ValueError:
                    env_config[config_key] = value
        
        self.config.update(env_config)
        self.sources.append(('env', prefix))
        print(f"✅ 加载完成: {len(env_config)} 个环境变量")
        return env_config
    
    def merge(self, config: dict):
        """合并配置"""
        self._deep_merge(self.config, config)
    
    def _deep_merge(self, base: dict, override: dict):
        """深度合并"""
        for key, value in override.items():
            if key in base and isinstance(base[key], dict) and isinstance(value, dict):
                self._deep_merge(base[key], value)
            else:
                base[key] = value
    
    def get(self, key: str, default=None):
        """获取配置值"""
        keys = key.split('.')
        value = self.config
        
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
            else:
                return default
        
        return value if value is not None else default
    
    def set(self, key: str, value):
        """设置配置值"""
        keys = key.split('.')
        config = self.config
        
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        
        config[keys[-1]] = value
    
    def has(self, key: str) -> bool:
        """检查配置是否存在"""
        return self.get(key) is not None
    
    def save_json(self, output_file: str = 'config.json'):
        """保存为 JSON"""
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(self.config, f, ensure_ascii=False, indent=2)
        print(f"✅ 保存完成: {output_file}")
        return output_file
    
    def save_yaml(self, output_file: str = 'config.yaml'):
        """保存为 YAML"""
        with open(output_file, 'w', encoding='utf-8') as f:
            yaml.dump(self.config, f, allow_unicode=True, default_flow_style=False)
        print(f"✅ 保存完成: {output_file}")
        return output_file
    
    def validate(self, schema: dict) -> dict:
        """验证配置"""
        errors = []
        
        for key, expected_type in schema.items():
            value = self.get(key)
            
            if value is None:
                errors.append(f"缺少配置: {key}")
            elif not isinstance(value, expected_type):
                errors.append(f"类型错误: {key}, 期望 {expected_type.__name__}, 实际 {type(value).__name__}")
        
        return {
            'valid': len(errors) == 0,
            'errors': errors,
        }
    
    def get_all(self) -> dict:
        """获取所有配置"""
        return self.config.copy()
    
    def get_sources(self) -> list:
        """获取配置来源"""
        return self.sources
    
    def create_template(self, keys: list, output_file: str = 'config.template.json') -> str:
        """创建配置模板"""
        template = {}
        
        for key in keys:
            template[key] = ''
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(template, f, ensure_ascii=False, indent=2)
        
        print(f"✅ 模板已创建: {output_file}")
        return output_file


def main():
    """主函数"""
    print("=" * 50)
    print("配置管理大师 v1.0")
    print("=" * 50)
    print()
    print("功能:")
    print("  1. 加载配置")
    print("  2. 合并配置")
    print("  3. 配置验证")
    print("  4. 配置保存")
    print("  5. 环境变量")
    print("  6. 配置模板")
    print()
    print("使用方法:")
    print("  from config_master import ConfigMaster")
    print("  config = ConfigMaster()")
    print("  config.load_json('config.json')")
    print("  db_url = config.get('database.url')")
    print()
    print("价格: $10.99")


if __name__ == "__main__":
    main()
