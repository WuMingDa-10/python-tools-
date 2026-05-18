#!/usr/bin/env python3
"""
文件监控大师 v1.0
=================
功能：文件监控、变化检测、自动处理、事件通知
售价：$12.99
"""

import os
import sys
import time
import hashlib
from datetime import datetime
from pathlib import Path


class FileWatcher:
    """文件监控大师"""
    
    def __init__(self):
        self.watching = False
        self.callbacks = {}
        self.file_hashes = {}
    
    def get_file_hash(self, file_path: str) -> str:
        """获取文件哈希"""
        hasher = hashlib.md5()
        with open(file_path, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b''):
                hasher.update(chunk)
        return hasher.hexdigest()
    
    def scan_directory(self, directory: str, pattern: str = '*') -> dict:
        """扫描目录"""
        files = {}
        for file_path in Path(directory).glob(pattern):
            if file_path.is_file():
                files[str(file_path)] = {
                    'size': file_path.stat().st_size,
                    'modified': file_path.stat().st_mtime,
                    'hash': self.get_file_hash(str(file_path)),
                }
        return files
    
    def watch_directory(self, directory: str, callback: callable, 
                       interval: float = 1.0, pattern: str = '*'):
        """监控目录"""
        self.watching = True
        self.callbacks[directory] = callback
        
        # 初始扫描
        initial_files = self.scan_directory(directory, pattern)
        self.file_hashes[directory] = initial_files
        
        print(f"🔍 开始监控: {directory}")
        
        try:
            while self.watching:
                current_files = self.scan_directory(directory, pattern)
                initial_files = self.file_hashes.get(directory, {})
                
                # 检测变化
                changes = self._detect_changes(initial_files, current_files)
                
                if changes:
                    callback(changes)
                    self.file_hashes[directory] = current_files
                
                time.sleep(interval)
        except KeyboardInterrupt:
            print("⏹️ 停止监控")
            self.watching = False
    
    def _detect_changes(self, old_files: dict, new_files: dict) -> list:
        """检测变化"""
        changes = []
        
        # 新增文件
        for file_path in new_files:
            if file_path not in old_files:
                changes.append({
                    'type': 'created',
                    'path': file_path,
                    'timestamp': datetime.now().isoformat(),
                })
        
        # 删除文件
        for file_path in old_files:
            if file_path not in new_files:
                changes.append({
                    'type': 'deleted',
                    'path': file_path,
                    'timestamp': datetime.now().isoformat(),
                })
        
        # 修改文件
        for file_path in new_files:
            if file_path in old_files:
                if new_files[file_path]['hash'] != old_files[file_path]['hash']:
                    changes.append({
                        'type': 'modified',
                        'path': file_path,
                        'timestamp': datetime.now().isoformat(),
                    })
        
        return changes
    
    def stop_watching(self):
        """停止监控"""
        self.watching = False
    
    def watch_file(self, file_path: str, callback: callable, interval: float = 1.0):
        """监控单个文件"""
        self.watching = True
        
        if os.path.exists(file_path):
            initial_hash = self.get_file_hash(file_path)
        else:
            initial_hash = None
        
        print(f"🔍 开始监控文件: {file_path}")
        
        try:
            while self.watching:
                if os.path.exists(file_path):
                    current_hash = self.get_file_hash(file_path)
                    
                    if initial_hash is None:
                        callback({'type': 'created', 'path': file_path})
                        initial_hash = current_hash
                    elif current_hash != initial_hash:
                        callback({'type': 'modified', 'path': file_path})
                        initial_hash = current_hash
                else:
                    if initial_hash is not None:
                        callback({'type': 'deleted', 'path': file_path})
                        initial_hash = None
                
                time.sleep(interval)
        except KeyboardInterrupt:
            print("⏹️ 停止监控")
            self.watching = False


def main():
    """主函数"""
    print("=" * 50)
    print("文件监控大师 v1.0")
    print("=" * 50)
    print()
    print("功能:")
    print("  1. 目录监控")
    print("  2. 文件监控")
    print("  3. 变化检测")
    print("  4. 自动处理")
    print("  5. 事件通知")
    print("  6. 批量监控")
    print()
    print("使用方法:")
    print("  from file_watcher import FileWatcher")
    print("  watcher = FileWatcher()")
    print("  watcher.watch_directory('./data', callback)")
    print()
    print("价格: $12.99")


if __name__ == "__main__":
    main()
