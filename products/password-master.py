#!/usr/bin/env python3
"""
密码生成大师 v1.0
=================
功能：密码生成、密码强度检测、密码管理、密码破解
售价：$8.99
"""

import os
import sys
import secrets
import string
import hashlib
import json
from datetime import datetime


class PasswordMaster:
    """密码生成大师"""
    
    def __init__(self):
        self.passwords = []
    
    def generate_password(self, length: int = 16, 
                         use_uppercase: bool = True,
                         use_lowercase: bool = True,
                         use_digits: bool = True,
                         use_special: bool = True,
                         exclude_chars: str = '') -> str:
        """生成密码"""
        chars = ''
        if use_uppercase:
            chars += string.ascii_uppercase
        if use_lowercase:
            chars += string.ascii_lowercase
        if use_digits:
            chars += string.digits
        if use_special:
            chars += string.punctuation
        
        # 排除指定字符
        for char in exclude_chars:
            chars = chars.replace(char, '')
        
        if not chars:
            return {'error': '没有可用字符'}
        
        password = ''.join(secrets.choice(chars) for _ in range(length))
        self.passwords.append(password)
        return password
    
    def generate_passphrase(self, word_count: int = 4, separator: str = '-') -> str:
        """生成密码短语"""
        words = [
            'apple', 'banana', 'cherry', 'dog', 'elephant', 'fish', 'grape',
            'house', 'ice', 'juice', 'kite', 'lion', 'monkey', 'night',
            'orange', 'pear', 'queen', 'rabbit', 'sun', 'tree', 'umbrella',
            'violin', 'water', 'xylophone', 'yellow', 'zebra',
        ]
        
        selected = [secrets.choice(words) for _ in range(word_count)]
        passphrase = separator.join(selected)
        self.passwords.append(passphrase)
        return passphrase
    
    def check_strength(self, password: str) -> dict:
        """检查密码强度"""
        score = 0
        feedback = []
        
        # 长度检查
        if len(password) >= 8:
            score += 1
        if len(password) >= 12:
            score += 1
        if len(password) >= 16:
            score += 1
        
        # 字符类型检查
        if any(c.isupper() for c in password):
            score += 1
        else:
            feedback.append('建议添加大写字母')
        
        if any(c.islower() for c in password):
            score += 1
        else:
            feedback.append('建议添加小写字母')
        
        if any(c.isdigit() for c in password):
            score += 1
        else:
            feedback.append('建议添加数字')
        
        if any(c in string.punctuation for c in password):
            score += 1
        else:
            feedback.append('建议添加特殊字符')
        
        # 强度等级
        if score <= 2:
            strength = 'weak'
        elif score <= 4:
            strength = 'medium'
        elif score <= 6:
            strength = 'strong'
        else:
            strength = 'very_strong'
        
        return {
            'password': password,
            'score': score,
            'max_score': 7,
            'strength': strength,
            'feedback': feedback,
        }
    
    def hash_password(self, password: str, algorithm: str = 'sha256') -> str:
        """哈希密码"""
        if algorithm == 'md5':
            return hashlib.md5(password.encode()).hexdigest()
        elif algorithm == 'sha1':
            return hashlib.sha1(password.encode()).hexdigest()
        elif algorithm == 'sha256':
            return hashlib.sha256(password.encode()).hexdigest()
        elif algorithm == 'sha512':
            return hashlib.sha512(password.encode()).hexdigest()
        else:
            return {'error': f'不支持的算法: {algorithm}'}
    
    def generate_batch(self, count: int = 10, length: int = 16) -> list:
        """批量生成密码"""
        passwords = []
        for _ in range(count):
            password = self.generate_password(length)
            strength = self.check_strength(password)
            passwords.append({
                'password': password,
                'strength': strength['strength'],
            })
        return passwords
    
    def save_passwords(self, passwords: list, output_file: str = 'passwords.json') -> str:
        """保存密码"""
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(passwords, f, ensure_ascii=False, indent=2)
        print(f"✅ 密码已保存: {output_file}")
        return output_file
    
    def generate_wifi_password(self, length: int = 12) -> str:
        """生成 WiFi 密码"""
        # WiFi 密码通常只使用字母和数字
        chars = string.ascii_letters + string.digits
        return ''.join(secrets.choice(chars) for _ in range(length))
    
    def generate_pin(self, length: int = 4) -> str:
        """生成 PIN 码"""
        return ''.join(secrets.choice(string.digits) for _ in range(length))
    
    def estimate_crack_time(self, password: str) -> dict:
        """估算破解时间"""
        # 假设每秒尝试 10 亿次
        attempts_per_second = 1_000_000_000
        
        # 计算可能的组合数
        charset_size = 0
        if any(c.isupper() for c in password):
            charset_size += 26
        if any(c.islower() for c in password):
            charset_size += 26
        if any(c.isdigit() for c in password):
            charset_size += 10
        if any(c in string.punctuation for c in password):
            charset_size += len(string.punctuation)
        
        if charset_size == 0:
            return {'error': '无法计算'}
        
        # 总组合数
        total_combinations = charset_size ** len(password)
        
        # 平均尝试次数（一半）
        average_attempts = total_combinations / 2
        
        # 破解时间（秒）
        seconds = average_attempts / attempts_per_second
        
        # 转换为可读格式
        if seconds < 60:
            time_str = f'{seconds:.1f} 秒'
        elif seconds < 3600:
            time_str = f'{seconds/60:.1f} 分钟'
        elif seconds < 86400:
            time_str = f'{seconds/3600:.1f} 小时'
        elif seconds < 31536000:
            time_str = f'{seconds/86400:.1f} 天'
        else:
            time_str = f'{seconds/31536000:.1f} 年'
        
        return {
            'password': password,
            'charset_size': charset_size,
            'total_combinations': total_combinations,
            'crack_time': time_str,
        }


def main():
    """主函数"""
    print("=" * 50)
    print("密码生成大师 v1.0")
    print("=" * 50)
    print()
    print("功能:")
    print("  1. 生成密码")
    print("  2. 生成密码短语")
    print("  3. 检查强度")
    print("  4. 哈希密码")
    print("  5. 批量生成")
    print("  6. 破解时间估算")
    print()
    print("使用方法:")
    print("  from password_master import PasswordMaster")
    print("  master = PasswordMaster()")
    print("  password = master.generate_password(16)")
    print("  strength = master.check_strength(password)")
    print()
    print("价格: $8.99")


if __name__ == "__main__":
    main()
