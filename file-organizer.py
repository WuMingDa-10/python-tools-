#!/usr/bin/env python3
"""
FileOrganizer Pro - 智能文件整理工具
====================================
功能：一键整理混乱的文件夹，自动分类、重命名、去重
售价：$9.99
"""

import os
import shutil
import hashlib
from pathlib import Path
from datetime import datetime
import json
import sys

class FileOrganizer:
    """智能文件整理工具"""
    
    # 文件类型分类
    FILE_TYPES = {
        '图片': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.svg', '.ico'],
        '视频': ['.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv', '.webm'],
        '音频': ['.mp3', '.wav', '.flac', '.aac', '.ogg', '.wma'],
        '文档': ['.pdf', '.doc', '.docx', '.txt', '.rtf', '.odt', '.xls', '.xlsx', '.ppt', '.pptx'],
        '代码': ['.py', '.js', '.html', '.css', '.java', '.cpp', '.c', '.go', '.rs', '.ts'],
        '压缩包': ['.zip', '.rar', '.7z', '.tar', '.gz', '.bz2'],
        '可执行': ['.exe', '.msi', '.dmg', '.app', '.deb', '.rpm'],
    }
    
    def __init__(self, source_dir: str):
        self.source_dir = Path(source_dir)
        self.stats = {'total': 0, 'organized': 0, 'duplicates': 0, 'errors': 0}
    
    def organize(self, output_dir: str = None, remove_duplicates: bool = True):
        """整理文件夹"""
        if output_dir:
            output_path = Path(output_dir)
            output_path.mkdir(parents=True, exist_ok=True)
        else:
            output_path = self.source_dir / '已整理'
            output_path.mkdir(exist_ok=True)
        
        print(f"开始整理: {self.source_dir}")
        print(f"输出目录: {output_path}")
        print("-" * 50)
        
        # 扫描所有文件
        files = list(self.source_dir.rglob('*'))
        files = [f for f in files if f.is_file() and '已整理' not in str(f)]
        
        self.stats['total'] = len(files)
        print(f"找到 {len(files)} 个文件")
        
        # 按类型分类
        for file_path in files:
            try:
                # 确定文件类型
                file_type = self._get_file_type(file_path)
                target_dir = output_path / file_type
                target_dir.mkdir(exist_ok=True)
                
                # 生成目标文件名
                target_file = self._get_unique_name(target_dir, file_path.name)
                
                # 移动文件
                shutil.move(str(file_path), str(target_file))
                self.stats['organized'] += 1
                print(f"  ✓ {file_path.name} -> {file_type}/")
                
            except Exception as e:
                self.stats['errors'] += 1
                print(f"  ✗ {file_path.name}: {e}")
        
        # 去重
        if remove_duplicates:
            print("\n开始去重...")
            self._remove_duplicates(output_path)
        
        # 生成报告
        report = self._generate_report(output_path)
        
        print("\n" + "=" * 50)
        print("整理完成！")
        print(f"  总文件数: {self.stats['total']}")
        print(f"  已整理: {self.stats['organized']}")
        print(f"  重复文件: {self.stats['duplicates']}")
        print(f"  错误: {self.stats['errors']}")
        
        return report
    
    def _get_file_type(self, file_path: Path) -> str:
        """获取文件类型"""
        ext = file_path.suffix.lower()
        for file_type, extensions in self.FILE_TYPES.items():
            if ext in extensions:
                return file_type
        return '其他'
    
    def _get_unique_name(self, target_dir: Path, filename: str) -> Path:
        """生成唯一的文件名"""
        target = target_dir / filename
        if not target.exists():
            return target
        
        # 添加时间戳
        name = Path(filename).stem
        ext = Path(filename).suffix
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        new_name = f"{name}_{timestamp}{ext}"
        
        return target_dir / new_name
    
    def _remove_duplicates(self, directory: Path):
        """删除重复文件"""
        seen_hashes = {}
        
        for file_path in directory.rglob('*'):
            if not file_path.is_file():
                continue
            
            # 计算文件哈希
            file_hash = self._hash_file(file_path)
            
            if file_hash in seen_hashes:
                # 删除重复文件
                file_path.unlink()
                self.stats['duplicates'] += 1
                print(f"  删除重复: {file_path.name}")
            else:
                seen_hashes[file_hash] = file_path
    
    def _hash_file(self, file_path: Path) -> str:
        """计算文件哈希"""
        hasher = hashlib.md5()
        with open(file_path, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b''):
                hasher.update(chunk)
        return hasher.hexdigest()
    
    def _generate_report(self, output_dir: Path) -> dict:
        """生成整理报告"""
        report = {
            'timestamp': datetime.now().isoformat(),
            'source': str(self.source_dir),
            'output': str(output_dir),
            'stats': self.stats,
            'categories': {}
        }
        
        # 统计每个分类的文件数
        for category in output_dir.iterdir():
            if category.is_dir():
                count = len(list(category.rglob('*')))
                report['categories'][category.name] = count
        
        # 保存报告
        report_file = output_dir / '整理报告.json'
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        return report


def quick_organize(source_dir: str, output_dir: str = None):
    """快速整理文件夹"""
    organizer = FileOrganizer(source_dir)
    return organizer.organize(output_dir)


def show_help():
    """显示帮助信息"""
    print("""
FileOrganizer Pro - 智能文件整理工具
====================================

用法:
    python file_organizer.py <目录路径> [输出目录]

参数:
    <目录路径>    要整理的目录路径（必需）
    [输出目录]    输出目录（可选，默认为原目录/已整理）

示例:
    python file_organizer.py ~/Downloads
    python file_organizer.py ~/Downloads ~/Desktop/整理后
    python file_organizer.py /path/to/messy/folder

功能:
    ✓ 智能分类：自动识别文件类型，按类别整理
    ✓ 自动去重：检测并删除重复文件
    ✓ 智能重命名：处理重名文件，添加时间戳
    ✓ 整理报告：生成详细的整理统计报告

支持的文件类型:
    - 图片：jpg, png, gif, bmp, webp, svg, ico
    - 视频：mp4, avi, mkv, mov, wmv, flv, webm
    - 音频：mp3, wav, flac, aac, ogg, wma
    - 文档：pdf, doc, docx, txt, rtf, xls, xlsx, ppt, pptx
    - 代码：py, js, html, css, java, cpp, c, go, rs, ts
    - 压缩包：zip, rar, 7z, tar, gz, bz2
    - 可执行：exe, msi, dmg, app, deb, rpm

价格：$9.99 (一次购买，终身使用)
支持：https://ko-fi.com/yourusername
""")


if __name__ == '__main__':
    if len(sys.argv) < 2 or sys.argv[1] in ['-h', '--help', 'help']:
        show_help()
        sys.exit(0)
    
    source = sys.argv[1]
    output = sys.argv[2] if len(sys.argv) > 2 else None
    
    if not os.path.exists(source):
        print(f"错误: 目录 '{source}' 不存在")
        sys.exit(1)
    
    quick_organize(source, output)
