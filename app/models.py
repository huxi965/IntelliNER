"""Pydantic数据模型"""
from pydantic import BaseModel, Field
from typing import List, Optional


class Entity(BaseModel):
    """实体信息"""
    text: str = Field(..., description="实体文本")
    type: str = Field(..., description="实体类型")
    start: int = Field(..., description="起始位置")
    end: int = Field(..., description="结束位置")
    confidence: float = Field(..., description="置信度", ge=0, le=1)


class NERRequest(BaseModel):
    """NER识别请求"""
    text: str = Field(..., description="待识别文本", min_length=1, max_length=5000)


class NERResponse(BaseModel):
    """NER识别响应"""
    text: str = Field(..., description="原始文本")
    entities: List[Entity] = Field(..., description="识别出的实体列表")
    processing_time: float = Field(..., description="处理耗时（秒）")


class ExampleText(BaseModel):
    """示例文本"""
    title: str = Field(..., description="标题")
    text: str = Field(..., description="文本内容")
