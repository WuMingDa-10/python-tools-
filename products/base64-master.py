#!/usr/bin/env python3
"""
Base64 编码大师 v1.0
====================
功能：Base64 编码/解码、批量处理、文件编码
售价：$7.99
"""

import os
import sys
import base64
import json
from datetime import datetime


class Base64Master:
    """Base64 编码大师"""
    
    def __init__(self):
        self.encoded_count = 0
    
    def encode_string(self, text: str) -> str:
        """编码字符串"""
        encoded = base64.b64encode(text.encode('utf-8')).decode('utf-8')
        self.encoded_count += 1
        return encoded
    
    def decode_string(self, encoded: str) -> str:
        """解码字符串"""
        decoded = base64.b64decode(encoded.encode('utf-8')).decode('utf-8')
        return decoded
    
    def encode_file(self, input_file: str, output_file: str = None) -> str:
        """编码文件"""
        with open(input_file, 'rb') as f:
            data = f.read()
        
        encoded = base64.b64encode(data).decode('utf-8')
        
        if output_file:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(encoded)
            print(f"✅ 编码完成: {output_file}")
        
        self.encoded_count += 1
        return encoded
    
    def decode_file(self, encoded_file: str, output_file: str) -> str:
        """解码文件"""
        with open(encoded_file, 'r', encoding='utf-8') as f:
            encoded = f.read()
        
        decoded = base64.b64decode(encoded.encode('utf-8'))
        
        with open(output_file, 'wb') as f:
            f.write(decoded)
        
        print(f"✅ 解码完成: {output_file}")
        return output_file
    
    def encode_url(self, text: str) -> str:
        """URL 安全编码"""
        encoded = base64.urlsafe_b64encode(text.encode('utf-8')).decode('utf-8')
        return encoded
    
    def decode_url(self, encoded: str) -> str:
        """URL 安全解码"""
        decoded = base64.urlsafe_b64decode(encoded.encode('utf-8')).decode('utf-8')
        return decoded
    
    def batch_encode(self, input_dir: str, output_dir: str) -> list:
        """批量编码"""
        os.makedirs(output_dir, exist_ok=True)
        output_files = []
        
        for filename in os.listdir(input_dir):
            input_path = os.path.join(input_dir, filename)
            output_path = os.path.join(output_dir, f"{filename}.b64")
            
            if os.path.isfile(input_path):
                self.encode_file(input_path, output_path)
                output_files.append(output_path)
        
        print(f"✅ 批量编码完成: {len(output_files)} 个文件")
        return output_files
    
    def batch_decode(self, input_dir: str, output_dir: str) -> list:
        """批量解码"""
        os.makedirs(output_dir, exist_ok=True)
        output_files = []
        
        for filename in os.listdir(input_dir):
            if filename.endswith('.b64'):
                input_path = os.path.join(input_dir, filename)
                output_path = os.path.join(output_dir, filename[:-4])
                
                self.decode_file(input_path, output_path)
                output_files.append(output_path)
        
        print(f"✅ 批量解码完成: {len(output_files)} 个文件")
        return output_files
    
    def encode_image(self, image_file: str) -> str:
        """编码图片为 Base64"""
        with open(image_file, 'rb') as f:
            data = f.read()
        
        encoded = base64.b64encode(data).decode('utf-8')
        
        # 获取 MIME 类型
        ext = os.path.splitext(image_file)[1].lower()
        mime_types = {
            '.jpg': 'image/jpeg',
            '.jpeg': 'image/jpeg',
            '.png': 'image/png',
            '.gif': 'image/gif',
            '.webp': 'image/webp',
        }
        mime = mime_types.get(ext, 'application/octet-stream')
        
        return f"data:{mime};base64,{encoded}"
    
    def decode_image(self, data_uri: str, output_file: str) -> str:
        """解码 Data URI 为图片"""
        # 提取 Base64 数据
        if ',' in data_uri:
            data_uri = data_uri.split(',')[1]
        
        decoded = base64.b64decode(data_uri)
        
        with open(output_file, 'wb') as f:
            f.write(decoded)
        
        print(f"✅ 解码完成: {output_file}")
        return output_file
    
    def generate_data_uri(self, file_path: str) -> str:
        """生成 Data URI"""
        with open(file_path, 'rb') as f:
            data = f.read()
        
        encoded = base64.b64encode(data).decode('utf-8')
        
        # 获取 MIME 类型
        ext = os.path.splitext(file_path)[1].lower()
        mime_types = {
            '.html': 'text/html',
            '.css': 'text/css',
            '.js': 'application/javascript',
            '.json': 'application/json',
            '.png': 'image/png',
            '.jpg': 'image/jpeg',
            '.jpeg': 'image/jpeg',
            '.gif': 'image/gif',
            '.svg': 'image/svg+xml',
        }
        mime = mime_types.get(ext, 'application/octet-stream')
        
        return f"data:{mime};base64,{encoded}"


def main():
    """主函数"""
    print("=" * 50)
    print("Base64 编码大师 v1.0")
    print("=" * 50)
    print()
    print("功能:")
    print("  1. 字符串编码/解码")
    print("  2. 文件编码/解码")
    print("  3. URL 安全编码")
    print("  4. 批量处理")
    print("  5. 图片编码")
    print("  6. Data URI 生成")
    print()
    print("使用方法:")
    print("  from base64_master import Base64Master")
    print("  master = Base64Master()")
    print("  encoded = master.encode_string('Hello World')")
    print("  decoded = master.decode_string(encoded)")
    print()
    print("价格: $7.99")


if __name__ == "__main__":
    main()
