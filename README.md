# IntelliNER

🎯 **中文智能实体识别系统** - 学习Demo

基于 **ModelScope NER模型 + 正则表达式** 的混合识别方案

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-green.svg)](https://fastapi.tiangolo.com)
[![ModelScope](https://img.shields.io/badge/ModelScope-damo/nlp_raner-orange.svg)](https://modelscope.cn)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## 📖 项目简介

这是一个中文命名实体识别(NER)的学习demo，展示如何结合深度学习模型和规则方法实现实体识别。

**核心特点**：
- 🧠 使用 ModelScope 的 `damo/nlp_raner_named-entity-recognition_chinese-base-news` 模型
- 📝 正则表达式识别结构化信息（手机号、身份证、邮箱等）
- 🎨 Web可视化界面展示识别结果
- ⚡ FastAPI后端 + 原生前端，代码简洁易读

---

## ✨ 支持的实体类型

### 语义实体（NER模型识别）
- 👤 **人名** (PER)
- 📍 **地名** (LOC)
- 🏢 **机构** (ORG)
- 🎓 **大学** (EDU)

### 结构化信息（正则表达式）
- 📱 **手机号** (PHONE)
- 🆔 **身份证** (ID_CARD)
- 📧 **邮箱** (EMAIL)
- 🏠 **详细地址** (ADDRESS)
- 🔗 **网址** (URL)

---

## 🎬 效果展示

**输入文本**：
```
张三的身份证号码是110101199001011234，手机号13800138000，
邮箱zhangsan@example.com，住址北京市朝阳区建国路88号。
```

**识别结果**：
- [人名] 张三
- [身份证] 110101199001011234
- [手机号] 13800138000
- [邮箱] zhangsan@example.com
- [地址] 北京市朝阳区建国路88号

---

## 🚀 快速开始

### 1. 安装依赖

```bash
# 克隆项目
git clone https://github.com/huxi965/IntelliNER.git
cd IntelliNER

# 安装依赖（推荐使用uv）
uv sync

# 或使用pip
pip install -r requirements.txt
```

### 2. 启动服务

```bash
# 使用uv
uv run uvicorn app.main:app --host 0.0.0.0 --port 8000

# 或使用python
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### 3. 访问应用

浏览器打开：http://localhost:8000

> ⚠️ **首次启动**：会自动下载模型文件（约400MB），需等待2-5分钟

---

## 📦 项目结构

```
IntelliNER/
├── app/
│   ├── main.py              # FastAPI主程序
│   ├── ner_engine.py        # NER推理引擎（混合识别核心）
│   ├── models.py            # Pydantic数据模型
│   └── config.py            # 配置文件
├── static/
│   ├── index.html           # 前端页面
│   ├── style.css
│   └── app.js
├── examples/
│   └── test_texts.json      # 示例文本
└── README.md
```

---

## 🔧 API接口

### 识别实体

**POST** `/api/ner/predict`

```bash
curl -X POST "http://localhost:8000/api/ner/predict" \
  -H "Content-Type: application/json" \
  -d '{"text":"马云在杭州创立了阿里巴巴"}'
```

**响应示例**：
```json
{
  "text": "马云在杭州创立了阿里巴巴",
  "entities": [
    {"text": "马云", "type": "PER", "start": 0, "end": 2, "confidence": 0.98},
    {"text": "杭州", "type": "LOC", "start": 3, "end": 5, "confidence": 0.95},
    {"text": "阿里巴巴", "type": "ORG", "start": 7, "end": 11, "confidence": 0.97}
  ],
  "processing_time": 0.234
}
```

### API文档

启动服务后访问：http://localhost:8000/docs

---

## ⚙️ 技术实现

### 混合识别策略

1. **NER模型**：使用ModelScope的中文新闻领域NER模型识别语义实体
2. **正则表达式**：识别格式固定的结构化信息
3. **智能合并**：当同一位置有多个识别结果时，优先保留结构化信息

核心代码在 `app/ner_engine.py`：
- `_post_process_entities()` - NER结果后处理
- `_extract_patterns()` - 正则表达式提取
- `_merge_entities()` - 结果合并去重

### 自定义扩展

**添加新的实体类型**（编辑 `app/config.py`）：

```python
# 1. 添加实体类型定义
ENTITY_TYPES = {
    "CUSTOM": {"label": "自定义", "color": "#your_color"},
}

# 2. 添加正则规则
PATTERNS = {
    "CUSTOM": re.compile(r'your_pattern'),
}
```

---

## 🛠️ 技术栈

- **NER模型**：[damo/nlp_raner_named-entity-recognition_chinese-base-news](https://modelscope.cn/models/damo/nlp_raner_named-entity-recognition_chinese-base-news)
- **后端框架**：FastAPI
- **深度学习**：Transformers 4.49.0
- **模型源**：ModelScope（国内下载速度快）
- **前端**：原生 HTML + CSS + JavaScript

---

## 📊 性能参考

| 指标 | 数值 |
|------|------|
| 模型大小 | ~400MB |
| 首次启动 | 2-5分钟（下载模型） |
| 后续启动 | <10秒 |
| 短文本（<50字） | <0.5秒 |
| 长文本（300字） | ~1.3秒 |
| 最大文本长度 | 400字（自动截断） |

---

## ❓ 常见问题

**Q: 为什么使用ModelScope而不是Hugging Face？**  
A: ModelScope是阿里云的模型平台，国内下载速度快（2-3MB/s），Hugging Face直连较慢。

**Q: 能否更换其他NER模型？**  
A: 可以，编辑 `app/config.py` 中的 `MODEL_NAME`，换成任何ModelScope上的中文NER模型。

**Q: 正则规则如何调整？**  
A: 编辑 `app/config.py` 中的 `PATTERNS` 字典，修改正则表达式即可。

**Q: 识别准确率如何？**  
A: 语义实体（人名/地名）依赖模型训练数据，在新闻领域效果较好。结构化信息（手机/邮箱）使用正则匹配，格式标准时准确率100%。

---

## 📄 开源协议

MIT License - 详见 [LICENSE](LICENSE)

---

## 🔗 相关资源

- [ModelScope平台](https://modelscope.cn)
- [FastAPI文档](https://fastapi.tiangolo.com)
- [Transformers文档](https://huggingface.co/docs/transformers)
