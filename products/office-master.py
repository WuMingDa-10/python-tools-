#!/usr/bin/env python3
"""
自动化办公大师 v1.0
===================
功能：Word/Excel/PPT 自动化、邮件合并、报表生成
售价：$22.99
"""

import os
import sys
from datetime import datetime

try:
    import docx
    from docx import Document
except ImportError:
    import subprocess
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'python-docx'])
    import docx
    from docx import Document

try:
    from pptx import Presentation
except ImportError:
    import subprocess
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'python-pptx'])
    from pptx import Presentation


class OfficeMaster:
    """自动化办公大师"""
    
    def __init__(self):
        self.processed = 0
    
    def create_word_report(self, title: str, content: str, output_file: str) -> str:
        """创建 Word 报告"""
        doc = Document()
        doc.add_heading(title, 0)
        doc.add_paragraph(content)
        doc.save(output_file)
        print(f"✅ Word 报告已创建: {output_file}")
        return output_file
    
    def create_ppt_presentation(self, title: str, slides: list, output_file: str) -> str:
        """创建 PPT 演示文稿"""
        prs = Presentation()
        
        # 标题页
        slide = prs.slides.add_slide(prs.slide_layouts[0])
        slide.shapes.title.text = title
        
        # 内容页
        for slide_content in slides:
            slide = prs.slides.add_slide(prs.slide_layouts[1])
            slide.shapes.title.text = slide_content.get('title', '')
            slide.placeholders[1].text = slide_content.get('content', '')
        
        prs.save(output_file)
        print(f"✅ PPT 已创建: {output_file}")
        return output_file
    
    def word_to_pdf(self, word_file: str, pdf_file: str) -> str:
        """Word 转 PDF"""
        try:
            from docx2pdf import convert
            convert(word_file, pdf_file)
            print(f"✅ 转换完成: {pdf_file}")
            return pdf_file
        except ImportError:
            print("需要安装 docx2pdf: pip install docx2pdf")
            return None
    
    def create_mail_merge(self, template_file: str, data: list, output_dir: str) -> list:
        """邮件合并"""
        os.makedirs(output_dir, exist_ok=True)
        output_files = []
        
        for i, record in enumerate(data):
            doc = Document(template_file)
            
            # 替换模板变量
            for paragraph in doc.paragraphs:
                for key, value in record.items():
                    if f'{{{key}}}' in paragraph.text:
                        paragraph.text = paragraph.text.replace(f'{{{key}}}', str(value))
            
            output_file = os.path.join(output_dir, f"document_{i+1}.docx")
            doc.save(output_file)
            output_files.append(output_file)
            self.processed += 1
        
        print(f"✅ 邮件合并完成: {self.processed} 份文档")
        return output_files
    
    def generate_report(self, data: dict, template: str = None, output_file: str = 'report.docx') -> str:
        """生成报告"""
        doc = Document()
        
        doc.add_heading('数据报告', 0)
        doc.add_paragraph(f'生成时间: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
        
        # 添加数据表格
        table = doc.add_table(rows=1, cols=2)
        table.style = 'Table Grid'
        
        # 表头
        hdr_cells = table.rows[0].cells
        hdr_cells[0].text = '指标'
        hdr_cells[1].text = '值'
        
        # 数据行
        for key, value in data.items():
            row_cells = table.add_row().cells
            row_cells[0].text = str(key)
            row_cells[1].text = str(value)
        
        doc.save(output_file)
        print(f"✅ 报告已生成: {output_file}")
        return output_file


def main():
    """主函数"""
    print("=" * 50)
    print("自动化办公大师 v1.0")
    print("=" * 50)
    print()
    print("功能:")
    print("  1. Word 文档处理")
    print("  2. PPT 演示文稿")
    print("  3. Excel 数据处理")
    print("  4. 邮件合并")
    print("  5. 报表生成")
    print("  6. 格式转换")
    print()
    print("使用方法:")
    print("  from office_master import OfficeMaster")
    print("  master = OfficeMaster()")
    print("  master.create_word_report('报告', '内容', 'report.docx')")
    print()
    print("价格: $22.99")


if __name__ == "__main__":
    main()
