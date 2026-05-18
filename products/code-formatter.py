#!/usr/bin/env python3
"""
代码格式化大师 v1.0
===================
功能：代码格式化、风格检查、代码美化、批量处理
售价：$11.99
"""

import os
import sys
import re
from datetime import datetime


class CodeFormatterMaster:
    """代码格式化大师"""
    
    def __init__(self):
        self.formatted = 0
    
    def format_python(self, code: str) -> str:
        """格式化 Python 代码"""
        # 简单的格式化
        lines = code.split('\n')
        formatted_lines = []
        
        for line in lines:
            # 去除尾部空白
            line = line.rstrip()
            
            # 处理空行
            if not line:
                formatted_lines.append('')
                continue
            
            # 处理缩进
            indent = len(line) - len(line.lstrip())
            content = line.strip()
            
            # 添加空格
            if '=' in content and '==' not in content and '!=' not in content:
                content = re.sub(r'(\w)=(\w)', r'\1 = \2', content)
            
            formatted_lines.append(' ' * indent + content)
        
        return '\n'.join(formatted_lines)
    
    def format_json(self, json_str: str, indent: int = 2) -> str:
        """格式化 JSON"""
        import json
        data = json.loads(json_str)
        return json.dumps(data, indent=indent, ensure_ascii=False)
    
    def format_html(self, html: str) -> str:
        """格式化 HTML"""
        # 简单的格式化
        html = re.sub(r'>\s+<', '>\n<', html)
        return html
    
    def format_css(self, css: str) -> str:
        """格式化 CSS"""
        # 简单的格式化
        css = re.sub(r'\s*{\s*', ' {\n  ', css)
        css = re.sub(r'\s*}\s*', '\n}\n', css)
        css = re.sub(r';\s*', ';\n  ', css)
        return css
    
    def format_sql(self, sql: str) -> str:
        """格式化 SQL"""
        # 简单的格式化
        keywords = ['SELECT', 'FROM', 'WHERE', 'AND', 'OR', 'ORDER BY', 'GROUP BY', 'HAVING']
        
        for keyword in keywords:
            sql = re.sub(f'\\b{keyword}\\b', f'\n{keyword}', sql, flags=re.IGNORECASE)
        
        return sql.strip()
    
    def check_style(self, code: str, language: str = 'python') -> list:
        """检查代码风格"""
        issues = []
        lines = code.split('\n')
        
        for i, line in enumerate(lines, 1):
            # 检查行长度
            if len(line) > 120:
                issues.append({
                    'line': i,
                    'type': 'line_too_long',
                    'message': f'行长度超过 120 字符 ({len(line)})',
                })
            
            # 检查尾部空白
            if line != line.rstrip():
                issues.append({
                    'line': i,
                    'type': 'trailing_whitespace',
                    'message': '行尾有多余空白',
                })
            
            # 检查空行
            if not line.strip() and i < len(lines) and not lines[i].strip():
                issues.append({
                    'line': i,
                    'type': 'multiple_blank_lines',
                    'message': '连续空行',
                })
        
        return issues
    
    def minify_js(self, js: str) -> str:
        """压缩 JavaScript"""
        # 移除注释
        js = re.sub(r'//.*?\n', '\n', js)
        js = re.sub(r'/\*.*?\*/', '', js, flags=re.DOTALL)
        
        # 移除多余空白
        js = re.sub(r'\s+', ' ', js)
        js = re.sub(r';\s*', ';', js)
        
        return js.strip()
    
    def minify_css(self, css: str) -> str:
        """压缩 CSS"""
        # 移除注释
        css = re.sub(r'/\*.*?\*/', '', css, flags=re.DOTALL)
        
        # 移除多余空白
        css = re.sub(r'\s+', ' ', css)
        css = re.sub(r';\s*', ';', css)
        css = re.sub(r'{\s*', '{', css)
        css = re.sub(r'\s*}', '}', css)
        
        return css.strip()
    
    def batch_format(self, input_dir: str, output_dir: str, 
                     language: str = 'python') -> list:
        """批量格式化"""
        os.makedirs(output_dir, exist_ok=True)
        output_files = []
        
        extensions = {
            'python': '.py',
            'javascript': '.js',
            'html': '.html',
            'css': '.css',
        }
        
        ext = extensions.get(language, '.txt')
        
        for filename in os.listdir(input_dir):
            if filename.endswith(ext):
                input_path = os.path.join(input_dir, filename)
                output_path = os.path.join(output_dir, filename)
                
                with open(input_path, 'r', encoding='utf-8') as f:
                    code = f.read()
                
                if language == 'python':
                    formatted = self.format_python(code)
                elif language == 'javascript':
                    formatted = self.minify_js(code)
                elif language == 'html':
                    formatted = self.format_html(code)
                elif language == 'css':
                    formatted = self.format_css(code)
                else:
                    formatted = code
                
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(formatted)
                
                output_files.append(output_path)
                self.formatted += 1
        
        print(f"✅ 批量格式化完成: {len(output_files)} 个文件")
        return output_files


def main():
    """主函数"""
    print("=" * 50)
    print("代码格式化大师 v1.0")
    print("=" * 50)
    print()
    print("功能:")
    print("  1. Python 格式化")
    print("  2. JSON 格式化")
    print("  3. HTML 格式化")
    print("  4. CSS 格式化")
    print("  5. SQL 格式化")
    print("  6. 风格检查")
    print()
    print("使用方法:")
    print("  from code_formatter import CodeFormatterMaster")
    print("  formatter = CodeFormatterMaster()")
    print("  formatted = formatter.format_python(code)")
    print()
    print("价格: $11.99")


if __name__ == "__main__":
    main()
