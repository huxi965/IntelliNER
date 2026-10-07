"""FastAPI主程序"""
import sys
import io

# Windows终端默认GBK编码，强制stdout/stderr用UTF-8避免打印emoji时报错
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8")

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
import json

from .models import NERRequest, NERResponse, ExampleText, Entity
from .ner_engine import ner_engine
from .config import (
    API_TITLE, API_VERSION, API_DESCRIPTION,
    ENTITY_TYPES, BASE_DIR
)

# 创建FastAPI应用
app = FastAPI(
    title=API_TITLE,
    version=API_VERSION,
    description=API_DESCRIPTION
)

# CORS配置（允许前端跨域访问）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 挂载静态文件
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")


@app.on_event("startup")
async def startup_event():
    """启动时加载模型"""
    print("🚀 启动NER Demo应用...")
    ner_engine.load_model()
    print("✅ 应用启动完成！")


@app.get("/", response_class=HTMLResponse)
async def read_root():
    """返回前端页面"""
    html_file = BASE_DIR / "static" / "index.html"
    if html_file.exists():
        return html_file.read_text(encoding="utf-8")
    return "<h1>NER Demo</h1><p>请创建 static/index.html 文件</p>"


@app.post("/api/ner/predict", response_model=NERResponse)
async def predict_ner(request: NERRequest):
    """NER识别接口"""
    try:
        entities, processing_time = ner_engine.predict(request.text)

        return NERResponse(
            text=request.text,
            entities=[Entity(**e) for e in entities],
            processing_time=round(processing_time, 4)
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"识别失败: {str(e)}")


@app.get("/api/ner/examples")
async def get_examples():
    """获取示例文本"""
    examples_file = BASE_DIR / "examples" / "test_texts.json"

    if examples_file.exists():
        with open(examples_file, "r", encoding="utf-8") as f:
            examples = json.load(f)
        return examples
    else:
        # 默认示例
        return [
            {
                "title": "科技新闻",
                "text": "马化腾在深圳腾讯大厦宣布，腾讯将与清华大学合作成立AI实验室。"
            }
        ]


@app.get("/api/ner/entity-types")
async def get_entity_types():
    """获取实体类型配置"""
    return ENTITY_TYPES