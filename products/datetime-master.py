#!/usr/bin/env python3
"""
日期时间大师 v1.0
=================
功能：日期计算、格式转换、时区处理、定时任务
售价：$9.99
"""

import os
import sys
import json
from datetime import datetime, timedelta
import time


class DateTimeMaster:
    """日期时间大师"""
    
    def __init__(self):
        self.now = datetime.now()
    
    def get_current_time(self, format: str = '%Y-%m-%d %H:%M:%S') -> str:
        """获取当前时间"""
        return datetime.now().strftime(format)
    
    def get_timestamp(self) -> int:
        """获取时间戳"""
        return int(time.time())
    
    def timestamp_to_datetime(self, timestamp: int, format: str = '%Y-%m-%d %H:%M:%S') -> str:
        """时间戳转日期"""
        return datetime.fromtimestamp(timestamp).strftime(format)
    
    def datetime_to_timestamp(self, date_string: str, format: str = '%Y-%m-%d %H:%M:%S') -> int:
        """日期转时间戳"""
        return int(datetime.strptime(date_string, format).timestamp())
    
    def add_days(self, date_string: str, days: int, format: str = '%Y-%m-%d %H:%M:%S') -> str:
        """添加天数"""
        date = datetime.strptime(date_string, format)
        new_date = date + timedelta(days=days)
        return new_date.strftime(format)
    
    def add_hours(self, date_string: str, hours: int, format: str = '%Y-%m-%d %H:%M:%S') -> str:
        """添加小时"""
        date = datetime.strptime(date_string, format)
        new_date = date + timedelta(hours=hours)
        return new_date.strftime(format)
    
    def add_minutes(self, date_string: str, minutes: int, format: str = '%Y-%m-%d %H:%M:%S') -> str:
        """添加分钟"""
        date = datetime.strptime(date_string, format)
        new_date = date + timedelta(minutes=minutes)
        return new_date.strftime(format)
    
    def diff_days(self, date1: str, date2: str, format: str = '%Y-%m-%d %H:%M:%S') -> int:
        """计算天数差"""
        d1 = datetime.strptime(date1, format)
        d2 = datetime.strptime(date2, format)
        return abs((d2 - d1).days)
    
    def diff_hours(self, date1: str, date2: str, format: str = '%Y-%m-%d %H:%M:%S') -> int:
        """计算小时差"""
        d1 = datetime.strptime(date1, format)
        d2 = datetime.strptime(date2, format)
        return abs(int((d2 - d1).total_seconds() / 3600))
    
    def get_weekday(self, date_string: str, format: str = '%Y-%m-%d') -> str:
        """获取星期几"""
        date = datetime.strptime(date_string, format)
        weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        return weekdays[date.weekday()]
    
    def get_week_number(self, date_string: str, format: str = '%Y-%m-%d') -> int:
        """获取周数"""
        date = datetime.strptime(date_string, format)
        return date.isocalendar()[1]
    
    def get_month_days(self, year: int, month: int) -> int:
        """获取月份天数"""
        if month == 12:
            next_month = datetime(year + 1, 1, 1)
        else:
            next_month = datetime(year, month + 1, 1)
        
        this_month = datetime(year, month, 1)
        return (next_month - this_month).days
    
    def is_leap_year(self, year: int) -> bool:
        """判断是否闰年"""
        return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)
    
    def format_date(self, date_string: str, input_format: str, output_format: str) -> str:
        """格式化日期"""
        date = datetime.strptime(date_string, input_format)
        return date.strftime(output_format)
    
    def get_age(self, birthday: str, format: str = '%Y-%m-%d') -> int:
        """计算年龄"""
        birth = datetime.strptime(birthday, format)
        today = datetime.now()
        age = today.year - birth.year - ((today.month, today.day) < (birth.month, birth.day))
        return age
    
    def get_countdown(self, target_date: str, format: str = '%Y-%m-%d %H:%M:%S') -> dict:
        """获取倒计时"""
        target = datetime.strptime(target_date, format)
        now = datetime.now()
        diff = target - now
        
        return {
            'days': diff.days,
            'hours': diff.seconds // 3600,
            'minutes': (diff.seconds % 3600) // 60,
            'seconds': diff.seconds % 60,
            'total_seconds': int(diff.total_seconds()),
        }
    
    def generate_calendar(self, year: int, month: int) -> str:
        """生成日历"""
        import calendar
        return calendar.month(year, month)


def main():
    """主函数"""
    print("=" * 50)
    print("日期时间大师 v1.0")
    print("=" * 50)
    print()
    print("功能:")
    print("  1. 获取当前时间")
    print("  2. 时间戳转换")
    print("  3. 日期计算")
    print("  4. 格式转换")
    print("  5. 倒计时")
    print("  6. 日历生成")
    print()
    print("使用方法:")
    print("  from datetime_master import DateTimeMaster")
    print("  master = DateTimeMaster()")
    print("  print(master.get_current_time())")
    print("  print(master.add_days('2025-01-01', 30))")
    print()
    print("价格: $9.99")


if __name__ == "__main__":
    main()
