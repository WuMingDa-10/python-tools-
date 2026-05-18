#!/usr/bin/env python3
"""
线程管理大师 v1.0
=================
功能：线程池、任务调度、并发控制、异步执行
售价：$13.99
"""

import os
import sys
import threading
import time
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed


class ThreadMaster:
    """线程管理大师"""
    
    def __init__(self, max_workers: int = 4):
        self.max_workers = max_workers
        self.executor = ThreadPoolExecutor(max_workers=max_workers)
        self.futures = {}
        self.results = {}
    
    def submit(self, func: callable, *args, **kwargs) -> str:
        """提交任务"""
        task_id = f"task_{len(self.futures) + 1}"
        future = self.executor.submit(func, *args, **kwargs)
        self.futures[task_id] = future
        return task_id
    
    def submit_with_callback(self, func: callable, callback: callable, 
                            *args, **kwargs) -> str:
        """提交任务并设置回调"""
        task_id = f"task_{len(self.futures) + 1}"
        
        def wrapper():
            result = func(*args, **kwargs)
            callback(result)
            return result
        
        future = self.executor.submit(wrapper)
        self.futures[task_id] = future
        return task_id
    
    def get_result(self, task_id: str, timeout: float = None):
        """获取结果"""
        if task_id in self.futures:
            future = self.futures[task_id]
            try:
                return future.result(timeout=timeout)
            except Exception as e:
                return {'error': str(e)}
        return None
    
    def wait_all(self, timeout: float = None) -> dict:
        """等待所有任务完成"""
        results = {}
        
        for task_id, future in self.futures.items():
            try:
                results[task_id] = future.result(timeout=timeout)
            except Exception as e:
                results[task_id] = {'error': str(e)}
        
        return results
    
    def map(self, func: callable, items: list) -> list:
        """并行映射"""
        results = []
        
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = [executor.submit(func, item) for item in items]
            
            for future in as_completed(futures):
                try:
                    results.append(future.result())
                except Exception as e:
                    results.append({'error': str(e)})
        
        return results
    
    def map_with_progress(self, func: callable, items: list, 
                         callback: callable = None) -> list:
        """带进度的并行映射"""
        results = []
        completed = 0
        total = len(items)
        
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            future_to_item = {executor.submit(func, item): item for item in items}
            
            for future in as_completed(future_to_item):
                try:
                    result = future.result()
                    results.append(result)
                except Exception as e:
                    results.append({'error': str(e)})
                
                completed += 1
                if callback:
                    callback(completed, total)
        
        return results
    
    def run_periodic(self, func: callable, interval: float, 
                    duration: float = None):
        """周期性执行"""
        start_time = time.time()
        
        while True:
            if duration and time.time() - start_time > duration:
                break
            
            func()
            time.sleep(interval)
    
    def run_with_timeout(self, func: callable, timeout: float, *args, **kwargs):
        """带超时执行"""
        future = self.executor.submit(func, *args, **kwargs)
        
        try:
            return future.result(timeout=timeout)
        except TimeoutError:
            future.cancel()
            return {'error': 'timeout'}
    
    def get_stats(self) -> dict:
        """获取统计信息"""
        return {
            'max_workers': self.max_workers,
            'pending_tasks': sum(1 for f in self.futures.values() if not f.done()),
            'completed_tasks': sum(1 for f in self.futures.values() if f.done()),
            'total_tasks': len(self.futures),
        }
    
    def cancel_all(self):
        """取消所有任务"""
        for future in self.futures.values():
            future.cancel()
    
    def shutdown(self, wait: bool = True):
        """关闭线程池"""
        self.executor.shutdown(wait=wait)
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.shutdown()


def main():
    """主函数"""
    print("=" * 50)
    print("线程管理大师 v1.0")
    print("=" * 50)
    print()
    print("功能:")
    print("  1. 线程池")
    print("  2. 任务调度")
    print("  3. 并发控制")
    print("  4. 异步执行")
    print("  5. 进度回调")
    print("  6. 超时控制")
    print()
    print("使用方法:")
    print("  from thread_master import ThreadMaster")
    print("  with ThreadMaster(4) as master:")
    print("      task_id = master.submit(func, arg1, arg2)")
    print("      result = master.get_result(task_id)")
    print()
    print("价格: $13.99")


if __name__ == "__main__":
    main()
