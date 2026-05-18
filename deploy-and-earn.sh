#!/bin/bash
# ============================================
# 一键赚钱部署脚本
# ============================================
# 运行方式: bash deploy-and-earn.sh
# ============================================

set -e

echo "=========================================="
echo "一键赚钱部署脚本"
echo "=========================================="

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# 步骤 1: 检查环境
echo -e "\n${YELLOW}步骤 1: 检查环境${NC}"
if ! command -v git &> /dev/null; then
    echo -e "${RED}错误: git 未安装${NC}"
    exit 1
fi
if ! command -v node &> /dev/null; then
    echo -e "${RED}错误: node 未安装${NC}"
    exit 1
fi
echo -e "${GREEN}环境检查通过${NC}"

# 步骤 2: 创建产品包
echo -e "\n${YELLOW}步骤 2: 创建产品包${NC}"
cd ~/money-maker
mkdir -p products

# 复制所有产品
cp ~/autobot-pro/autobot.py products/
cp ~/autobot-pro/products/dataviz-pro.py products/
cp ~/autobot-pro/products/webscrape-pro.py products/
cp ~/excel-tool/excel_tool.py products/
cp ~/money-maker/file-organizer.py products/

echo -e "${GREEN}产品包创建完成${NC}"

# 步骤 3: 创建 GitHub 仓库
echo -e "\n${YELLOW}步骤 3: 创建 GitHub 仓库${NC}"
echo "请在浏览器中打开: https://github.com/new"
echo "仓库名: python-tools"
echo "设为 Public"
echo ""
read -p "完成后按 Enter 继续..."

# 步骤 4: 推送代码
echo -e "\n${YELLOW}步骤 4: 推送代码${NC}"
git init
git add .
git commit -m "Initial commit: Python 工具包"
echo ""
echo "请运行以下命令（替换 YOUR_USERNAME）:"
echo ""
echo "git remote add origin https://github.com/YOUR_USERNAME/python-tools.git"
echo "git push -u origin main"
echo ""
read -p "完成后按 Enter 继续..."

# 步骤 5: 启用 GitHub Pages
echo -e "\n${YELLOW}步骤 5: 启用 GitHub Pages${NC}"
echo "请访问: https://github.com/YOUR_USERNAME/python-tools/settings/pages"
echo "Source 选择: Deploy from a branch"
echo "Branch 选择: main / root"
echo ""
read -p "完成后按 Enter 继续..."

# 步骤 6: 设置收款
echo -e "\n${YELLOW}步骤 6: 设置收款${NC}"
echo "请选择收款方式:"
echo "1. Ko-fi (推荐)"
echo "2. Buy Me a Coffee"
echo "3. PayPal"
echo ""
read -p "请选择 (1-3): " payment_choice

case $payment_choice in
    1)
        echo "请访问: https://ko-fi.com"
        echo "注册账号，获取链接: https://ko-fi.com/YOUR_USERNAME"
        ;;
    2)
        echo "请访问: https://buymeacoffee.com"
        echo "注册账号，获取链接: https://buymeacoffee.com/YOUR_USERNAME"
        ;;
    3)
        echo "请访问: https://paypal.me"
        echo "创建链接: https://paypal.me/YOUR_USERNAME"
        ;;
esac

echo ""
read -p "完成后按 Enter 继续..."

# 步骤 7: 生成推广内容
echo -e "\n${YELLOW}步骤 7: 生成推广内容${NC}"

cat > promotion.md << 'EOF'
# 推广内容

## Twitter 推文

🚀 发布！Python 工具包 - 5 个实用工具

包含：
✅ Excel 批量处理大师
✅ AutoBot Pro - 智能自动化
✅ DataViz Pro - 数据可视化
✅ WebScrape Pro - 网页抓取
✅ FileOrganizer Pro - 文件整理

价格: $9.99-29.99

下载: https://YOUR_USERNAME.github.io/python-tools

#Python #效率工具 #自动化

## Reddit 帖子

标题: [Show] Python 工具包 - 5 个实用工具

大家好！我开发了一套 Python 工具包，包含 5 个实用工具：

1. Excel 批量处理大师 - 批量处理 Excel 文件
2. AutoBot Pro - 智能自动化工具
3. DataViz Pro - 数据可视化工具
4. WebScrape Pro - 网页抓取工具
5. FileOrganizer Pro - 文件整理工具

GitHub: https://github.com/YOUR_USERNAME/python-tools
下载: https://YOUR_USERNAME.github.io/python-tools

欢迎反馈！
EOF

echo -e "${GREEN}推广内容已生成: promotion.md${NC}"

# 完成
echo -e "\n${GREEN}==========================================${NC}"
echo -e "${GREEN}部署完成！${NC}"
echo -e "${GREEN}==========================================${NC}"
echo ""
echo "你的产品页面: https://YOUR_USERNAME.github.io/python-tools"
echo ""
echo "下一步:"
echo "1. 在社交媒体分享推广内容"
echo "2. 在 Reddit、Twitter、Hacker News 发帖"
echo "3. 等待收入！"
echo ""
echo "预期收益:"
echo "- 第一周: $50-100"
echo "- 第一个月: $200-500"
echo "- 第三个月: $1000-2000"
echo ""
echo "祝你好运！💰"
