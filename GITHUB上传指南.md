# GitHub 上传指南

## 📋 准备清单

在上传到GitHub之前，确认以下文件已就绪：

- ✅ README.md - 完整项目说明
- ✅ LICENSE - MIT开源协议
- ✅ .gitignore - Git忽略规则
- ✅ requirements.txt - Python依赖列表
- ✅ pyproject.toml - 项目配置文件
- ✅ 所有源代码文件

## 🚀 上传步骤

### 1. 初始化Git仓库

```bash
cd E:\projects\ner-python
git init
```

### 2. 添加所有文件

```bash
git add .
```

### 3. 查看将要提交的文件

```bash
git status
```

**检查要点**：
- ❌ models/ 目录下的大文件不应被包含（已在.gitignore中排除）
- ❌ .venv 虚拟环境不应被包含
- ❌ __pycache__ 不应被包含
- ✅ app/ static/ examples/ 等核心代码应被包含

### 4. 创建首次提交

```bash
git commit -m "Initial commit: IntelliNER v1.0.0

- 支持9种实体类型识别（人名/地名/机构/大学/手机/身份证/邮箱/地址/网址）
- 混合识别方案（深度学习+正则表达式）
- Web可视化界面
- 基于ModelScope + FastAPI构建"
```

### 5. 在GitHub上创建新仓库

1. 访问 https://github.com/new
2. 仓库名：`intelliner` 或 `IntelliNER`
3. 描述：`🎯 中文智能实体识别系统 - Chinese NER with Hybrid Intelligence`
4. 选择：**Public**（公开）
5. **不要**勾选 "Initialize with README"（我们已有README）
6. 点击 **Create repository**

### 6. 关联远程仓库

```bash
# 替换为你的实际GitHub用户名
git remote add origin https://github.com/YOUR_GITHUB_USERNAME/intelliner.git

# 或使用SSH（需配置SSH密钥）
git remote add origin git@github.com:YOUR_GITHUB_USERNAME/intelliner.git
```

### 7. 推送到GitHub

```bash
# 首次推送，设置上游分支
git branch -M main
git push -u origin main
```

如遇到需要登录，输入GitHub用户名和Personal Access Token（不是密码）。

---

## 🎨 可选：添加项目封面图

### 创建Demo截图

1. 启动服务：`uv run uvicorn app.main:app --host 0.0.0.0 --port 8000`
2. 打开浏览器访问 http://localhost:8000
3. 选择一个复杂示例（如"案件报告记录"）
4. 点击"开始识别"
5. 截取完整识别结果的屏幕截图
6. 保存为 `assets/demo_screenshot.png`

### 上传截图

```bash
mkdir assets
# 将截图放入 assets/ 目录
git add assets/demo_screenshot.png
git commit -m "Add demo screenshot"
git push
```

---

## 🏷️ 添加GitHub标签

在GitHub仓库页面右侧：

1. 点击 **⚙️ Settings** → **Manage topics**
2. 添加标签：
   - `chinese`
   - `ner`
   - `named-entity-recognition`
   - `nlp`
   - `fastapi`
   - `modelscope`
   - `transformers`
   - `python`
   - `entity-extraction`
   - `information-extraction`

---

## 📝 完善项目信息

### 1. 编辑仓库描述

在仓库首页，点击 ⚙️ 图标，填写：
```
🎯 中文智能实体识别系统 - 支持人名/地名/机构/手机/身份证/邮箱/地址/网址识别 | Chinese NER with Hybrid Intelligence
```

### 2. 设置主页

如需设置GitHub Pages：
1. Settings → Pages
2. Source: Deploy from a branch
3. Branch: main, /static
4. Save

### 3. 添加徽章（可选）

在README.md顶部已有徽章，可访问 https://shields.io 定制更多。

---

## 🎯 后续维护

### 创建Release

当有重大更新时，创建版本发布：

```bash
git tag -a v1.0.0 -m "Release version 1.0.0"
git push origin v1.0.0
```

在GitHub仓库页面：
1. Releases → Create a new release
2. 选择刚创建的tag
3. 填写Release notes
4. Publish release

### 更新代码

```bash
# 修改代码后
git add .
git commit -m "描述你的改动"
git push
```

---

## ⚠️ 注意事项

### 不要上传的文件
- ❌ 模型文件（models/ 目录，太大）
- ❌ 虚拟环境（.venv/）
- ❌ 缓存文件（__pycache__/）
- ❌ 日志文件（*.log）
- ❌ 敏感信息（.env、密钥）

### 修改README中的占位符

上传前，在README.md中替换：
- `YOUR_GITHUB_USERNAME` → 你的GitHub用户名（如需公开仓库链接）
- 或保持通用链接 `github.com/intelliner/intelliner`（作为组织仓库）

### 首次使用Git？

如需配置用户信息：
```bash
git config --global user.name "Your Name"
git config --global user.email "your-email@example.com"
```

---

## 🎉 完成！

上传成功后，你的项目地址将是：
```
https://github.com/YOUR_GITHUB_USERNAME/intelliner
```

可以分享这个链接让别人访问你的项目了！

---

## 💡 推广建议

1. **写一篇博客**：介绍项目设计思路和技术细节
2. **发布到社区**：
   - 掘金、CSDN等技术社区
   - V2EX、Ruby China等论坛
   - Reddit r/MachineLearning
3. **添加到Awesome列表**：搜索"awesome-chinese-nlp"等
4. **社交媒体**：Twitter/X、微博、知乎分享

好的README + 实用功能 = ⭐Star增长！
