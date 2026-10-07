#!/bin/bash
# IntelliNER GitHub上传脚本
# 请在执行前阅读此脚本，确认无误后手动执行

set -e

echo "=== IntelliNER GitHub上传准备 ==="
echo ""

# 检查是否在正确目录
if [ ! -f "pyproject.toml" ]; then
    echo "错误: 请在项目根目录执行此脚本"
    exit 1
fi

# 提示用户
echo "⚠️  注意事项："
echo "1. 此脚本将初始化Git仓库并准备首次提交"
echo "2. 不会自动推送到GitHub，需手动执行推送命令"
echo "3. 确保已在GitHub创建了空仓库（仓库名建议：intelliner）"
echo ""
read -p "是否继续? (y/n) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "已取消"
    exit 0
fi

# 1. 初始化Git（如果尚未初始化）
if [ ! -d ".git" ]; then
    echo "✓ 初始化Git仓库..."
    git init
else
    echo "✓ Git仓库已存在"
fi

# 2. 设置本地提交用户信息（不影响全局配置）
echo ""
echo "设置Git提交信息（仅本仓库）："
read -p "请输入用户名（建议用组织名，如 IntelliNER Team）: " git_name
read -p "请输入邮箱（建议用项目邮箱，如 noreply@example.com）: " git_email

git config user.name "$git_name"
git config user.email "$git_email"
echo "✓ 本地Git用户信息已设置"

# 3. 添加所有文件
echo ""
echo "✓ 添加文件到暂存区..."
git add .

# 4. 查看将要提交的文件
echo ""
echo "=== 将要提交的文件 ==="
git status
echo ""

# 5. 检查敏感文件
echo "检查敏感文件..."
if git ls-files | grep -E "\.env$|\.key$|password|secret" > /dev/null; then
    echo "⚠️  警告：检测到可能包含敏感信息的文件"
    git ls-files | grep -E "\.env$|\.key$|password|secret"
    read -p "是否继续? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "已取消"
        exit 0
    fi
fi

# 6. 检查大文件
echo ""
echo "检查大文件..."
large_files=$(find . -type f -size +10M ! -path "./.git/*" ! -path "./.venv/*" ! -path "./models/*" 2>/dev/null || true)
if [ ! -z "$large_files" ]; then
    echo "⚠️  警告：检测到大文件（>10MB）"
    echo "$large_files"
    read -p "这些文件应该被添加吗? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Nn]$ ]]; then
        :
    else
        echo "请手动将这些文件添加到.gitignore"
        exit 0
    fi
fi

# 7. 创建首次提交
echo ""
echo "✓ 创建首次提交..."
git commit -m "Initial commit: IntelliNER v1.0.0

- 支持9种实体类型识别（人名/地名/机构/大学/手机/身份证/邮箱/地址/网址）
- 混合识别方案（深度学习NER模型 + 正则表达式）
- Web可视化界面，彩色高亮显示
- 基于ModelScope + FastAPI构建
- 完整的中英文文档"

# 8. 设置主分支名
echo "✓ 设置主分支为 main..."
git branch -M main

# 9. 提示后续步骤
echo ""
echo "=== ✅ 准备完成！==="
echo ""
echo "📝 后续步骤："
echo ""
echo "1. 在GitHub创建新仓库（如果还没创建）："
echo "   https://github.com/new"
echo "   仓库名建议：intelliner"
echo "   选择 Public，不要勾选 Initialize with README"
echo ""
echo "2. 关联远程仓库（替换YOUR_USERNAME为你的GitHub用户名）："
echo "   git remote add origin https://github.com/YOUR_USERNAME/intelliner.git"
echo ""
echo "3. 推送到GitHub："
echo "   git push -u origin main"
echo ""
echo "4. 如需使用SSH："
echo "   git remote set-url origin git@github.com:YOUR_USERNAME/intelliner.git"
echo ""
echo "⚠️  注意：推送前请确认："
echo "   - 仓库设置为Public（开源）或Private（私有）"
echo "   - 没有包含敏感信息（密码、密钥等）"
echo "   - .gitignore已正确排除models/目录"
echo ""
