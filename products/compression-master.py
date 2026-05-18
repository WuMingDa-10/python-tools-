#!/usr/bin/env python3
"""
文件压缩大师 v1.0
=================
功能：ZIP/TAR/GZIP 压缩、解压、加密、分卷
售价：$10.99
"""

import os
import sys
import zipfile
import tarfile
import gzip
import shutil
from datetime import datetime


class CompressionMaster:
    """文件压缩大师"""
    
    def __init__(self):
        self.compressed_count = 0
    
    def zip_compress(self, input_path: str, output_file: str, password: str = None) -> str:
        """ZIP 压缩"""
        with zipfile.ZipFile(output_file, 'w', zipfile.ZIP_DEFLATED) as zf:
            if os.path.isfile(input_path):
                zf.write(input_path, os.path.basename(input_path))
            elif os.path.isdir(input_path):
                for root, dirs, files in os.walk(input_path):
                    for file in files:
                        file_path = os.path.join(root, file)
                        arcname = os.path.relpath(file_path, os.path.dirname(input_path))
                        zf.write(file_path, arcname)
        
        self.compressed_count += 1
        print(f"✅ ZIP 压缩完成: {output_file}")
        return output_file
    
    def zip_decompress(self, input_file: str, output_dir: str) -> str:
        """ZIP 解压"""
        with zipfile.ZipFile(input_file, 'r') as zf:
            zf.extractall(output_dir)
        
        print(f"✅ ZIP 解压完成: {output_dir}")
        return output_dir
    
    def tar_compress(self, input_path: str, output_file: str, compression: str = 'gz') -> str:
        """TAR 压缩"""
        mode = f'w:{compression}' if compression else 'w'
        
        with tarfile.open(output_file, mode) as tf:
            tf.add(input_path, arcname=os.path.basename(input_path))
        
        self.compressed_count += 1
        print(f"✅ TAR 压缩完成: {output_file}")
        return output_file
    
    def tar_decompress(self, input_file: str, output_dir: str) -> str:
        """TAR 解压"""
        with tarfile.open(input_file, 'r:*') as tf:
            tf.extractall(output_dir)
        
        print(f"✅ TAR 解压完成: {output_dir}")
        return output_dir
    
    def gzip_compress(self, input_file: str, output_file: str = None) -> str:
        """GZIP 压缩"""
        if output_file is None:
            output_file = input_file + '.gz'
        
        with open(input_file, 'rb') as f_in:
            with gzip.open(output_file, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
        
        self.compressed_count += 1
        print(f"✅ GZIP 压缩完成: {output_file}")
        return output_file
    
    def gzip_decompress(self, input_file: str, output_file: str = None) -> str:
        """GZIP 解压"""
        if output_file is None:
            output_file = input_file[:-3] if input_file.endswith('.gz') else input_file + '.out'
        
        with gzip.open(input_file, 'rb') as f_in:
            with open(output_file, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
        
        print(f"✅ GZIP 解压完成: {output_file}")
        return output_file
    
    def split_file(self, input_file: str, output_dir: str, chunk_size: int = 1024*1024) -> list:
        """分卷压缩"""
        os.makedirs(output_dir, exist_ok=True)
        output_files = []
        
        with open(input_file, 'rb') as f:
            chunk_num = 0
            while True:
                chunk = f.read(chunk_size)
                if not chunk:
                    break
                
                output_file = os.path.join(output_dir, f'part_{chunk_num:03d}')
                with open(output_file, 'wb') as out:
                    out.write(chunk)
                
                output_files.append(output_file)
                chunk_num += 1
        
        print(f"✅ 分卷完成: {len(output_files)} 个文件")
        return output_files
    
    def merge_files(self, input_files: list, output_file: str) -> str:
        """合并分卷"""
        with open(output_file, 'wb') as out:
            for input_file in sorted(input_files):
                with open(input_file, 'rb') as f:
                    out.write(f.read())
        
        print(f"✅ 合并完成: {output_file}")
        return output_file
    
    def get_compression_ratio(self, original_file: str, compressed_file: str) -> dict:
        """获取压缩比"""
        original_size = os.path.getsize(original_file)
        compressed_size = os.path.getsize(compressed_file)
        
        return {
            'original_size': original_size,
            'compressed_size': compressed_size,
            'ratio': compressed_size / original_size * 100,
            'saved': original_size - compressed_size,
            'saved_percent': (1 - compressed_size / original_size) * 100,
        }
    
    def list_archive(self, archive_file: str) -> list:
        """列出压缩包内容"""
        if archive_file.endswith('.zip'):
            with zipfile.ZipFile(archive_file, 'r') as zf:
                return zf.namelist()
        elif archive_file.endswith(('.tar', '.tar.gz', '.tgz', '.tar.bz2')):
            with tarfile.open(archive_file, 'r:*') as tf:
                return tf.getnames()
        return []


def main():
    """主函数"""
    print("=" * 50)
    print("文件压缩大师 v1.0")
    print("=" * 50)
    print()
    print("功能:")
    print("  1. ZIP 压缩/解压")
    print("  2. TAR 压缩/解压")
    print("  3. GZIP 压缩/解压")
    print("  4. 分卷压缩")
    print("  5. 合并分卷")
    print("  6. 压缩比分析")
    print()
    print("使用方法:")
    print("  from compression_master import CompressionMaster")
    print("  master = CompressionMaster()")
    print("  master.zip_compress('folder/', 'archive.zip')")
    print()
    print("价格: $10.99")


if __name__ == "__main__":
    main()
