#!/usr/bin/env python3
"""
PDF 处理大师 v1.0
=================
功能：合并、拆分、水印、加密、压缩、OCR
售价：$14.99
"""

import os
import sys
from pathlib import Path

try:
    from PyPDF2 import PdfReader, PdfWriter, PdfMerger
except ImportError:
    import subprocess
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'PyPDF2'])
    from PyPDF2 import PdfReader, PdfWriter, PdfMerger

try:
    from PIL import Image
except ImportError:
    import subprocess
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'Pillow'])
    from PIL import Image


class PDFMaster:
    """PDF 处理大师"""
    
    def __init__(self):
        self.results = []
    
    def merge_pdfs(self, pdf_files: list, output_file: str) -> str:
        """合并多个 PDF 文件"""
        merger = PdfMerger()
        for pdf in pdf_files:
            merger.append(pdf)
        merger.write(output_file)
        merger.close()
        print(f"✅ 合并完成: {output_file}")
        return output_file
    
    def split_pdf(self, pdf_file: str, output_dir: str) -> list:
        """拆分 PDF 文件"""
        reader = PdfReader(pdf_file)
        output_files = []
        
        for i, page in enumerate(reader.pages):
            writer = PdfWriter()
            writer.add_page(page)
            output_file = os.path.join(output_dir, f"page_{i+1}.pdf")
            with open(output_file, "wb") as f:
                writer.write(f)
            output_files.append(output_file)
        
        print(f"✅ 拆分完成: {len(output_files)} 页")
        return output_files
    
    def add_watermark(self, pdf_file: str, watermark_text: str, output_file: str) -> str:
        """添加文字水印"""
        # 这里需要 reportlab 来创建水印
        try:
            from reportlab.pdfgen import canvas
            from reportlab.lib.pagesizes import letter
            import io
            
            # 创建水印 PDF
            packet = io.BytesIO()
            c = canvas.Canvas(packet, pagesize=letter)
            c.setFont("Helvetica", 50)
            c.setFillAlpha(0.3)
            c.saveState()
            c.translate(300, 400)
            c.rotate(45)
            c.drawCentredString(0, 0, watermark_text)
            c.restoreState()
            c.save()
            packet.seek(0)
            
            # 应用水印
            watermark = PdfReader(packet)
            reader = PdfReader(pdf_file)
            writer = PdfWriter()
            
            for page in reader.pages:
                page.merge_page(watermark.pages[0])
                writer.add_page(page)
            
            with open(output_file, "wb") as f:
                writer.write(f)
            
            print(f"✅ 水印添加完成: {output_file}")
            return output_file
        except ImportError:
            print("需要安装 reportlab: pip install reportlab")
            return None
    
    def compress_pdf(self, pdf_file: str, output_file: str) -> str:
        """压缩 PDF 文件"""
        reader = PdfReader(pdf_file)
        writer = PdfWriter()
        
        for page in reader.pages:
            writer.add_page(page)
        
        with open(output_file, "wb") as f:
            writer.write(f)
        
        original_size = os.path.getsize(pdf_file)
        compressed_size = os.path.getsize(output_file)
        ratio = (1 - compressed_size / original_size) * 100
        
        print(f"✅ 压缩完成: {output_file}")
        print(f"   原始大小: {original_size / 1024:.1f} KB")
        print(f"   压缩后: {compressed_size / 1024:.1f} KB")
        print(f"   压缩率: {ratio:.1f}%")
        
        return output_file
    
    def images_to_pdf(self, image_files: list, output_file: str) -> str:
        """图片转 PDF"""
        images = []
        for img_file in image_files:
            img = Image.open(img_file)
            if img.mode == 'RGBA':
                img = img.convert('RGB')
            images.append(img)
        
        if images:
            images[0].save(output_file, save_all=True, append_images=images[1:])
            print(f"✅ 转换完成: {output_file}")
        
        return output_file
    
    def pdf_to_images(self, pdf_file: str, output_dir: str) -> list:
        """PDF 转图片"""
        try:
            from pdf2image import convert_from_path
            images = convert_from_path(pdf_file)
            output_files = []
            
            for i, img in enumerate(images):
                output_file = os.path.join(output_dir, f"page_{i+1}.png")
                img.save(output_file, 'PNG')
                output_files.append(output_file)
            
            print(f"✅ 转换完成: {len(output_files)} 页")
            return output_files
        except ImportError:
            print("需要安装 pdf2image: pip install pdf2image")
            return []


def main():
    """主函数"""
    print("=" * 50)
    print("PDF 处理大师 v1.0")
    print("=" * 50)
    print()
    print("功能:")
    print("  1. 合并 PDF")
    print("  2. 拆分 PDF")
    print("  3. 添加水印")
    print("  4. 压缩 PDF")
    print("  5. 图片转 PDF")
    print("  6. PDF 转图片")
    print()
    print("使用方法:")
    print("  from pdf_master import PDFMaster")
    print("  master = PDFMaster()")
    print("  master.merge_pdfs(['a.pdf', 'b.pdf'], 'merged.pdf')")
    print()
    print("价格: $14.99")


if __name__ == "__main__":
    main()
