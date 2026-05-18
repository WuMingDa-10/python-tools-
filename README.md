# 📁 FileOrganizer Pro - 智能文件整理工具

[![GitHub Pages](https://img.shields.io/badge/GitHub-Pages-blue)](https://yourusername.github.io/file-organizer-pro)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Price](https://img.shields.io/badge/Price-$9.99-orange)](https://ko-fi.com/yourusername)

## ✨ 功能特点

- 🗂️ **智能分类** - 自动识别文件类型，按类别整理
- 🔄 **自动去重** - 检测并删除重复文件，释放磁盘空间
- 📝 **智能重命名** - 处理重名文件，添加时间戳避免冲突
- 📊 **整理报告** - 生成详细的整理统计报告
- ⚡ **一键操作** - 命令行工具，简单高效

## 📦 支持的文件类型

| 类型 | 扩展名 |
|------|--------|
| 图片 | jpg, png, gif, bmp, webp, svg, ico |
| 视频 | mp4, avi, mkv, mov, wmv, flv, webm |
| 音频 | mp3, wav, flac, aac, ogg, wma |
| 文档 | pdf, doc, docx, txt, rtf, xls, xlsx, ppt, pptx |
| 代码 | py, js, html, css, java, cpp, c, go, rs, ts |
| 压缩包 | zip, rar, 7z, tar, gz, bz2 |
| 可执行 | exe, msi, dmg, app, deb, rpm |

## 🚀 快速开始

### 安装

```bash
# 直接下载脚本
wget https://yourusername.github.io/file-organizer-pro/file-organizer.py

# 或者克隆仓库
git clone https://github.com/yourusername/file-organizer-pro.git
```

### 使用

```bash
# 整理下载文件夹
python file_organizer.py ~/Downloads

# 整理并指定输出目录
python file_organizer.py ~/Downloads ~/Desktop/整理后

# 查看帮助
python file_organizer.py --help
```

## 💻 使用示例

```python
from file_organizer import FileOrganizer

# 创建整理器
organizer = FileOrganizer("~/Downloads")

# 开始整理
organizer.organize()

# 指定输出目录
organizer.organize("~/Desktop/整理后")

# 不去重
organizer.organize(remove_duplicates=False)
```

## 📊 输出示例

```
开始整理: ~/Downloads
输出目录: ~/Downloads/已整理
--------------------------------------------------
找到 156 个文件
  ✓ photo.jpg -> 图片/
  ✓ video.mp4 -> 视频/
  ✓ document.pdf -> 文档/
  ✓ script.py -> 代码/
  ...

==================================================
整理完成！
  总文件数: 156
  已整理: 156
  重复文件: 23
  错误: 0
```

## 💰 价格

**$9.99** - 一次购买，终身使用，免费更新

### 购买方式

- [☕ Ko-fi](https://ko-fi.com/yourusername)
- [💳 PayPal](https://paypal.me/yourusername/9.99)
- [☕ Buy Me a Coffee](https://buymeacoffee.com/yourusername)

## 📝 更新日志

### v1.0.0 (2025-05-17)
- ✨ 初始发布
- ✨ 智能文件分类
- ✨ 自动去重功能
- ✨ 智能重命名
- ✨ 整理报告生成

## 🤝 支持

- 📧 Email: your@email.com
- 🐛 Issues: [GitHub Issues](https://github.com/yourusername/file-organizer-pro/issues)

## 📄 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件

---

**如果觉得有用，请考虑支持一下 ❤️**

[![Ko-fi](https://img.shields.io/badge/Ko--fi-Support%20Me-red?logo=ko-fi)](https://ko-fi.com/yourusername)
