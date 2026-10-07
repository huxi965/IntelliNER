# 贡献指南

感谢您对 IntelliNER 的关注！我们欢迎各种形式的贡献。

## 🤝 如何贡献

### 报告Bug

如发现Bug，请在 [Issues](https://github.com/intelliner/intelliner/issues) 中提交，包含：
- 问题描述
- 复现步骤
- 期望行为
- 实际行为
- 环境信息（OS、Python版本）

### 提出新功能

在 Issues 中提交 Feature Request，说明：
- 功能描述
- 使用场景
- 预期效果

### 提交代码

1. **Fork 项目**
2. **创建特性分支**：`git checkout -b feature/YourFeature`
3. **编写代码**：遵循现有代码风格
4. **编写测试**：确保测试通过
5. **提交改动**：`git commit -m 'Add: YourFeature'`
6. **推送分支**：`git push origin feature/YourFeature`
7. **提交Pull Request**

## 📝 代码规范

### Python代码风格

- 遵循 PEP 8
- 使用有意义的变量名
- 函数添加文档字符串
- 单行不超过120字符

### 提交信息格式

```
类型: 简短描述（不超过50字符）

详细说明（可选）
```

**类型**：
- `Add`: 新增功能
- `Fix`: 修复Bug
- `Update`: 更新功能
- `Refactor`: 重构代码
- `Docs`: 文档更新
- `Style`: 代码格式调整
- `Test`: 测试相关

## ✅ Pull Request检查清单

提交PR前，确认：

- [ ] 代码无语法错误
- [ ] 功能测试通过
- [ ] 更新了相关文档
- [ ] 提交信息清晰明确
- [ ] 无多余的调试代码

## 💡 开发建议

### 添加新的实体类型

编辑 `app/config.py`：

```python
# 1. 在 ENTITY_TYPES 中添加
ENTITY_TYPES = {
    "NEW_TYPE": {"label": "新类型", "color": "#hex_color"},
}

# 2. 在 PATTERNS 中添加正则规则
PATTERNS = {
    "NEW_TYPE": re.compile(r'your_pattern'),
}
```

### 更换NER模型

编辑 `app/config.py`，修改 `MODEL_NAME` 为任何 ModelScope 上的中文NER模型。

## 🙏 感谢贡献者

所有贡献者将在 README.md 中列出，感谢你们的付出！

## 📮 联系方式

- Issue: [GitHub Issues](https://github.com/intelliner/intelliner/issues)
- 讨论区: [GitHub Discussions](https://github.com/intelliner/intelliner/discussions)
