#!/usr/bin/env python3
"""
系统监控大师 v1.0
=================
功能：CPU/内存/磁盘监控、进程管理、日志分析
售价：$19.99
"""

import os
import sys
import time
import json
from datetime import datetime

try:
    import psutil
except ImportError:
    import subprocess
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'psutil'])
    import psutil


class SystemMonitor:
    """系统监控大师"""
    
    def __init__(self):
        self.alerts = []
    
    def get_cpu_info(self) -> dict:
        """获取 CPU 信息"""
        return {
            'usage_percent': psutil.cpu_percent(interval=1),
            'count': psutil.cpu_count(),
            'freq': psutil.cpu_freq()._asdict() if psutil.cpu_freq() else None,
        }
    
    def get_memory_info(self) -> dict:
        """获取内存信息"""
        mem = psutil.virtual_memory()
        return {
            'total': mem.total,
            'available': mem.available,
            'used': mem.used,
            'percent': mem.percent,
        }
    
    def get_disk_info(self) -> list:
        """获取磁盘信息"""
        disks = []
        for partition in psutil.disk_partitions():
            try:
                usage = psutil.disk_usage(partition.mountpoint)
                disks.append({
                    'device': partition.device,
                    'mountpoint': partition.mountpoint,
                    'total': usage.total,
                    'used': usage.used,
                    'free': usage.free,
                    'percent': usage.percent,
                })
            except:
                pass
        return disks
    
    def get_network_info(self) -> dict:
        """获取网络信息"""
        net = psutil.net_io_counters()
        return {
            'bytes_sent': net.bytes_sent,
            'bytes_recv': net.bytes_recv,
            'packets_sent': net.packets_sent,
            'packets_recv': net.packets_recv,
        }
    
    def get_top_processes(self, n: int = 10) -> list:
        """获取 Top N 进程"""
        processes = []
        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
            try:
                processes.append(proc.info)
            except:
                pass
        
        processes.sort(key=lambda x: x.get('cpu_percent', 0), reverse=True)
        return processes[:n]
    
    def monitor_system(self, duration: int = 60, interval: int = 5) -> list:
        """监控系统"""
        print(f"🔍 开始监控系统 ({duration}秒, 间隔{interval}秒)")
        
        history = []
        start_time = time.time()
        
        while time.time() - start_time < duration:
            snapshot = {
                'timestamp': datetime.now().isoformat(),
                'cpu': self.get_cpu_info(),
                'memory': self.get_memory_info(),
                'disk': self.get_disk_info(),
                'network': self.get_network_info(),
            }
            history.append(snapshot)
            
            # 检查告警
            if snapshot['cpu']['usage_percent'] > 90:
                self.alerts.append(f"CPU 使用率过高: {snapshot['cpu']['usage_percent']}%")
            if snapshot['memory']['percent'] > 90:
                self.alerts.append(f"内存使用率过高: {snapshot['memory']['percent']}%")
            
            time.sleep(interval)
        
        print(f"✅ 监控完成: {len(history)} 条记录")
        return history
    
    def generate_report(self, history: list, output_file: str = 'system_report.json') -> str:
        """生成监控报告"""
        report = {
            'timestamp': datetime.now().isoformat(),
            'duration': len(history),
            'alerts': self.alerts,
            'history': history,
        }
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        print(f"✅ 报告已生成: {output_file}")
        return output_file
    
    def kill_process(self, pid: int) -> bool:
        """终止进程"""
        try:
            proc = psutil.Process(pid)
            proc.terminate()
            print(f"✅ 进程已终止: {pid}")
            return True
        except Exception as e:
            print(f"❌ 终止失败: {e}")
            return False


def main():
    """主函数"""
    print("=" * 50)
    print("系统监控大师 v1.0")
    print("=" * 50)
    print()
    print("功能:")
    print("  1. CPU 监控")
    print("  2. 内存监控")
    print("  3. 磁盘监控")
    print("  4. 网络监控")
    print("  5. 进程管理")
    print("  6. 告警通知")
    print()
    print("使用方法:")
    print("  from system_monitor import SystemMonitor")
    print("  monitor = SystemMonitor()")
    print("  cpu = monitor.get_cpu_info()")
    print("  memory = monitor.get_memory_info()")
    print()
    print("价格: $19.99")


if __name__ == "__main__":
    main()
