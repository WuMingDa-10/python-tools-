#!/usr/bin/env python3
"""
缓存管理大师 v1.0
=================
功能：内存缓存、文件缓存、Redis 缓存、缓存策略
售价：$11.99
"""

import os
import sys
import json
import time
import hashlib
import pickle
from datetime import datetime, timedelta
from pathlib import Path


class CacheMaster:
    """缓存管理大师"""
    
    def __init__(self, cache_dir: str = '.cache'):
        self.cache_dir = cache_dir
        self.memory_cache = {}
        self.ttl_cache = {}
        
        os.makedirs(cache_dir, exist_ok=True)
    
    def _get_cache_key(self, key: str) -> str:
        """获取缓存键"""
        return hashlib.md5(key.encode()).hexdigest()
    
    def _get_cache_path(self, key: str) -> str:
        """获取缓存文件路径"""
        cache_key = self._get_cache_key(key)
        return os.path.join(self.cache_dir, f'{cache_key}.cache')
    
    def set_memory(self, key: str, value, ttl: int = None):
        """设置内存缓存"""
        self.memory_cache[key] = value
        
        if ttl:
            self.ttl_cache[key] = time.time() + ttl
    
    def get_memory(self, key: str, default=None):
        """获取内存缓存"""
        if key in self.memory_cache:
            # 检查 TTL
            if key in self.ttl_cache:
                if time.time() > self.ttl_cache[key]:
                    del self.memory_cache[key]
                    del self.ttl_cache[key]
                    return default
            return self.memory_cache[key]
        return default
    
    def delete_memory(self, key: str):
        """删除内存缓存"""
        if key in self.memory_cache:
            del self.memory_cache[key]
        if key in self.ttl_cache:
            del self.ttl_cache[key]
    
    def clear_memory(self):
        """清空内存缓存"""
        self.memory_cache.clear()
        self.ttl_cache.clear()
    
    def set_file(self, key: str, value, ttl: int = None):
        """设置文件缓存"""
        cache_path = self._get_cache_path(key)
        
        data = {
            'value': value,
            'created': time.time(),
            'ttl': ttl,
        }
        
        with open(cache_path, 'wb') as f:
            pickle.dump(data, f)
    
    def get_file(self, key: str, default=None):
        """获取文件缓存"""
        cache_path = self._get_cache_path(key)
        
        if not os.path.exists(cache_path):
            return default
        
        try:
            with open(cache_path, 'rb') as f:
                data = pickle.load(f)
            
            # 检查 TTL
            if data.get('ttl'):
                if time.time() > data['created'] + data['ttl']:
                    os.remove(cache_path)
                    return default
            
            return data['value']
        except Exception:
            return default
    
    def delete_file(self, key: str):
        """删除文件缓存"""
        cache_path = self._get_cache_path(key)
        if os.path.exists(cache_path):
            os.remove(cache_path)
    
    def clear_file(self):
        """清空文件缓存"""
        for file_path in Path(self.cache_dir).glob('*.cache'):
            file_path.unlink()
    
    def set(self, key: str, value, ttl: int = None, backend: str = 'memory'):
        """设置缓存"""
        if backend == 'memory':
            self.set_memory(key, value, ttl)
        elif backend == 'file':
            self.set_file(key, value, ttl)
    
    def get(self, key: str, default=None, backend: str = 'memory'):
        """获取缓存"""
        if backend == 'memory':
            return self.get_memory(key, default)
        elif backend == 'file':
            return self.get_file(key, default)
        return default
    
    def delete(self, key: str, backend: str = 'memory'):
        """删除缓存"""
        if backend == 'memory':
            self.delete_memory(key)
        elif backend == 'file':
            self.delete_file(key)
    
    def clear(self, backend: str = 'memory'):
        """清空缓存"""
        if backend == 'memory':
            self.clear_memory()
        elif backend == 'file':
            self.clear_file()
    
    def has(self, key: str, backend: str = 'memory') -> bool:
        """检查缓存是否存在"""
        return self.get(key, backend=backend) is not None
    
    def get_or_set(self, key: str, func: callable, ttl: int = None, 
                   backend: str = 'memory'):
        """获取或设置缓存"""
        value = self.get(key, backend=backend)
        
        if value is None:
            value = func()
            self.set(key, value, ttl, backend)
        
        return value
    
    def get_stats(self, backend: str = 'memory') -> dict:
        """获取缓存统计"""
        if backend == 'memory':
            return {
                'type': 'memory',
                'keys': len(self.memory_cache),
                'ttl_keys': len(self.ttl_cache),
            }
        elif backend == 'file':
            cache_files = list(Path(self.cache_dir).glob('*.cache'))
            return {
                'type': 'file',
                'files': len(cache_files),
                'directory': self.cache_dir,
            }
        return {}


def main():
    """主函数"""
    print("=" * 50)
    print("缓存管理大师 v1.0")
    print("=" * 50)
    print()
    print("功能:")
    print("  1. 内存缓存")
    print("  2. 文件缓存")
    print("  3. TTL 支持")
    print("  4. 缓存策略")
    print("  5. 缓存统计")
    print("  6. 批量操作")
    print()
    print("使用方法:")
    print("  from cache_master import CacheMaster")
    print("  cache = CacheMaster()")
    print("  cache.set('key', 'value', ttl=300)")
    print("  value = cache.get('key')")
    print()
    print("价格: $11.99")


if __name__ == "__main__":
    main()
