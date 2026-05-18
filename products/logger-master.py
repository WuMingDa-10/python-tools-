#!/usr/bin/env python3
"""
日志记录大师 v1.0
=================
功能：日志记录、格式化、轮转、过滤
售价：$8.99
"""

import os
import sys
import logging
from datetime import datetime


class LoggerMaster:
    """日志记录大师"""
    
    def __init__(self, name: str = 'app', level: str = 'INFO'):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(getattr(logging, level.upper()))
        
        # 清除现有处理器
        self.logger.handlers.clear()
    
    def add_console_handler(self, level: str = 'INFO', format: str = None):
        """添加控制台处理器"""
        handler = logging.StreamHandler()
        handler.setLevel(getattr(logging, level.upper()))
        
        if format is None:
            format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        
        formatter = logging.Formatter(format)
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
    
    def add_file_handler(self, file_path: str, level: str = 'INFO', 
                         format: str = None, max_bytes: int = 1024*1024,
                         backup_count: int = 5):
        """添加文件处理器"""
        from logging.handlers import RotatingFileHandler
        
        handler = RotatingFileHandler(
            file_path, 
            maxBytes=max_bytes,
            backupCount=backup_count,
            encoding='utf-8'
        )
        handler.setLevel(getattr(logging, level.upper()))
        
        if format is None:
            format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        
        formatter = logging.Formatter(format)
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
    
    def debug(self, message: str):
        """记录调试信息"""
        self.logger.debug(message)
    
    def info(self, message: str):
        """记录信息"""
        self.logger.info(message)
    
    def warning(self, message: str):
        """记录警告"""
        self.logger.warning(message)
    
    def error(self, message: str):
        """记录错误"""
        self.logger.error(message)
    
    def critical(self, message: str):
        """记录严重错误"""
        self.logger.critical(message)
    
    def exception(self, message: str):
        """记录异常"""
        self.logger.exception(message)
    
    def log_with_context(self, level: str, message: str, **context):
        """带上下文的日志"""
        context_str = ' '.join(f'{k}={v}' for k, v in context.items())
        full_message = f'{message} [{context_str}]' if context_str else message
        
        getattr(self.logger, level.lower())(full_message)
    
    def create_logger(self, name: str, level: str = 'INFO', 
                      console: bool = True, file: str = None) -> 'LoggerMaster':
        """创建日志记录器"""
        logger = LoggerMaster(name, level)
        
        if console:
            logger.add_console_handler(level)
        
        if file:
            logger.add_file_handler(file, level)
        
        return logger
    
    def set_level(self, level: str):
        """设置日志级别"""
        self.logger.setLevel(getattr(logging, level.upper()))
    
    def get_logger(self) -> logging.Logger:
        """获取日志记录器"""
        return self.logger


def main():
    """主函数"""
    print("=" * 50)
    print("日志记录大师 v1.0")
    print("=" * 50)
    print()
    print("功能:")
    print("  1. 日志记录")
    print("  2. 格式化输出")
    print("  3. 文件轮转")
    print("  4. 多级别支持")
    print("  5. 上下文日志")
    print("  6. 日志过滤")
    print()
    print("使用方法:")
    print("  from logger_master import LoggerMaster")
    print("  logger = LoggerMaster('myapp', 'DEBUG')")
    print("  logger.add_console_handler()")
    print("  logger.info('应用启动')")
    print()
    print("价格: $8.99")


if __name__ == "__main__":
    main()
