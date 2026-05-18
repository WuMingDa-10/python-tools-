#!/bin/bash
# FileOrganizer Pro - 快速部署脚本

echo "=========================================="
echo "FileOrganizer Pro - 快速部署"
echo "=========================================="

# 1. 创建 GitHub 仓库
echo ""
echo "步骤 1: 创建 GitHub 仓库"
echo "----------------------------------------"
echo "1. 访问 https://github.com/new"
echo "2. 仓库名: file-organizer-pro"
echo "3. 设为 Public"
echo "4. 不要初始化 README"
echo "5. 点击 Create repository"
echo ""

# 2. 初始化 Git
echo "步骤 2: 初始化 Git"
echo "----------------------------------------"
cd ~/money-maker
git init
git add .
git commit -m "Initial commit: FileOrganizer Pro"
echo ""

# 3. 推送到 GitHub
echo "步骤 3: 推送到 GitHub"
echo "----------------------------------------"
echo "运行以下命令（替换 YOUR_USERNAME）:"
echo ""
echo "git remote add origin https://github.com/YOUR_USERNAME/file-organizer-pro.git"
echo "git push -u origin main"
echo ""

# 4. 启用 GitHub Pages
echo "步骤 4: 启用 GitHub Pages"
echo "----------------------------------------"
echo "1. 访问: https://github.com/YOUR_USERNAME/file-organizer-pro/settings/pages"
echo "2. Source 选择: Deploy from a branch"
echo "3. Branch 选择: main / root"
echo "4. 点击 Save"
echo ""

# 5. 设置支付
echo "步骤 5: 设置支付"
echo "----------------------------------------"
echo "选项 1: Ko-fi (推荐)"
echo "  - 访问 https://ko-fi.com"
echo "  - 注册账号"
echo "  - 获取链接: https://ko-fi.com/YOUR_USERNAME"
echo ""
echo "选项 2: Buy Me a Coffee"
echo "  - 访问 https://buymeacoffee.com"
echo "  - 注册账号"
echo "  - 获取链接: https://buymeacoffee.com/YOUR_USERNAME"
echo ""
echo "选项 3: PayPal"
echo "  - 访问 https://paypal.me"
echo "  - 创建链接: https://paypal.me/YOUR_USERNAME/9.99"
echo ""

# 6. 更新链接
echo "步骤 6: 更新链接"
echo "----------------------------------------"
echo "编辑 index.html，替换以下链接:"
echo "  - ko-fi.com/yourusername -> 你的 Ko-fi 链接"
echo "  - paypal.me/yourusername -> 你的 PayPal 链接"
echo ""

# 7. 推广
echo "步骤 7: 推广"
echo "----------------------------------------"
echo "社交媒体帖子模板:"
echo ""
echo "🚀 发布！FileOrganizer Pro - 智能文件整理工具"
echo ""
echo "功能:"
echo "✅ 一键整理混乱文件夹"
echo "✅ 自动分类（图片/视频/文档/代码）"
echo "✅ 智能去重，释放磁盘空间"
echo "✅ 生成整理报告"
echo ""
echo "价格: \$9.99 (一次购买，终身使用)"
echo ""
echo "下载: https://YOUR_USERNAME.github.io/file-organizer-pro"
echo ""
echo "#Python #效率工具 #文件整理 #自动化"
echo ""

echo "=========================================="
echo "部署完成！"
echo "=========================================="
echo ""
echo "下一步:"
echo "1. 创建 GitHub 仓库"
echo "2. 推送代码"
echo "3. 启用 GitHub Pages"
echo "4. 设置支付链接"
echo "5. 开始推广！"
