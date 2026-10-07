# IntelliNER

<div align="center">

🎯 **中文智能实体识别系统**

Chinese Named Entity Recognition with Hybrid Intelligence

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-green.svg)](https://fastapi.tiangolo.com)
[![ModelScope](https://img.shields.io/badge/ModelScope-damo/nlp_raner-orange.svg)](https://modelscope.cn)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

[在线演示](#快速开始) · [功能特性](#功能特性) · [安装部署](#安装部署) · [API文档](#api接口)

</div>

---

## 📖 项目简介

IntelliNER 是一个开箱即用的中文智能实体识别系统，采用**深度学习模型 + 正则表达式**混合识别方案，支持多种实体类型的高精度识别。

### 为什么选择 IntelliNER？

- 🚀 **开箱即用**：无需训练模型，下载即可运行
- 🧠 **混合智能**：NER深度学习 + 正则表达式，准确率更高
- 🎨 **可视化界面**：Web端彩色高亮展示，一目了然
- ⚡ **高性能**：基于ModelScope国内镜像，模型下载快，推理速度快
- 🔌 **API友好**：RESTful API，轻松集成到任何系统

---

## ✨ 功能特性

### 支持的实体类型

#### 语义实体（深度学习模型识别）
- 👤 **人名** (PER) - Person
- 📍 **地名** (LOC) - Location  
- 🏢 **机构** (ORG) - Organization
- 🎓 **大学** (EDU) - Education

#### 结构化信息（正则表达式识别）
- 📱 **手机号** (PHONE) - 11位手机号码
- 🆔 **身份证** (ID_CARD) - 18位身份证号
- 📧 **邮箱** (EMAIL) - 电子邮件地址
- 🏠 **详细地址** (ADDRESS) - 省市区街道门牌号
- 🔗 **网址** (URL) - HTTP/HTTPS链接

### 核心能力

✅ 智能去重：重叠实体自动合并，优先保留高置信度结果  
✅ 长文本支持：自动截断保护，最大支持400字  
✅ 批量识别：支持单次请求或批量API调用  
✅ 实时处理：毫秒级响应速度（300字约1.3秒）

---

## 🎬 效果展示

### Web界面
<img src="assets/demo_screenshot.png" alt="IntelliNER Demo" width="800">

### 识别示例

**输入文本**：
```
张三的身份证号码是110101199001011234，手机号13800138000，
邮箱zhangsan@example.com，住址北京市朝阳区建国路88号SOHO现代城B座1201室。
```

**识别结果**：
```
[人名] 张三
[身份证] 110101199001011234
[手机号] 13800138000
[邮箱] zhangsan@example.com
[地址] 北京市朝阳区建国路88号
[地名] SOHO现代城B座1201室
```

---

## 🚀 快速开始

### 环境要求

- Python 3.10+
- uv（推荐）或 pip

### 安装依赖

```bash
# 克隆项目
git clone https://github.com/YOUR_USERNAME/intelliner.git
cd intelliner

# 使用 uv 安装（推荐）
uv sync

# 或使用 pip
pip install -r requirements.txt
```

### 启动服务

```bash
uv run uvicorn app.main:app --host 0.0.0.0 --port 8000

# 或使用 python
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### 访问应用

浏览器打开：**http://localhost:8000**

> ⚠️ **首次启动**：会自动下载模型文件（约400MB），需等待2-5分钟

---

## 📦 项目结构

```
intelliner/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI主程序
│   ├── models.py            # Pydantic数据模型
│   ├── ner_engine.py        # NER推理引擎（混合识别）
│   └── config.py            # 配置文件
├── static/
│   ├── index.html           # 前端页面
│   ├── style.css            # 样式表
│   └── app.js               # 前端逻辑
├── examples/
│   └── test_texts.json      # 示例文本库
├── models/                  # 模型缓存目录（自动生成）
├── pyproject.toml           # 项目配置
├── README.md
└── LICENSE
```

---

## 🔧 API接口

### 1. 执行NER识别

**POST** `/api/ner/predict`

**请求体**：
```json
{
  "text": "马云在杭州创立了阿里巴巴"
}
```

**响应**：
```json
{
  "text": "马云在杭州创立了阿里巴巴",
  "entities": [
    {
      "text": "马云",
      "type": "PER",
      "start": 0,
      "end": 2,
      "confidence": 0.98
    },
    {
      "text": "杭州",
      "type": "LOC",
      "start": 3,
      "end": 5,
      "confidence": 0.95
    },
    {
      "text": "阿里巴巴",
      "type": "ORG",
      "start": 7,
      "end": 11,
      "confidence": 0.97
    }
  ],
  "processing_time": 0.234
}
```

### 2. 获取实体类型配置

**GET** `/api/ner/entity-types`

### 3. 获取示例文本

**GET** `/api/ner/examples`

### 完整API文档

启动服务后访问：**http://localhost:8000/docs**

---

## ⚙️ 配置说明

### 自定义实体类型

编辑 `app/config.py`：

```python
ENTITY_TYPES = {
    "PER": {"label": "人名", "color": "#ef4444"},
    "CUSTOM": {"label": "自定义类型", "color": "#your_color"},
}
```

### 更换NER模型

```python
# 支持任何 ModelScope 上的中文NER模型
MODEL_NAME = "your-model-name"
```

### 自定义正则规则

```python
PATTERNS = {
    "CUSTOM_TYPE": re.compile(r'your_regex_pattern'),
}
```

---

## 🎯 使用场景

- 📄 **文档信息提取**：从合同、报告中提取关键信息
- 🔍 **舆情监控**：自动识别新闻中的人物、机构
- 📞 **客户管理**：CRM系统自动提取联系方式
- 🚨 **风险控制**：金融、法律文书中的实体识别
- 📧 **邮件解析**：自动提取邮件中的联系人和地址
- 🎓 **知识图谱**：构建实体关系网络

---

## 🛠️ 技术栈

- **后端框架**：FastAPI
- **NER模型**：ModelScope - damo/nlp_raner_named-entity-recognition_chinese-base-news
- **深度学习**：Transformers 4.49.0
- **前端**：原生 HTML + CSS + JavaScript
- **包管理**：uv / pip

---

## 📊 性能指标

| 指标 | 数值 |
|------|------|
| 模型大小 | ~400MB |
| 首次启动时间 | 2-5分钟（下载模型） |
| 后续启动时间 | <10秒 |
| 短文本识别 | <0.5秒（<50字） |
| 长文本识别 | ~1.3秒（300字） |
| 最大支持长度 | 400字（自动截断） |

---

## ❓ 常见问题

### Q1: 模型下载太慢？
A: 项目已使用 ModelScope 国内镜像，速度约2-3MB/s。如仍有问题，检查网络连接。

### Q2: 识别准确率如何？
A: 
- 语义实体（人名/地名/机构）：置信度0.3-0.99，复杂场景下80%+准确率
- 结构化信息（手机/身份证）：正则匹配，100%准确率（格式标准时）

### Q3: 支持哪些身份证格式？
A: 目前仅支持18位二代身份证号（15位一代证可自行扩展正则）

### Q4: 能否识别英文实体？
A: 当前模型针对中文优化，英文识别效果有限。

### Q5: 如何扩展新的实体类型？
A: 编辑 `app/config.py`，在 `PATTERNS` 中添加正则规则即可。

---

## 🤝 贡献指南

欢迎提交 Issue 和 Pull Request！

1. Fork 本项目
2. 创建特性分支：`git checkout -b feature/AmazingFeature`
3. 提交改动：`git commit -m 'Add some AmazingFeature'`
4. 推送到分支：`git push origin feature/AmazingFeature`
5. 提交 Pull Request

---

## 📄 开源协议

本项目采用 [MIT License](LICENSE) 开源协议。

---

## 🙏 致谢

- [ModelScope](https://modelscope.cn) - 提供高质量中文NER模型
- [FastAPI](https://fastapi.tiangolo.com) - 现代化Python Web框架
- [Transformers](https://huggingface.co/transformers) - NLP模型推理库

---

## 📮 联系方式

- 提交Issue：[GitHub Issues](https://github.com/intelliner/intelliner/issues)
- 项目主页：https://github.com/intelliner/intelliner

---

<div align="center">

**⭐ 如果这个项目对您有帮助，请给一个Star支持！**

Made with ❤️ by IntelliNER Contributors

</div>
