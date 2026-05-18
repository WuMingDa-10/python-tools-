#!/usr/bin/env python3
"""
环境变量大师 v1.0
=================
功能：环境变量管理、配置文件处理、密钥管理
售价：$8.99
"""

import os
import sys
import json
from datetime import datetime


class EnvMaster:
    """环境变量大师"""
    
    def __init__(self):
        self.env_vars = {}
    
    def get_env(self, key: str, default: str = None) -> str:
        """获取环境变量"""
        return os.environ.get(key, default)
    
    def set_env(self, key: str, value: str):
        """设置环境变量"""
        os.environ[key] = value
        self.env_vars[key] = value
    
    def load_env_file(self, file_path: str) -> dict:
        """加载 .env 文件"""
        env_vars = {}
        
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                
                if '=' in line:
                    key, value = line.split('=', 1)
                    key = key.strip()
                    value = value.strip().strip('"').strip("'")
                    env_vars[key] = value
                    os.environ[key] = value
        
        self.env_vars.update(env_vars)
        print(f"✅ 加载完成: {len(env_vars)} 个变量")
        return env_vars
    
    def save_env_file(self, env_vars: dict = None, output_file: str = '.env') -> str:
        """保存 .env 文件"""
        if env_vars is None:
            env_vars = self.env_vars
        
        with open(output_file, 'w', encoding='utf-8') as f:
            for key, value in env_vars.items():
                f.write(f'{key}={value}\n')
        
        print(f"✅ 保存完成: {output_file}")
        return output_file
    
    def load_json_config(self, file_path: str) -> dict:
        """加载 JSON 配置"""
        with open(file_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        # 设置为环境变量
        for key, value in config.items():
            if isinstance(value, str):
                os.environ[key] = value
        
        return config
    
    def save_json_config(self, config: dict, output_file: str = 'config.json') -> str:
        """保存 JSON 配置"""
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(config, f, ensure_ascii=False, indent=2)
        
        print(f"✅ 保存完成: {output_file}")
        return output_file
    
    def get_all_env(self) -> dict:
        """获取所有环境变量"""
        return dict(os.environ)
    
    def filter_env(self, prefix: str) -> dict:
        """过滤环境变量"""
        return {k: v for k, v in os.environ.items() if k.startswith(prefix)}
    
    def export_env(self, output_file: str = 'env_export.json') -> str:
        """导出环境变量"""
        env_vars = dict(os.environ)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(env_vars, f, ensure_ascii=False, indent=2)
        
        print(f"✅ 导出完成: {output_file}")
        return output_file
    
    def create_config_template(self, keys: list, output_file: str = '.env.example') -> str:
        """创建配置模板"""
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write('# 环境变量配置模板\n')
            f.write(f'# 生成时间: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}\n\n')
            
            for key in keys:
                f.write(f'{key}=\n')
        
        print(f"✅ 模板已创建: {output_file}")
        return output_file
    
    def validate_env(self, required_keys: list) -> dict:
        """验证环境变量"""
        missing = []
        
        for key in required_keys:
            if key not in os.environ:
                missing.append(key)
        
        return {
            'valid': len(missing) == 0,
            'missing': missing,
        }
    
    def generate_secret(self, length: int = 32) -> str:
        """生成密钥"""
        import secrets
        return secrets.token_hex(length)
    
    def mask_value(self, value: str, show_chars: int = 4) -> str:
        """遮蔽值"""
        if len(value) <= show_chars:
            return '*' * len(value)
        return value[:show_chars] + '*' * (len(value) - show_chars)


def main():
    """主函数"""
    print("=" * 50)
    print("环境变量大师 v1.0")
    print("=" * 50)
    print()
    print("功能:")
    print("  1. 环境变量管理")
    print("  2. .env 文件处理")
    print("  3. JSON 配置处理")
    print("  4. 配置模板生成")
    print("  5. 密钥生成")
    print("  6. 配置验证")
    print()
    print("使用方法:")
    print("  from env_master import EnvMaster")
    print("  master = EnvMaster()")
    print("  master.load_env_file('.env')")
    print("  db_url = master.get_env('DATABASE_URL')")
    print()
    print("价格: $8.99")


if __name__ == "__main__":
    main()
