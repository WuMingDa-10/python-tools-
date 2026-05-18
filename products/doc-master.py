#!/usr/bin/env python3
"""
文档生成大师 v1.0
=================
功能：API 文档、代码文档、用户手册、技术文档
售价：$12.99
"""

import os
import sys
import json
from datetime import datetime


class DocMaster:
    """文档生成大师"""
    
    def __init__(self):
        self.docs = {}
    
    def generate_api_doc(self, endpoints: list, output_file: str = 'api_docs.md') -> str:
        """生成 API 文档"""
        doc = "# API 文档\n\n"
        doc += f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        
        for endpoint in endpoints:
            doc += f"## {endpoint['method']} {endpoint['path']}\n\n"
            doc += f"{endpoint.get('description', '')}\n\n"
            
            if endpoint.get('parameters'):
                doc += "### 参数\n\n"
                doc += "| 名称 | 类型 | 必填 | 描述 |\n"
                doc += "|------|------|------|------|\n"
                for param in endpoint['parameters']:
                    doc += f"| {param['name']} | {param['type']} | {'是' if param.get('required') else '否'} | {param.get('description', '')} |\n"
                doc += "\n"
            
            if endpoint.get('response'):
                doc += "### 响应\n\n"
                doc += f"```json\n{json.dumps(endpoint['response'], indent=2, ensure_ascii=False)}\n```\n\n"
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(doc)
        
        print(f"✅ API 文档已生成: {output_file}")
        return output_file
    
    def generate_code_doc(self, code: str, output_file: str = 'code_docs.md') -> str:
        """生成代码文档"""
        doc = "# 代码文档\n\n"
        doc += f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        
        # 简单解析代码
        lines = code.split('\n')
        functions = []
        classes = []
        
        for i, line in enumerate(lines):
            if line.strip().startswith('def '):
                func_name = line.strip().split('(')[0].replace('def ', '')
                functions.append({'name': func_name, 'line': i + 1})
            elif line.strip().startswith('class '):
                class_name = line.strip().split('(')[0].replace('class ', '').replace(':', '')
                classes.append({'name': class_name, 'line': i + 1})
        
        if classes:
            doc += "## 类\n\n"
            for cls in classes:
                doc += f"- `{cls['name']}` (第 {cls['line']} 行)\n"
            doc += "\n"
        
        if functions:
            doc += "## 函数\n\n"
            for func in functions:
                doc += f"- `{func['name']}` (第 {func['line']} 行)\n"
            doc += "\n"
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(doc)
        
        print(f"✅ 代码文档已生成: {output_file}")
        return output_file
    
    def generate_user_manual(self, title: str, sections: list, 
                            output_file: str = 'user_manual.md') -> str:
        """生成用户手册"""
        doc = f"# {title}\n\n"
        doc += f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        
        for section in sections:
            doc += f"## {section['title']}\n\n"
            doc += f"{section['content']}\n\n"
            
            if section.get('subsections'):
                for subsection in section['subsections']:
                    doc += f"### {subsection['title']}\n\n"
                    doc += f"{subsection['content']}\n\n"
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(doc)
        
        print(f"✅ 用户手册已生成: {output_file}")
        return output_file
    
    def generate_readme(self, project_name: str, description: str,
                       features: list = None, installation: str = None,
                       usage: str = None, output_file: str = 'README.md') -> str:
        """生成 README"""
        doc = f"# {project_name}\n\n"
        doc += f"{description}\n\n"
        
        if features:
            doc += "## 功能特点\n\n"
            for feature in features:
                doc += f"- {feature}\n"
            doc += "\n"
        
        if installation:
            doc += "## 安装\n\n"
            doc += f"```bash\n{installation}\n```\n\n"
        
        if usage:
            doc += "## 使用方法\n\n"
            doc += f"```python\n{usage}\n```\n\n"
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(doc)
        
        print(f"✅ README 已生成: {output_file}")
        return output_file
    
    def generate_changelog(self, versions: list, output_file: str = 'CHANGELOG.md') -> str:
        """生成更新日志"""
        doc = "# 更新日志\n\n"
        
        for version in versions:
            doc += f"## {version['version']} - {version['date']}\n\n"
            
            if version.get('added'):
                doc += "### 新增\n\n"
                for item in version['added']:
                    doc += f"- {item}\n"
                doc += "\n"
            
            if version.get('changed'):
                doc += "### 变更\n\n"
                for item in version['changed']:
                    doc += f"- {item}\n"
                doc += "\n"
            
            if version.get('fixed'):
                doc += "### 修复\n\n"
                for item in version['fixed']:
                    doc += f"- {item}\n"
                doc += "\n"
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(doc)
        
        print(f"✅ 更新日志已生成: {output_file}")
        return output_file
    
    def generate_license(self, license_type: str = 'MIT', 
                        author: str = 'Your Name',
                        output_file: str = 'LICENSE') -> str:
        """生成许可证"""
        licenses = {
            'MIT': f"""MIT License

Copyright (c) {datetime.now().year} {author}

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.""",
        }
        
        license_text = licenses.get(license_type, licenses['MIT'])
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(license_text)
        
        print(f"✅ 许可证已生成: {output_file}")
        return output_file


def main():
    """主函数"""
    print("=" * 50)
    print("文档生成大师 v1.0")
    print("=" * 50)
    print()
    print("功能:")
    print("  1. API 文档")
    print("  2. 代码文档")
    print("  3. 用户手册")
    print("  4. README")
    print("  5. 更新日志")
    print("  6. 许可证")
    print()
    print("使用方法:")
    print("  from doc_master import DocMaster")
    print("  master = DocMaster()")
    print("  master.generate_readme('项目名', '描述', ['功能1', '功能2'])")
    print()
    print("价格: $12.99")


if __name__ == "__main__":
    main()
