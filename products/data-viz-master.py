#!/usr/bin/env python3
"""
数据可视化大师 v1.0
===================
功能：图表生成、数据大屏、交互式图表、报告导出
售价：$29.99
"""

import os
import sys
import json
from datetime import datetime

try:
    import matplotlib.pyplot as plt
    import matplotlib
    matplotlib.use('Agg')
except ImportError:
    import subprocess
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'matplotlib'])
    import matplotlib.pyplot as plt
    import matplotlib
    matplotlib.use('Agg')

try:
    import pandas as pd
except ImportError:
    import subprocess
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'pandas'])
    import pandas as pd


class DataVisualizationMaster:
    """数据可视化大师"""
    
    def __init__(self, style: str = 'seaborn'):
        try:
            plt.style.use(style)
        except:
            pass
        self.figures = []
    
    def create_bar_chart(self, data: dict, title: str = '柱状图', 
                        output_file: str = 'bar_chart.png') -> str:
        """创建柱状图"""
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.bar(data.keys(), data.values(), color='steelblue')
        ax.set_title(title)
        ax.set_xlabel('类别')
        ax.set_ylabel('值')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(output_file, dpi=150)
        plt.close()
        
        print(f"✅ 柱状图已生成: {output_file}")
        return output_file
    
    def create_line_chart(self, data: dict, title: str = '折线图', 
                         output_file: str = 'line_chart.png') -> str:
        """创建折线图"""
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(list(data.keys()), list(data.values()), marker='o', color='steelblue')
        ax.set_title(title)
        ax.set_xlabel('时间')
        ax.set_ylabel('值')
        plt.xticks(rotation=45)
        plt.grid(True)
        plt.tight_layout()
        plt.savefig(output_file, dpi=150)
        plt.close()
        
        print(f"✅ 折线图已生成: {output_file}")
        return output_file
    
    def create_pie_chart(self, data: dict, title: str = '饼图', 
                        output_file: str = 'pie_chart.png') -> str:
        """创建饼图"""
        fig, ax = plt.subplots(figsize=(8, 8))
        ax.pie(data.values(), labels=data.keys(), autopct='%1.1f%%', startangle=90)
        ax.set_title(title)
        plt.tight_layout()
        plt.savefig(output_file, dpi=150)
        plt.close()
        
        print(f"✅ 饼图已生成: {output_file}")
        return output_file
    
    def create_scatter_plot(self, x: list, y: list, title: str = '散点图', 
                           output_file: str = 'scatter_plot.png') -> str:
        """创建散点图"""
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.scatter(x, y, alpha=0.6, color='steelblue')
        ax.set_title(title)
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        plt.grid(True)
        plt.tight_layout()
        plt.savefig(output_file, dpi=150)
        plt.close()
        
        print(f"✅ 散点图已生成: {output_file}")
        return output_file
    
    def create_heatmap(self, data: list, title: str = '热力图', 
                       output_file: str = 'heatmap.png') -> str:
        """创建热力图"""
        fig, ax = plt.subplots(figsize=(10, 8))
        im = ax.imshow(data, cmap='YlOrRd')
        ax.set_title(title)
        plt.colorbar(im)
        plt.tight_layout()
        plt.savefig(output_file, dpi=150)
        plt.close()
        
        print(f"✅ 热力图已生成: {output_file}")
        return output_file
    
    def create_dashboard(self, data: dict, output_file: str = 'dashboard.html') -> str:
        """创建数据大屏"""
        html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <title>数据大屏</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; background: #1a1a2e; color: #eee; }}
        .container {{ max-width: 1200px; margin: 0 auto; }}
        .card {{ background: #16213e; padding: 20px; margin: 15px 0; border-radius: 10px; }}
        .stats {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; }}
        .stat-box {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 20px; border-radius: 10px; text-align: center; }}
        .stat-value {{ font-size: 2rem; font-weight: bold; }}
        .stat-label {{ font-size: 0.9rem; opacity: 0.9; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>📊 数据大屏</h1>
        <div class="stats">
"""
        
        for key, value in data.items():
            html_content += f"""
            <div class="stat-box">
                <div class="stat-value">{value}</div>
                <div class="stat-label">{key}</div>
            </div>
"""
        
        html_content += """
        </div>
    </div>
</body>
</html>
"""
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"✅ 数据大屏已生成: {output_file}")
        return output_file
    
    def export_report(self, charts: list, output_file: str = 'report.pdf') -> str:
        """导出 PDF 报告"""
        try:
            from matplotlib.backends.backend_pdf import PdfPages
            
            with PdfPages(output_file) as pdf:
                for chart_file in charts:
                    if os.path.exists(chart_file):
                        img = plt.imread(chart_file)
                        fig, ax = plt.subplots(figsize=(10, 6))
                        ax.imshow(img)
                        ax.axis('off')
                        pdf.savefig(fig)
                        plt.close()
            
            print(f"✅ PDF 报告已生成: {output_file}")
            return output_file
        except Exception as e:
            print(f"❌ 导出失败: {e}")
            return None


def main():
    """主函数"""
    print("=" * 50)
    print("数据可视化大师 v1.0")
    print("=" * 50)
    print()
    print("功能:")
    print("  1. 柱状图")
    print("  2. 折线图")
    print("  3. 饼图")
    print("  4. 散点图")
    print("  5. 热力图")
    print("  6. 数据大屏")
    print()
    print("使用方法:")
    print("  from data_viz import DataVisualizationMaster")
    print("  viz = DataVisualizationMaster()")
    print("  viz.create_bar_chart({'A': 10, 'B': 20, 'C': 30})")
    print()
    print("价格: $29.99")


if __name__ == "__main__":
    main()
