# IntelliNER - 中文智能实体识别系统

[![GitHub](https://img.shields.io/badge/GitHub-intelliner-blue)](https://github.com/intelliner/intelliner)
[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

> 🎯 开箱即用的中文实体识别，支持人名、地名、机构、手机号、身份证、邮箱、地址、网址等9种实体类型

[English](README.md) | 简体中文

---

## 快速开始

```bash
# 1. 安装依赖
pip install -r requirements.txt

# 2. 启动服务
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000

# 3. 打开浏览器
http://localhost:8000
```

**首次启动**：自动下载模型（约400MB），需等待2-5分钟

---

## 支持的实体类型

| 类型 | 说明 | 示例 |
|------|------|------|
| 👤 人名 | 中文姓名 | 马云、张伟 |
| 📍 地名 | 地理位置 | 北京、杭州西湖 |
| 🏢 机构 | 公司组织 | 阿里巴巴、腾讯 |
| 🎓 大学 | 高等院校 | 清华大学、北京大学 |
| 📱 手机号 | 11位手机号码 | 13800138000 |
| 🆔 身份证 | 18位身份证号 | 110101199001011234 |
| 📧 邮箱 | 电子邮件 | user@example.com |
| 🏠 地址 | 详细地址 | 北京市朝阳区建国路88号 |
| 🔗 网址 | HTTP链接 | https://www.example.com |

---

## 识别示例

**输入**：
```
张三的身份证号码是110101199001011234，手机号13800138000，
邮箱zhangsan@example.com，住址北京市朝阳区建国路88号。
```

**输出**：
- [人名] 张三
- [身份证] 110101199001011234  
- [手机号] 13800138000
- [邮箱] zhangsan@example.com
- [地址] 北京市朝阳区建国路88号

---

## 技术特点

✅ **混合识别**：深度学习模型 + 正则表达式，准确率更高  
✅ **国内优化**：基于ModelScope，模型下载速度快  
✅ **Web界面**：彩色高亮显示，直观易用  
✅ **RESTful API**：方便集成到其他系统  
✅ **开箱即用**：无需训练，下载即跑

---

## API接口

### 识别实体

```bash
curl -X POST http://localhost:8000/api/ner/predict \
  -H "Content-Type: application/json" \
  -d '{"text":"马云在杭州创立阿里巴巴"}'
```

### API文档

启动后访问：http://localhost:8000/docs

---

## 项目结构

```
intelliner/
├── app/              # 后端代码
├── static/           # 前端页面
├── examples/         # 示例文本
├── models/           # 模型缓存（自动生成）
└── README.md
```

---

## 使用场景

- 📄 文档信息提取（合同、报告）
- 📞 客户信息管理（CRM系统）
- 🔍 舆情监控（新闻分析）
- 🚨 风险控制（金融、法律）
- 📧 邮件智能解析

---

## 常见问题

**Q：支持哪些Python版本？**  
A：Python 3.10及以上

**Q：模型在哪下载？**  
A：首次启动自动从ModelScope下载

**Q：能否识别英文？**  
A：当前针对中文优化，英文效果有限

**Q：如何扩展新类型？**  
A：编辑 `app/config.py` 添加正则规则

---

## 开源协议

MIT License - 详见 [LICENSE](LICENSE)

---

## 贡献

欢迎提交 Issue 和 Pull Request！  
详见 [贡献指南](CONTRIBUTING.md)

---

⭐ **如果觉得有用，请给个Star支持！**
