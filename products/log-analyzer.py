#!/usr/bin/env python3
"""
日志分析大师 v1.0
=================
功能：日志解析、统计分析、告警检测、可视化
售价：$18.99
"""

import os
import sys
import re
import json
from datetime import datetime
from collections import Counter, defaultdict


class LogAnalyzer:
    """日志分析大师"""
    
    def __init__(self):
        self.logs = []
        self.errors = []
        self.warnings = []
    
    def parse_log_file(self, log_file: str, pattern: str = None) -> list:
        """解析日志文件"""
        logs = []
        
        with open(log_file, 'r', encoding='utf-8', errors='ignore') as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip()
                if not line:
                    continue
                
                log_entry = {
                    'line_number': line_num,
                    'content': line,
                    'timestamp': self._extract_timestamp(line),
                    'level': self._extract_level(line),
                }
                logs.append(log_entry)
                
                # 分类
                if log_entry['level'] == 'ERROR':
                    self.errors.append(log_entry)
                elif log_entry['level'] == 'WARNING':
                    self.warnings.append(log_entry)
        
        self.logs.extend(logs)
        print(f"✅ 解析完成: {len(logs)} 条日志")
        return logs
    
    def _extract_timestamp(self, line: str) -> str:
        """提取时间戳"""
        patterns = [
            r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}',
            r'\d{2}/\d{2}/\d{4} \d{2}:\d{2}:\d{2}',
            r'\w{3} \d{2} \d{2}:\d{2}:\d{2}',
        ]
        for pattern in patterns:
            match = re.search(pattern, line)
            if match:
                return match.group()
        return None
    
    def _extract_level(self, line: str) -> str:
        """提取日志级别"""
        line_upper = line.upper()
        if 'ERROR' in line_upper or 'ERR' in line_upper:
            return 'ERROR'
        elif 'WARNING' in line_upper or 'WARN' in line_upper:
            return 'WARNING'
        elif 'INFO' in line_upper:
            return 'INFO'
        elif 'DEBUG' in line_upper:
            return 'DEBUG'
        return 'UNKNOWN'
    
    def get_statistics(self) -> dict:
        """获取统计信息"""
        level_counts = Counter(log['level'] for log in self.logs)
        
        return {
            'total_logs': len(self.logs),
            'errors': len(self.errors),
            'warnings': len(self.warnings),
            'level_distribution': dict(level_counts),
            'first_timestamp': self.logs[0]['timestamp'] if self.logs else None,
            'last_timestamp': self.logs[-1]['timestamp'] if self.logs else None,
        }
    
    def search_logs(self, keyword: str, case_sensitive: bool = False) -> list:
        """搜索日志"""
        results = []
        for log in self.logs:
            content = log['content']
            if not case_sensitive:
                content = content.lower()
                keyword = keyword.lower()
            
            if keyword in content:
                results.append(log)
        
        print(f"✅ 搜索完成: 找到 {len(results)} 条匹配")
        return results
    
    def filter_by_level(self, level: str) -> list:
        """按级别过滤"""
        return [log for log in self.logs if log['level'] == level.upper()]
    
    def filter_by_time(self, start_time: str = None, end_time: str = None) -> list:
        """按时间过滤"""
        results = []
        for log in self.logs:
            if log['timestamp']:
                if start_time and log['timestamp'] < start_time:
                    continue
                if end_time and log['timestamp'] > end_time:
                    continue
                results.append(log)
        return results
    
    def detect_anomalies(self) -> list:
        """检测异常"""
        anomalies = []
        
        # 检测错误激增
        if len(self.errors) > len(self.logs) * 0.1:
            anomalies.append({
                'type': 'error_spike',
                'message': f'错误率过高: {len(self.errors)}/{len(self.logs)} ({len(self.errors)/len(self.logs)*100:.1f}%)',
                'severity': 'high',
            })
        
        # 检测警告激增
        if len(self.warnings) > len(self.logs) * 0.2:
            anomalies.append({
                'type': 'warning_spike',
                'message': f'警告率过高: {len(self.warnings)}/{len(self.logs)} ({len(self.warnings)/len(self.logs)*100:.1f}%)',
                'severity': 'medium',
            })
        
        print(f"✅ 异常检测完成: 发现 {len(anomalies)} 个异常")
        return anomalies
    
    def generate_report(self, output_file: str = 'log_report.json') -> str:
        """生成分析报告"""
        report = {
            'timestamp': datetime.now().isoformat(),
            'statistics': self.get_statistics(),
            'anomalies': self.detect_anomalies(),
            'top_errors': self.errors[:10],
            'top_warnings': self.warnings[:10],
        }
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        print(f"✅ 报告已生成: {output_file}")
        return output_file
    
    def export_to_csv(self, output_file: str = 'logs.csv') -> str:
        """导出到 CSV"""
        import csv
        
        with open(output_file, 'w', newline='', encoding='utf-8-sig') as f:
            writer = csv.DictWriter(f, fieldnames=['line_number', 'timestamp', 'level', 'content'])
            writer.writeheader()
            writer.writerows(self.logs)
        
        print(f"✅ 导出完成: {output_file}")
        return output_file


def main():
    """主函数"""
    print("=" * 50)
    print("日志分析大师 v1.0")
    print("=" * 50)
    print()
    print("功能:")
    print("  1. 日志解析")
    print("  2. 统计分析")
    print("  3. 关键词搜索")
    print("  4. 级别过滤")
    print("  5. 异常检测")
    print("  6. 报告生成")
    print()
    print("使用方法:")
    print("  from log_analyzer import LogAnalyzer")
    print("  analyzer = LogAnalyzer()")
    print("  analyzer.parse_log_file('access.log')")
    print("  stats = analyzer.get_statistics()")
    print()
    print("价格: $18.99")


if __name__ == "__main__":
    main()
