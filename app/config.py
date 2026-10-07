"""配置文件"""
from pathlib import Path

# 项目根目录
BASE_DIR = Path(__file__).resolve().parent.parent

# 模型配置（ModelScope模型，国内下载速度快）
MODEL_NAME = "damo/nlp_raner_named-entity-recognition_chinese-base-news"
MODEL_CACHE_DIR = BASE_DIR / "models"

# ModelScope原始标签 -> 本系统统一标签映射
RAW_LABEL_MAPPING = {
    "PER": "PER",
    "LOC": "LOC",
    "GPE": "LOC",   # 地理政治实体，归并为地名
    "ORG": "ORG",
}

# 实体类型配置
ENTITY_TYPES = {
    "PER": {"label": "人名", "color": "#ef4444"},      # 红色
    "LOC": {"label": "地名", "color": "#3b82f6"},      # 蓝色
    "ORG": {"label": "机构", "color": "#10b981"},      # 绿色
    "EDU": {"label": "大学", "color": "#8b5cf6"},      # 紫色
    "PHONE": {"label": "手机号", "color": "#f59e0b"},  # 橙色
    "ID_CARD": {"label": "身份证", "color": "#ec4899"},# 粉色
    "EMAIL": {"label": "邮箱", "color": "#06b6d4"},    # 青色
    "ADDRESS": {"label": "地址", "color": "#84cc16"},  # 黄绿色
    "URL": {"label": "网址", "color": "#a855f7"},      # 紫罗兰
}

# 大学关键词（用于ORG细分为EDU）
UNIVERSITY_KEYWORDS = [
    "大学", "学院", "高校", "University", "College",
    "师范", "理工", "科技大学", "医科大学"
]

# API配置
API_TITLE = "IntelliNER - 中文智能实体识别API"
API_VERSION = "1.0.0"
API_DESCRIPTION = """
命名实体识别(NER)演示系统

支持识别：
- 人名 (PER)
- 地名 (LOC)
- 机构 (ORG)
- 大学 (EDU)
- 手机号 (PHONE)
- 身份证号 (ID_CARD)
- 邮箱 (EMAIL)
- 地址 (ADDRESS)
- 网址 (URL)
"""

# 正则表达式模式（用于结构化信息识别）
import re

PATTERNS = {
    # 手机号：1开头11位数字
    "PHONE": re.compile(r'1[3-9]\d{9}'),

    # 身份证号：18位数字或17位数字+X
    "ID_CARD": re.compile(r'\d{17}[\dXx]'),

    # 邮箱
    "EMAIL": re.compile(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'),

    # URL
    "URL": re.compile(r'https?://[^\s一-龥]+'),

    # 详细地址：省/市/区 + 街道/路/小区等 + 号/栋/室
    "ADDRESS": re.compile(
        r'(?:[一-龥]{2,4}?(?:省|市|自治区|特别行政区))?'
        r'[一-龥]{2,10}?(?:市|县|区|旗)'
        r'[一-龥]{2,20}?(?:街道|路|大道|胡同|村|镇|乡)'
        r'[一-龥\d号楼栋单元室\-#]{2,30}'
    ),
}
