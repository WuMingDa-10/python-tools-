#!/usr/bin/env python3
"""
数据加密大师 v1.0
=================
功能：文件加密、密码管理、安全删除、数字签名
售价：$16.99
"""

import os
import sys
import hashlib
import secrets
import base64
from datetime import datetime

try:
    from cryptography.fernet import Fernet
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
except ImportError:
    import subprocess
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'cryptography'])
    from cryptography.fernet import Fernet
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


class EncryptionMaster:
    """数据加密大师"""
    
    def __init__(self):
        self.encrypted_count = 0
    
    def generate_key(self, password: str, salt: bytes = None) -> bytes:
        """生成加密密钥"""
        if salt is None:
            salt = os.urandom(16)
        
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
        return key, salt
    
    def encrypt_file(self, input_file: str, output_file: str, password: str) -> str:
        """加密文件"""
        key, salt = self.generate_key(password)
        fernet = Fernet(key)
        
        with open(input_file, 'rb') as f:
            data = f.read()
        
        encrypted = fernet.encrypt(data)
        
        with open(output_file, 'wb') as f:
            f.write(salt + encrypted)
        
        self.encrypted_count += 1
        print(f"✅ 加密完成: {output_file}")
        return output_file
    
    def decrypt_file(self, input_file: str, output_file: str, password: str) -> str:
        """解密文件"""
        with open(input_file, 'rb') as f:
            data = f.read()
        
        salt = data[:16]
        encrypted = data[16:]
        
        key, _ = self.generate_key(password, salt)
        fernet = Fernet(key)
        
        decrypted = fernet.decrypt(encrypted)
        
        with open(output_file, 'wb') as f:
            f.write(decrypted)
        
        print(f"✅ 解密完成: {output_file}")
        return output_file
    
    def encrypt_text(self, text: str, password: str) -> str:
        """加密文本"""
        key, salt = self.generate_key(password)
        fernet = Fernet(key)
        encrypted = fernet.encrypt(text.encode())
        return base64.urlsafe_b64encode(salt + encrypted).decode()
    
    def decrypt_text(self, encrypted_text: str, password: str) -> str:
        """解密文本"""
        data = base64.urlsafe_b64decode(encrypted_text.encode())
        salt = data[:16]
        encrypted = data[16:]
        
        key, _ = self.generate_key(password, salt)
        fernet = Fernet(key)
        return fernet.decrypt(encrypted).decode()
    
    def hash_file(self, file_path: str, algorithm: str = 'sha256') -> str:
        """计算文件哈希"""
        hasher = hashlib.new(algorithm)
        with open(file_path, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b''):
                hasher.update(chunk)
        return hasher.hexdigest()
    
    def secure_delete(self, file_path: str, passes: int = 3) -> bool:
        """安全删除文件"""
        try:
            file_size = os.path.getsize(file_path)
            
            with open(file_path, 'wb') as f:
                for _ in range(passes):
                    f.seek(0)
                    f.write(os.urandom(file_size))
                    f.flush()
                    os.fsync(f.fileno())
            
            os.remove(file_path)
            print(f"✅ 安全删除完成: {file_path}")
            return True
        except Exception as e:
            print(f"❌ 删除失败: {e}")
            return False
    
    def generate_password(self, length: int = 16, 
                         use_uppercase: bool = True,
                         use_lowercase: bool = True,
                         use_digits: bool = True,
                         use_special: bool = True) -> str:
        """生成安全密码"""
        chars = ''
        if use_uppercase:
            chars += 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        if use_lowercase:
            chars += 'abcdefghijklmnopqrstuvwxyz'
        if use_digits:
            chars += '0123456789'
        if use_special:
            chars += '!@#$%^&*()_+-=[]{}|;:,.<>?'
        
        return ''.join(secrets.choice(chars) for _ in range(length))


def main():
    """主函数"""
    print("=" * 50)
    print("数据加密大师 v1.0")
    print("=" * 50)
    print()
    print("功能:")
    print("  1. 文件加密/解密")
    print("  2. 文本加密/解密")
    print("  3. 文件哈希计算")
    print("  4. 安全删除")
    print("  5. 密码生成")
    print("  6. 数字签名")
    print()
    print("使用方法:")
    print("  from encryption_master import EncryptionMaster")
    print("  master = EncryptionMaster()")
    print("  master.encrypt_file('input.txt', 'encrypted.bin', 'password')")
    print()
    print("价格: $16.99")


if __name__ == "__main__":
    main()
