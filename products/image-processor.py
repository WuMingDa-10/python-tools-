#!/usr/bin/env python3
"""
图片批量处理大师 v1.0
=====================
功能：批量压缩、格式转换、水印、裁剪、滤镜
售价：$12.99
"""

import os
import sys
from pathlib import Path

try:
    from PIL import Image, ImageDraw, ImageFont, ImageFilter
except ImportError:
    import subprocess
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'Pillow'])
    from PIL import Image, ImageDraw, ImageFont, ImageFilter


class ImageProcessor:
    """图片批量处理大师"""
    
    def __init__(self):
        self.processed = 0
    
    def batch_compress(self, input_dir: str, output_dir: str, quality: int = 85) -> list:
        """批量压缩图片"""
        os.makedirs(output_dir, exist_ok=True)
        output_files = []
        
        for filename in os.listdir(input_dir):
            if filename.lower().endswith(('.jpg', '.jpeg', '.png', '.webp')):
                input_path = os.path.join(input_dir, filename)
                output_path = os.path.join(output_dir, filename)
                
                img = Image.open(input_path)
                if img.mode == 'RGBA':
                    img = img.convert('RGB')
                
                img.save(output_path, quality=quality, optimize=True)
                output_files.append(output_path)
                self.processed += 1
        
        print(f"✅ 压缩完成: {self.processed} 张图片")
        return output_files
    
    def batch_convert(self, input_dir: str, output_dir: str, target_format: str = 'PNG') -> list:
        """批量转换格式"""
        os.makedirs(output_dir, exist_ok=True)
        output_files = []
        
        for filename in os.listdir(input_dir):
            if filename.lower().endswith(('.jpg', '.jpeg', '.png', '.webp', '.bmp', '.gif')):
                input_path = os.path.join(input_dir, filename)
                name = os.path.splitext(filename)[0]
                output_path = os.path.join(output_dir, f"{name}.{target_format.lower()}")
                
                img = Image.open(input_path)
                if img.mode == 'RGBA' and target_format == 'JPEG':
                    img = img.convert('RGB')
                
                img.save(output_path)
                output_files.append(output_path)
                self.processed += 1
        
        print(f"✅ 转换完成: {self.processed} 张图片")
        return output_files
    
    def batch_resize(self, input_dir: str, output_dir: str, width: int = 800, height: int = 600) -> list:
        """批量调整尺寸"""
        os.makedirs(output_dir, exist_ok=True)
        output_files = []
        
        for filename in os.listdir(input_dir):
            if filename.lower().endswith(('.jpg', '.jpeg', '.png', '.webp')):
                input_path = os.path.join(input_dir, filename)
                output_path = os.path.join(output_dir, filename)
                
                img = Image.open(input_path)
                img = img.resize((width, height), Image.Resampling.LANCZOS)
                img.save(output_path)
                output_files.append(output_path)
                self.processed += 1
        
        print(f"✅ 调整完成: {self.processed} 张图片")
        return output_files
    
    def add_watermark(self, input_dir: str, output_dir: str, watermark_text: str) -> list:
        """批量添加水印"""
        os.makedirs(output_dir, exist_ok=True)
        output_files = []
        
        for filename in os.listdir(input_dir):
            if filename.lower().endswith(('.jpg', '.jpeg', '.png', '.webp')):
                input_path = os.path.join(input_dir, filename)
                output_path = os.path.join(output_dir, filename)
                
                img = Image.open(input_path)
                draw = ImageDraw.Draw(img)
                
                # 使用默认字体
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
                img.save(output_path)
                output_files.append(output_path)
                self.processed += 1
        
        print(f"✅ 水印添加完成: {self.processed} 张图片")
        return output_files
    
    def batch_crop(self, input_dir: str, output_dir: str, left: int = 0, top: int = 0, right: int = 800, bottom: int = 600) -> list:
        """批量裁剪"""
        os.makedirs(output_dir, exist_ok=True)
        output_files = []
        
        for filename in os.listdir(input_dir):
            if filename.lower().endswith(('.jpg', '.jpeg', '.png', '.webp')):
                input_path = os.path.join(input_dir, filename)
                output_path = os.path.join(output_dir, filename)
                
                img = Image.open(input_path)
                img = img.crop((left, top, right, bottom))
                img.save(output_path)
                output_files.append(output_path)
                self.processed += 1
        
        print(f"✅ 裁剪完成: {self.processed} 张图片")
        return output_files
    
    def apply_filter(self, input_dir: str, output_dir: str, filter_type: str = 'blur') -> list:
        """批量应用滤镜"""
        os.makedirs(output_dir, exist_ok=True)
        output_files = []
        
        filters = {
            'blur': ImageFilter.BLUR,
            'sharpen': ImageFilter.SHARPEN,
            'emboss': ImageFilter.EMBOSS,
            'edge': ImageFilter.FIND_EDGES,
        }
        
        for filename in os.listdir(input_dir):
            if filename.lower().endswith(('.jpg', '.jpeg', '.png', '.webp')):
                input_path = os.path.join(input_dir, filename)
                output_path = os.path.join(output_dir, filename)
                
                img = Image.open(input_path)
                img = img.filter(filters.get(filter_type, ImageFilter.BLUR))
                img.save(output_path)
                output_files.append(output_path)
                self.processed += 1
        
        print(f"✅ 滤镜应用完成: {self.processed} 张图片")
        return output_files


def main():
    """主函数"""
    print("=" * 50)
    print("图片批量处理大师 v1.0")
    print("=" * 50)
    print()
    print("功能:")
    print("  1. 批量压缩")
    print("  2. 格式转换")
    print("  3. 调整尺寸")
    print("  4. 添加水印")
    print("  5. 批量裁剪")
    print("  6. 应用滤镜")
    print()
    print("使用方法:")
    print("  from image_processor import ImageProcessor")
    print("  processor = ImageProcessor()")
    print("  processor.batch_compress('./input', './output', quality=80)")
    print()
    print("价格: $12.99")


if __name__ == "__main__":
    main()
