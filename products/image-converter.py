#!/usr/bin/env python3
"""
图片格式转换大师 v1.0
=====================
功能：批量转换、压缩、调整大小、添加水印
售价：$10.99
"""

import os
import sys
from datetime import datetime

try:
    from PIL import Image
except ImportError:
    import subprocess
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'Pillow'])
    from PIL import Image


class ImageConverterMaster:
    """图片格式转换大师"""
    
    def __init__(self):
        self.converted = 0
    
    def convert_format(self, input_file: str, output_file: str, 
                       target_format: str = 'PNG') -> str:
        """转换格式"""
        img = Image.open(input_file)
        
        if img.mode == 'RGBA' and target_format == 'JPEG':
            img = img.convert('RGB')
        
        img.save(output_file, target_format)
        self.converted += 1
        print(f"✅ 转换完成: {output_file}")
        return output_file
    
    def batch_convert(self, input_dir: str, output_dir: str, 
                      target_format: str = 'PNG') -> list:
        """批量转换"""
        os.makedirs(output_dir, exist_ok=True)
        output_files = []
        
        for filename in os.listdir(input_dir):
            if filename.lower().endswith(('.jpg', '.jpeg', '.png', '.webp', '.bmp', '.gif')):
                input_path = os.path.join(input_dir, filename)
                name = os.path.splitext(filename)[0]
                output_path = os.path.join(output_dir, f"{name}.{target_format.lower()}")
                
                try:
                    self.convert_format(input_path, output_path, target_format)
                    output_files.append(output_path)
                except Exception as e:
                    print(f"❌ 转换失败: {filename} - {e}")
        
        print(f"✅ 批量转换完成: {len(output_files)} 个文件")
        return output_files
    
    def compress_image(self, input_file: str, output_file: str, 
                       quality: int = 85) -> str:
        """压缩图片"""
        img = Image.open(input_file)
        
        if img.mode == 'RGBA':
            img = img.convert('RGB')
        
        img.save(output_file, quality=quality, optimize=True)
        
        original_size = os.path.getsize(input_file)
        compressed_size = os.path.getsize(output_file)
        ratio = (1 - compressed_size / original_size) * 100
        
        print(f"✅ 压缩完成: {output_file}")
        print(f"   原始大小: {original_size / 1024:.1f} KB")
        print(f"   压缩后: {compressed_size / 1024:.1f} KB")
        print(f"   压缩率: {ratio:.1f}%")
        
        return output_file
    
    def batch_compress(self, input_dir: str, output_dir: str, 
                       quality: int = 85) -> list:
        """批量压缩"""
        os.makedirs(output_dir, exist_ok=True)
        output_files = []
        
        for filename in os.listdir(input_dir):
            if filename.lower().endswith(('.jpg', '.jpeg', '.png', '.webp')):
                input_path = os.path.join(input_dir, filename)
                output_path = os.path.join(output_dir, filename)
                
                try:
                    self.compress_image(input_path, output_path, quality)
                    output_files.append(output_path)
                except Exception as e:
                    print(f"❌ 压缩失败: {filename} - {e}")
        
        print(f"✅ 批量压缩完成: {len(output_files)} 个文件")
        return output_files
    
    def resize_image(self, input_file: str, output_file: str, 
                     width: int = 800, height: int = 600) -> str:
        """调整大小"""
        img = Image.open(input_file)
        img = img.resize((width, height), Image.Resampling.LANCZOS)
        img.save(output_file)
        print(f"✅ 调整完成: {output_file}")
        return output_file
    
    def batch_resize(self, input_dir: str, output_dir: str, 
                     width: int = 800, height: int = 600) -> list:
        """批量调整大小"""
        os.makedirs(output_dir, exist_ok=True)
        output_files = []
        
        for filename in os.listdir(input_dir):
            if filename.lower().endswith(('.jpg', '.jpeg', '.png', '.webp')):
                input_path = os.path.join(input_dir, filename)
                output_path = os.path.join(output_dir, filename)
                
                try:
                    self.resize_image(input_path, output_path, width, height)
                    output_files.append(output_path)
                except Exception as e:
                    print(f"❌ 调整失败: {filename} - {e}")
        
        print(f"✅ 批量调整完成: {len(output_files)} 个文件")
        return output_files
    
    def add_watermark(self, input_file: str, output_file: str, 
                      watermark_text: str) -> str:
        """添加水印"""
        from PIL import ImageDraw, ImageFont
        
        img = Image.open(input_file)
        draw = ImageDraw.Draw(img)
        
        try:
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 36)
        except:
            font = ImageFont.load_default()
        
        # 计算文字位置
        bbox = draw.textbbox((0, 0), watermark_text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        x = img.width - text_width - 20
        y = img.height - text_height - 20
        
        # 绘制水印
        draw.text((x, y), watermark_text, fill=(255, 255, 255, 128), font=font)
        img.save(output_file)
        
        print(f"✅ 水印添加完成: {output_file}")
        return output_file
    
    def rotate_image(self, input_file: str, output_file: str, 
                     angle: int = 90) -> str:
        """旋转图片"""
        img = Image.open(input_file)
        img = img.rotate(angle, expand=True)
        img.save(output_file)
        print(f"✅ 旋转完成: {output_file}")
        return output_file
    
    def flip_image(self, input_file: str, output_file: str, 
                   direction: str = 'horizontal') -> str:
        """翻转图片"""
        img = Image.open(input_file)
        
        if direction == 'horizontal':
            img = img.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
        elif direction == 'vertical':
            img = img.transpose(Image.Transpose.FLIP_TOP_BOTTOM)
        
        img.save(output_file)
        print(f"✅ 翻转完成: {output_file}")
        return output_file
    
    def get_image_info(self, input_file: str) -> dict:
        """获取图片信息"""
        img = Image.open(input_file)
        
        return {
            'filename': os.path.basename(input_file),
            'format': img.format,
            'mode': img.mode,
            'size': img.size,
            'width': img.width,
            'height': img.height,
            'file_size': os.path.getsize(input_file),
        }


def main():
    """主函数"""
    print("=" * 50)
    print("图片格式转换大师 v1.0")
    print("=" * 50)
    print()
    print("功能:")
    print("  1. 格式转换")
    print("  2. 批量转换")
    print("  3. 压缩图片")
    print("  4. 调整大小")
    print("  5. 添加水印")
    print("  6. 旋转翻转")
    print()
    print("使用方法:")
    print("  from image_converter import ImageConverterMaster")
    print("  master = ImageConverterMaster()")
    print("  master.convert_format('input.jpg', 'output.png', 'PNG')")
    print()
    print("价格: $10.99")


if __name__ == "__main__":
    main()
