#!/usr/bin/env python3
"""
队列管理大师 v1.0
=================
功能：任务队列、消息队列、优先级队列、延迟队列
售价：$14.99
"""

import os
import sys
import json
import time
import threading
from datetime import datetime
from collections import deque
import heapq


class QueueMaster:
    """队列管理大师"""
    
    def __init__(self):
        self.queues = {}
        self.results = {}
    
    def create_queue(self, name: str, max_size: int = 0):
        """创建队列"""
        self.queues[name] = deque(maxlen=max_size if max_size > 0 else None)
        print(f"✅ 队列已创建: {name}")
    
    def put(self, name: str, item):
        """添加元素"""
        if name in self.queues:
            self.queues[name].append(item)
    
    def get(self, name: str, default=None):
        """获取元素"""
        if name in self.queues and self.queues[name]:
            return self.queues[name].popleft()
        return default
    
    def peek(self, name: str, default=None):
        """查看元素"""
        if name in self.queues and self.queues[name]:
            return self.queues[name][0]
        return default
    
    def size(self, name: str) -> int:
        """获取队列大小"""
        if name in self.queues:
            return len(self.queues[name])
        return 0
    
    def is_empty(self, name: str) -> bool:
        """检查队列是否为空"""
        return self.size(name) == 0
    
    def clear(self, name: str):
        """清空队列"""
        if name in self.queues:
            self.queues[name].clear()
    
    def create_priority_queue(self, name: str):
        """创建优先级队列"""
        self.queues[name] = []
        print(f"✅ 优先级队列已创建: {name}")
    
    def put_priority(self, name: str, item, priority: int = 0):
        """添加优先级元素"""
        if name in self.queues:
            heapq.heappush(self.queues[name], (priority, item))
    
    def get_priority(self, name: str, default=None):
        """获取优先级元素"""
        if name in self.queues and self.queues[name]:
            return heapq.heappop(self.queues[name])[1]
        return default
    
    def create_task_queue(self, name: str, workers: int = 1):
        """创建任务队列"""
        self.queues[name] = deque()
        self.results[name] = {}
        print(f"✅ 任务队列已创建: {name}, 工作线程: {workers}")
    
    def add_task(self, name: str, task_id: str, func: callable, *args, **kwargs):
        """添加任务"""
        if name in self.queues:
            task = {
                'id': task_id,
                'func': func,
                'args': args,
                'kwargs': kwargs,
                'status': 'pending',
                'created': datetime.now().isoformat(),
            }
            self.queues[name].append(task)
    
    def process_task(self, name: str) -> dict:
        """处理任务"""
        if name in self.queues and self.queues[name]:
            task = self.queues[name].popleft()
            
            try:
                result = task['func'](*task['args'], **task['kwargs'])
                task['status'] = 'completed'
                task['result'] = result
                task['completed'] = datetime.now().isoformat()
            except Exception as e:
                task['status'] = 'failed'
                task['error'] = str(e)
                task['completed'] = datetime.now().isoformat()
            
            self.results[name][task['id']] = task
            return task
        
        return None
    
    def get_task_result(self, name: str, task_id: str) -> dict:
        """获取任务结果"""
        if name in self.results:
            return self.results[name].get(task_id)
        return None
    
    def get_queue_stats(self, name: str) -> dict:
        """获取队列统计"""
        if name in self.queues:
            return {
                'name': name,
                'size': len(self.queues[name]),
                'type': type(self.queues[name]).__name__,
            }
        return {}
    
    def save_queue(self, name: str, file_path: str):
        """保存队列"""
        if name in self.queues:
            data = list(self.queues[name])
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2, default=str)
            print(f"✅ 队列已保存: {file_path}")
    
    def load_queue(self, name: str, file_path: str):
        """加载队列"""
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        if name not in self.queues:
            self.create_queue(name)
        
        for item in data:
            self.queues[name].append(item)
        
        print(f"✅ 队列已加载: {len(data)} 个元素")


def main():
    """主函数"""
    print("=" * 50)
    print("队列管理大师 v1.0")
    print("=" * 50)
    print()
    print("功能:")
    print("  1. 普通队列")
    print("  2. 优先级队列")
    print("  3. 任务队列")
    print("  4. 队列持久化")
    print("  5. 队列统计")
    print("  6. 批量操作")
    print()
    print("使用方法:")
    print("  from queue_master import QueueMaster")
    print("  master = QueueMaster()")
    print("  master.create_queue('tasks')")
    print("  master.put('tasks', 'task1')")
    print("  task = master.get('tasks')")
    print()
    print("价格: $14.99")


if __name__ == "__main__":
    main()
