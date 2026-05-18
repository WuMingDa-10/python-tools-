#!/usr/bin/env python3
"""
命令行大师 v1.0
=================
功能：命令行参数解析、交互式命令、进度条、颜色输出
售价：$9.99
"""

import os
import sys
import argparse
import time
from datetime import datetime


class CLIMaster:
    """命令行大师"""
    
    def __init__(self):
        self.parser = None
    
    def create_parser(self, description: str = '') -> argparse.ArgumentParser:
        """创建参数解析器"""
        self.parser = argparse.ArgumentParser(description=description)
        return self.parser
    
    def add_argument(self, name: str, **kwargs):
        """添加参数"""
        if self.parser:
            self.parser.add_argument(name, **kwargs)
    
    def parse_args(self, args: list = None) -> dict:
        """解析参数"""
        if self.parser:
            if args:
                return vars(self.parser.parse_args(args))
            return vars(self.parser.parse_args())
        return {}
    
    def print_color(self, text: str, color: str = 'white'):
        """彩色输出"""
        colors = {
            'red': '\033[91m',
            'green': '\033[92m',
            'yellow': '\033[93m',
            'blue': '\033[94m',
            'purple': '\033[95m',
            'cyan': '\033[96m',
            'white': '\033[97m',
            'reset': '\033[0m',
        }
        
        color_code = colors.get(color, colors['white'])
        reset_code = colors['reset']
        print(f"{color_code}{text}{reset_code}")
    
    def print_success(self, text: str):
        """打印成功信息"""
        self.print_color(f"✅ {text}", 'green')
    
    def print_error(self, text: str):
        """打印错误信息"""
        self.print_color(f"❌ {text}", 'red')
    
    def print_warning(self, text: str):
        """打印警告信息"""
        self.print_color(f"⚠️ {text}", 'yellow')
    
    def print_info(self, text: str):
        """打印信息"""
        self.print_color(f"ℹ️ {text}", 'blue')
    
    def progress_bar(self, total: int, description: str = 'Processing'):
        """进度条"""
        for i in range(total + 1):
            percent = i / total * 100
            bar = '█' * int(percent / 2) + '░' * (50 - int(percent / 2))
            sys.stdout(f'\r{description}: |{bar}| {percent:.1f}%')
            sys.stdout.flush()
            time.sleep(0.05)
        print()
    
    def confirm(self, message: str, default: bool = False) -> bool:
        """确认提示"""
        suffix = ' [Y/n] ' if default else ' [y/N] '
        response = input(message + suffix).strip().lower()
        
        if not response:
            return default
        
        return response in ('y', 'yes')
    
    def select(self, message: str, options: list) -> int:
        """选择提示"""
        print(message)
        for i, option in enumerate(options, 1):
            print(f"  {i}. {option}")
        
        while True:
            try:
                choice = int(input("请选择: "))
                if 1 <= choice <= len(options):
                    return choice - 1
                print("无效选择，请重试")
            except ValueError:
                print("请输入数字")
    
    def input_with_default(self, message: str, default: str = '') -> str:
        """带默认值的输入"""
        if default:
            response = input(f"{message} [{default}]: ").strip()
            return response if response else default
        return input(f"{message}: ").strip()
    
    def table(self, headers: list, rows: list):
        """打印表格"""
        # 计算列宽
        col_widths = [len(str(h)) for h in headers]
        for row in rows:
            for i, cell in enumerate(row):
                col_widths[i] = max(col_widths[i], len(str(cell)))
        
        # 打印表头
        header_line = ' | '.join(str(h).ljust(w) for h, w in zip(headers, col_widths))
        print(header_line)
        print('-' * len(header_line))
        
        # 打印数据行
        for row in rows:
            row_line = ' | '.join(str(cell).ljust(w) for cell, w in zip(row, col_widths))
            print(row_line)
    
    def clear_screen(self):
        """清屏"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def print_banner(self, text: str, char: str = '='):
        """打印横幅"""
        width = len(text) + 4
        print(char * width)
        print(f"{char} {text} {char}")
        print(char * width)
    
    def print_dict(self, data: dict, indent: int = 0):
        """打印字典"""
        for key, value in data.items():
            if isinstance(value, dict):
                print(' ' * indent + f'{key}:')
                self.print_dict(value, indent + 2)
            else:
                print(' ' * indent + f'{key}: {value}')


def main():
    """主函数"""
    print("=" * 50)
    print("命令行大师 v1.0")
    print("=" * 50)
    print()
    print("功能:")
    print("  1. 参数解析")
    print("  2. 彩色输出")
    print("  3. 进度条")
    print("  4. 交互式命令")
    print("  5. 表格打印")
    print("  6. 横幅打印")
    print()
    print("使用方法:")
    print("  from cli_master import CLIMaster")
    print("  cli = CLIMaster()")
    print("  cli.print_success('操作成功')")
    print("  cli.print_error('操作失败')")
    print()
    print("价格: $9.99")


if __name__ == "__main__":
    main()
