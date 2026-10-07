# IntelliNER 快速部署指南

## 🎯 5分钟快速上手

### 方式一：使用 uv（推荐，速度最快）

```bash
# 1. 克隆项目
git clone https://github.com/intelliner/intelliner.git
cd intelliner

# 2. 使用uv安装依赖（自动创建虚拟环境）
uv sync

# 3. 启动服务
uv run uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### 方式二：使用传统 pip

```bash
# 1. 克隆项目
git clone https://github.com/intelliner/intelliner.git
cd intelliner

# 2. 创建虚拟环境
python -m venv .venv

# 3. 激活虚拟环境
# Windows:
.venv\Scripts\activate
# Linux/Mac:
source .venv/bin/activate

# 4. 安装依赖
pip install -r requirements.txt

# 5. 启动服务
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### 访问应用

浏览器打开：**http://localhost:8000**

---

## ⏱️ 首次启动注意事项

**首次启动会自动下载模型文件（约400MB）**，过程：

1. 看到 `正在从ModelScope加载NER模型...`
2. 下载进度显示（速度约2-3MB/s）
3. 看到 `Application startup complete` 即完成
4. 整个过程约2-5分钟

**后续启动**：模型已缓存，10秒左右即可启动完成。

---

## 🧪 快速测试

### Web界面测试

1. 打开 http://localhost:8000
2. 在示例下拉框选择"案件报告记录"
3. 点击"🚀 开始识别"
4. 查看彩色高亮的识别结果

### API接口测试

```bash
# 测试识别接口
curl -X POST http://localhost:8000/api/ner/predict \
  -H "Content-Type: application/json" \
  -d '{"text":"张三的手机号13800138000，邮箱test@example.com"}'

# 查看API文档
open http://localhost:8000/docs
```

---

## 📦 Docker部署（可选）

```dockerfile
# Dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

```bash
# 构建镜像
docker build -t intelliner .

# 运行容器
docker run -d -p 8000:8000 intelliner
```

---

## ⚙️ 生产环境部署

### 使用 Gunicorn + Uvicorn

```bash
# 安装gunicorn
pip install gunicorn

# 启动（4个worker进程）
gunicorn app.main:app \
  --workers 4 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000
```

### 使用 Nginx 反向代理

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

---

## 🔧 环境变量配置（可选）

创建 `.env` 文件：

```bash
# 服务端口
PORT=8000

# 模型缓存目录
MODEL_CACHE_DIR=./models

# 日志级别
LOG_LEVEL=INFO
```

---

## ❓ 常见启动问题

### 1. 端口被占用

```bash
# Windows查看8000端口占用
netstat -ano | findstr :8000

# 杀掉占用进程（PID替换为实际值）
taskkill /PID 1234 /F

# 或换个端口启动
uvicorn app.main:app --port 8001
```

### 2. 依赖安装失败

```bash
# 使用国内镜像
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### 3. 模型下载失败

检查网络连接，重新启动服务自动重试。

### 4. ImportError

确认已激活虚拟环境，重新安装依赖：
```bash
pip install --force-reinstall -r requirements.txt
```

---

## 📊 性能优化建议

1. **使用SSD**：模型加载速度更快
2. **增加内存**：建议8GB以上
3. **多Worker**：生产环境使用4-8个worker
4. **缓存**：可在前端加Redis缓存识别结果

---

## 🎉 部署成功

服务启动后，你应该看到：

```
INFO:     Started server process [12345]
INFO:     Waiting for application startup.
正在从ModelScope加载NER模型: damo/nlp_raner_named-entity-recognition_chinese-base-news
模型加载成功！
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

现在访问 http://localhost:8000 开始使用吧！
