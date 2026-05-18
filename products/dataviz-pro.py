#!/usr/bin/env python3
"""
DataViz Pro - 数据可视化工具包
==============================
功能：
1. 自动生成图表
2. 数据分析报告
3. 交互式仪表盘
4. 导出多种格式

定价：$19.99
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from typing import List, Dict, Optional
import json
import os

class DataVizPro:
    """数据可视化专业工具"""
    
    def __init__(self, style: str = 'seaborn'):
        plt.style.use(style)
        self.figures = []
    
    def auto_plot(self, df: pd.DataFrame, title: str = "数据分析") -> plt.Figure:
        """自动分析并生成图表"""
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        fig.suptitle(title, fontsize=16, fontweight='bold')
        
        # 数值列统计
        numeric_cols = df.select_dtypes(include=['number']).columns
        if len(numeric_cols) > 0:
            # 直方图
            df[numeric_cols[0]].hist(ax=axes[0, 0], bins=20, color='steelblue', edgecolor='white')
            axes[0, 0].set_title(f'{numeric_cols[0]} 分布')
            axes[0, 0].set_xlabel(numeric_cols[0])
            axes[0, 0].set_ylabel('频次')
            
            # 箱线图
            if len(numeric_cols) >= 2:
                df[numeric_cols[:4]].boxplot(ax=axes[0, 1])
                axes[0, 1].set_title('数值列箱线图')
            
            # 相关性热力图
            if len(numeric_cols) >= 2:
                corr = df[numeric_cols].corr()
                sns.heatmap(corr, ax=axes[1, 0], annot=True, cmap='coolwarm', center=0)
                axes[1, 0].set_title('相关性矩阵')
            
            # 散点图
            if len(numeric_cols) >= 2:
                axes[1, 1].scatter(df[numeric_cols[0]], df[numeric_cols[1]], 
                                  alpha=0.6, color='steelblue')
                axes[1, 1].set_xlabel(numeric_cols[0])
                axes[1, 1].set_ylabel(numeric_cols[1])
                axes[1, 1].set_title(f'{numeric_cols[0]} vs {numeric_cols[1]}')
        
        plt.tight_layout()
        self.figures.append(fig)
        return fig
    
    def create_dashboard(self, df: pd.DataFrame, output_file: str = "dashboard.html"):
        """创建交互式 HTML 仪表盘"""
        numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
        categorical_cols = df.select_dtypes(include=['object']).columns.tolist()
        
        html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <title>数据仪表盘</title>
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }}
        .container {{ max-width: 1200px; margin: 0 auto; }}
        .card {{ background: white; padding: 20px; margin: 15px 0; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
        .stats {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; }}
        .stat-box {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; border-radius: 8px; text-align: center; }}
        .stat-value {{ font-size: 2rem; font-weight: bold; }}
        .stat-label {{ font-size: 0.9rem; opacity: 0.9; }}
        .chart {{ width: 100%; height: 400px; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>📊 数据分析仪表盘</h1>
        
        <div class="stats">
            <div class="stat-box">
                <div class="stat-value">{len(df)}</div>
                <div class="stat-label">总行数</div>
            </div>
            <div class="stat-box">
                <div class="stat-value">{len(df.columns)}</div>
                <div class="stat-label">总列数</div>
            </div>
            <div class="stat-box">
                <div class="stat-value">{len(numeric_cols)}</div>
                <div class="stat-label">数值列</div>
            </div>
            <div class="stat-box">
                <div class="stat-value">{df.isnull().sum().sum()}</div>
                <div class="stat-label">缺失值</div>
            </div>
        </div>
        
        <div class="card">
            <h2>数据预览</h2>
            {df.head(10).to_html(classes='table', index=False)}
        </div>
        
        <div class="card">
            <h2>描述性统计</h2>
            {df.describe().to_html(classes='table')}
        </div>
    </div>
</body>
</html>
"""
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        return output_file
    
    def export_report(self, df: pd.DataFrame, output_file: str = "report.pdf"):
        """导出 PDF 报告"""
        from matplotlib.backends.backend_pdf import PdfPages
        
        with PdfPages(output_file) as pdf:
            # 第一页：概览
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.text(0.5, 0.5, f'数据报告\n\n总行数: {len(df)}\n总列数: {len(df.columns)}',
                    ha='center', va='center', fontsize=20, transform=ax.transAxes)
            ax.axis('off')
            pdf.savefig(fig)
            plt.close()
            
            # 第二页：统计
            fig = plt.figure(figsize=(10, 6))
            ax = fig.add_subplot(111)
            ax.axis('off')
            table_data = df.describe().round(2)
            table = ax.table(cellText=table_data.values,
                            colLabels=table_data.columns,
                            rowLabels=table_data.index,
                            loc='center')
            table.auto_set_font_size(False)
            table.set_fontsize(9)
            table.scale(1.2, 1.5)
            pdf.savefig(fig)
            plt.close()
            
            # 第三页：图表
            if len(df.select_dtypes(include=['number']).columns) > 0:
                fig = self.auto_plot(df)
                pdf.savefig(fig)
                plt.close()
        
        return output_file


def quick_analysis(file_path: str, output_dir: str = "./output"):
    """快速分析文件并生成报告"""
    os.makedirs(output_dir, exist_ok=True)
    
    # 读取数据
    if file_path.endswith('.csv'):
        df = pd.read_csv(file_path)
    elif file_path.endswith('.xlsx'):
        df = pd.read_excel(file_path)
    elif file_path.endswith('.json'):
        df = pd.read_json(file_path)
    else:
        raise ValueError(f"不支持的文件格式: {file_path}")
    
    # 生成可视化
    viz = DataVizPro()
    
    # 生成图表
    fig = viz.auto_plot(df, title=f"数据分析 - {os.path.basename(file_path)}")
    fig.savefig(os.path.join(output_dir, "analysis.png"), dpi=150, bbox_inches='tight')
    
    # 生成仪表盘
    viz.create_dashboard(df, os.path.join(output_dir, "dashboard.html"))
    
    # 生成报告
    viz.export_report(df, os.path.join(output_dir, "report.pdf"))
    
    print(f"✅ 分析完成！输出目录: {output_dir}")
    print(f"  - analysis.png: 数据图表")
    print(f"  - dashboard.html: 交互式仪表盘")
    print(f"  - report.pdf: PDF 报告")
    
    return df


if __name__ == "__main__":
    # 示例用法
    print("DataViz Pro - 数据可视化工具")
    print("=" * 40)
    print("使用方法:")
    print("  from dataviz import quick_analysis")
    print("  df = quick_analysis('data.csv')")
