#!/usr/bin/env python3
"""
XML 处理大师 v1.0
=================
功能：XML 解析、转换、验证、生成
售价：$11.99
"""

import os
import sys
import json
import xml.etree.ElementTree as ET
from datetime import datetime


class XMLMaster:
    """XML 处理大师"""
    
    def __init__(self):
        self.tree = None
        self.root = None
    
    def load_file(self, file_path: str) -> ET.Element:
        """加载 XML 文件"""
        self.tree = ET.parse(file_path)
        self.root = self.tree.getroot()
        print(f"✅ 加载完成: {file_path}")
        return self.root
    
    def load_string(self, xml_string: str) -> ET.Element:
        """加载字符串"""
        self.root = ET.fromstring(xml_string)
        return self.root
    
    def parse_xml(self, xml_string: str) -> dict:
        """解析 XML"""
        root = ET.fromstring(xml_string)
        return self._element_to_dict(root)
    
    def _element_to_dict(self, element: ET.Element) -> dict:
        """元素转字典"""
        result = {
            'tag': element.tag,
            'attributes': element.attrib,
            'text': element.text,
            'children': [],
        }
        
        for child in element:
            result['children'].append(self._element_to_dict(child))
        
        return result
    
    def find_elements(self, xpath: str, root: ET.Element = None) -> list:
        """查找元素"""
        if root is None:
            root = self.root
        
        return root.findall(xpath)
    
    def find_text(self, xpath: str, root: ET.Element = None) -> list:
        """查找文本"""
        elements = self.find_elements(xpath, root)
        return [elem.text for elem in elements if elem.text]
    
    def find_attribute(self, xpath: str, attribute: str, 
                       root: ET.Element = None) -> list:
        """查找属性"""
        elements = self.find_elements(xpath, root)
        return [elem.get(attribute) for elem in elements if elem.get(attribute)]
    
    def xml_to_dict(self, root: ET.Element = None) -> dict:
        """XML 转字典"""
        if root is None:
            root = self.root
        
        return self._element_to_dict(root)
    
    def xml_to_json(self, root: ET.Element = None, output_file: str = None) -> str:
        """XML 转 JSON"""
        data = self.xml_to_dict(root)
        json_str = json.dumps(data, ensure_ascii=False, indent=2)
        
        if output_file:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(json_str)
            print(f"✅ 转换完成: {output_file}")
        
        return json_str
    
    def dict_to_xml(self, data: dict, root_tag: str = 'root') -> ET.Element:
        """字典转 XML"""
        root = ET.Element(root_tag)
        self._dict_to_element(data, root)
        return root
    
    def _dict_to_element(self, data: dict, parent: ET.Element):
        """字典转元素"""
        for key, value in data.items():
            if isinstance(value, dict):
                child = ET.SubElement(parent, key)
                self._dict_to_element(value, child)
            elif isinstance(value, list):
                for item in value:
                    child = ET.SubElement(parent, key)
                    if isinstance(item, dict):
                        self._dict_to_element(item, child)
                    else:
                        child.text = str(item)
            else:
                child = ET.SubElement(parent, key)
                child.text = str(value)
    
    def create_xml(self, root_tag: str, children: dict = None) -> ET.Element:
        """创建 XML"""
        root = ET.Element(root_tag)
        
        if children:
            for tag, text in children.items():
                child = ET.SubElement(root, tag)
                child.text = str(text)
        
        return root
    
    def add_element(self, parent: ET.Element, tag: str, 
                    text: str = None, attributes: dict = None) -> ET.Element:
        """添加元素"""
        child = ET.SubElement(parent, tag)
        
        if text:
            child.text = text
        
        if attributes:
            for key, value in attributes.items():
                child.set(key, value)
        
        return child
    
    def remove_element(self, parent: ET.Element, tag: str):
        """移除元素"""
        for child in parent.findall(tag):
            parent.remove(child)
    
    def update_element(self, element: ET.Element, text: str = None, 
                       attributes: dict = None):
        """更新元素"""
        if text:
            element.text = text
        
        if attributes:
            for key, value in attributes.items():
                element.set(key, value)
    
    def to_string(self, root: ET.Element = None, encoding: str = 'unicode') -> str:
        """转字符串"""
        if root is None:
            root = self.root
        
        return ET.tostring(root, encoding=encoding)
    
    def save_file(self, root: ET.Element = None, output_file: str = 'output.xml',
                  encoding: str = 'utf-8') -> str:
        """保存文件"""
        if root is None:
            root = self.root
        
        tree = ET.ElementTree(root)
        tree.write(output_file, encoding=encoding, xml_declaration=True)
        
        print(f"✅ 保存完成: {output_file}")
        return output_file
    
    def validate_xml(self, xml_string: str) -> dict:
        """验证 XML"""
        try:
            ET.fromstring(xml_string)
            return {'valid': True, 'error': None}
        except ET.ParseError as e:
            return {'valid': False, 'error': str(e)}
    
    def get_namespaces(self, file_path: str) -> dict:
        """获取命名空间"""
        namespaces = {}
        
        for event, elem in ET.iterparse(file_path, events=['start-ns']):
            prefix, uri = elem
            namespaces[prefix] = uri
        
        return namespaces


def main():
    """主函数"""
    print("=" * 50)
    print("XML 处理大师 v1.0")
    print("=" * 50)
    print()
    print("功能:")
    print("  1. XML 解析")
    print("  2. XML 转 JSON")
    print("  3. XML 验证")
    print("  4. XML 生成")
    print("  5. 元素操作")
    print("  6. 命名空间处理")
    print()
    print("使用方法:")
    print("  from xml_master import XMLMaster")
    print("  master = XMLMaster()")
    print("  root = master.load_file('data.xml')")
    print("  data = master.xml_to_dict(root)")
    print()
    print("价格: $11.99")


if __name__ == "__main__":
    main()
