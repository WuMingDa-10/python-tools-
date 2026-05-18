#!/usr/bin/env python3
"""
代码分析大师 v1.0
=================
功能：代码复杂度分析、依赖分析、代码统计、质量评估
售价：$14.99
"""

import os
import sys
import re
import json
from datetime import datetime


class CodeAnalyzerMaster:
    """代码分析大师"""
    
    def __init__(self):
        self.results = {}
    
    def analyze_python(self, code: str) -> dict:
        """分析 Python 代码"""
        lines = code.split('\n')
        
        # 统计
        total_lines = len(lines)
        blank_lines = sum(1 for line in lines if not line.strip())
        comment_lines = sum(1 for line in lines if line.strip().startswith('#'))
        code_lines = total_lines - blank_lines - comment_lines
        
        # 函数和类
        functions = re.findall(r'def\s+(\w+)\s*\(', code)
        classes = re.findall(r'class\s+(\w+)\s*[\(:]', code)
        imports = re.findall(r'(?:from\s+\S+\s+)?import\s+(\S+)', code)
        
        # 复杂度（简化版）
        complexity = 0
        for line in lines:
            line = line.strip()
            if line.startswith(('if ', 'elif ', 'else:', 'for ', 'while ', 'try:', 'except', 'finally:')):
                complexity += 1
        
        return {
            'total_lines': total_lines,
            'blank_lines': blank_lines,
            'comment_lines': comment_lines,
            'code_lines': code_lines,
            'functions': len(functions),
            'function_names': functions,
            'classes': len(classes),
            'class_names': classes,
            'imports': len(imports),
            'import_names': imports,
            'complexity': complexity,
            'comment_ratio': comment_lines / total_lines if total_lines > 0 else 0,
        }
    
    def analyze_javascript(self, code: str) -> dict:
        """分析 JavaScript 代码"""
        lines = code.split('\n')
        
        # 统计
        total_lines = len(lines)
        blank_lines = sum(1 for line in lines if not line.strip())
        comment_lines = sum(1 for line in lines if line.strip().startswith('//'))
        code_lines = total_lines - blank_lines - comment_lines
        
        # 函数
        functions = re.findall(r'function\s+(\w+)\s*\(', code)
        arrow_functions = re.findall(r'(?:const|let|var)\s+(\w+)\s*=\s*(?:\([^)]*\)|[^=])\s*=>', code)
        
        return {
            'total_lines': total_lines,
            'blank_lines': blank_lines,
            'comment_lines': comment_lines,
            'code_lines': code_lines,
            'functions': len(functions) + len(arrow_functions),
            'function_names': functions + arrow_functions,
        }
    
    def analyze_directory(self, directory: str, language: str = 'python') -> dict:
        """分析目录"""
        extensions = {
            'python': '.py',
            'javascript': '.js',
            'java': '.java',
            'cpp': '.cpp',
        }
        
        ext = extensions.get(language, '.py')
        
        results = {
            'files': 0,
            'total_lines': 0,
            'code_lines': 0,
            'functions': 0,
            'classes': 0,
        }
        
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.endswith(ext):
                    file_path = os.path.join(root, file)
                    
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        code = f.read()
                    
                    if language == 'python':
                        analysis = self.analyze_python(code)
                    elif language == 'javascript':
                        analysis = self.analyze_javascript(code)
                    else:
                        continue
                    
                    results['files'] += 1
                    results['total_lines'] += analysis['total_lines']
                    results['code_lines'] += analysis['code_lines']
                    results['functions'] += analysis['functions']
                    results['classes'] += analysis.get('classes', 0)
        
        return results
    
    def calculate_quality_score(self, analysis: dict) -> dict:
        """计算质量分数"""
        score = 100
        issues = []
        
        # 检查代码行数
        if analysis['code_lines'] > 1000:
            score -= 10
            issues.append('代码行数过多')
        
        # 检查注释比例
        if analysis['comment_ratio'] < 0.1:
            score -= 15
            issues.append('注释比例过低')
        
        # 检查复杂度
        if analysis['complexity'] > 50:
            score -= 20
            issues.append('代码复杂度过高')
        
        # 检查函数数量
        if analysis['functions'] > 20:
            score -= 10
            issues.append('函数数量过多')
        
        return {
            'score': max(0, score),
            'issues': issues,
            'grade': 'A' if score >= 90 else 'B' if score >= 80 else 'C' if score >= 70 else 'D',
        }
    
    def generate_report(self, analysis: dict, output_file: str = 'code_analysis.json') -> str:
        """生成分析报告"""
        report = {
            'timestamp': datetime.now().isoformat(),
            'analysis': analysis,
            'quality': self.calculate_quality_score(analysis),
        }
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        print(f"✅ 分析报告已生成: {output_file}")
        return output_file


def main():
    """主函数"""
    print("=" * 50)
    print("代码分析大师 v1.0")
    print("=" * 50)
    print()
    print("功能:")
    print("  1. 代码统计")
    print("  2. 复杂度分析")
    print("  3. 依赖分析")
    print("  4. 质量评估")
    print("  5. 批量分析")
    print("  6. 报告生成")
    print()
    print("使用方法:")
    print("  from code_analyzer import CodeAnalyzerMaster")
    print("  analyzer = CodeAnalyzerMaster()")
    print("  result = analyzer.analyze_python(code)")
    print()
    print("价格: $14.99")


if __name__ == "__main__":
    main()
