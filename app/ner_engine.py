"""NER推理引擎（基于ModelScope）"""
import time
from typing import List, Dict

from .config import MODEL_NAME, MODEL_CACHE_DIR, UNIVERSITY_KEYWORDS, RAW_LABEL_MAPPING, PATTERNS


class NEREngine:
    """NER推理引擎"""

    def __init__(self):
        self.pipeline = None

    def load_model(self):
        """加载模型（启动时调用）"""
        from modelscope.pipelines import pipeline
        from modelscope.utils.constant import Tasks

        print(f"正在从ModelScope加载NER模型: {MODEL_NAME}")
        print(f"模型缓存目录: {MODEL_CACHE_DIR}")

        try:
            self.pipeline = pipeline(
                task=Tasks.named_entity_recognition,
                model=MODEL_NAME,
                cache_dir=str(MODEL_CACHE_DIR)
            )
            print("模型加载成功！")

        except Exception as e:
            print(f"模型加载失败: {e}")
            raise

    def _post_process_entities(self, text: str, raw_entities: List[Dict]) -> List[Dict]:
        """
        将ModelScope输出转换为统一格式，并把ORG中的大学单独标记为EDU
        ModelScope输出格式: [{"type": "PER", "start": 0, "end": 2, "span": "马云"}, ...]
        """
        processed = []
        for entity in raw_entities:
            raw_type = entity["type"]
            entity_type = RAW_LABEL_MAPPING.get(raw_type, raw_type)
            entity_text = entity["span"]

            # 如果是ORG类型，检查是否包含大学关键词
            if entity_type == "ORG":
                if any(keyword in entity_text for keyword in UNIVERSITY_KEYWORDS):
                    entity_type = "EDU"

            processed.append({
                "text": entity_text,
                "type": entity_type,
                "start": entity["start"],
                "end": entity["end"],
                "confidence": round(entity.get("prob", 1.0), 4)
            })

        return processed

    def _extract_patterns(self, text: str) -> List[Dict]:
        """
        用正则表达式提取结构化信息（手机号、身份证、邮箱等）
        """
        pattern_entities = []

        for entity_type, pattern in PATTERNS.items():
            for match in pattern.finditer(text):
                pattern_entities.append({
                    "text": match.group(),
                    "type": entity_type,
                    "start": match.start(),
                    "end": match.end(),
                    "confidence": 1.0  # 正则匹配置信度设为1.0
                })

        return pattern_entities

    def _merge_entities(self, ner_entities: List[Dict], pattern_entities: List[Dict]) -> List[Dict]:
        """
        合并NER模型和正则识别的结果，处理重叠情况
        规则：
        1. 结构化信息（手机、身份证等）优先级高，覆盖NER结果
        2. 完整地址（ADDRESS）优先级高于单独的地名（LOC）
        3. 去重：同一位置只保留优先级最高的实体
        """
        # 优先级定义（数字越大优先级越高）
        PRIORITY = {
            "LOC": 1,
            "PER": 2,
            "ORG": 2,
            "EDU": 2,
            "ADDRESS": 3,  # 详细地址优先于地名
            "PHONE": 4,
            "ID_CARD": 4,
            "EMAIL": 4,
            "URL": 4,
        }

        all_entities = ner_entities + pattern_entities

        # 按起始位置排序
        all_entities.sort(key=lambda x: x["start"])

        # 去重：如果两个实体有重叠，保留优先级高的
        merged = []
        for entity in all_entities:
            # 检查是否与已有实体重叠
            overlapped = False
            for i, existing in enumerate(merged):
                # 判断是否重叠：[start1, end1) 与 [start2, end2) 有交集
                if not (entity["end"] <= existing["start"] or entity["start"] >= existing["end"]):
                    overlapped = True
                    # 如果当前实体优先级更高，替换已有实体
                    if PRIORITY.get(entity["type"], 0) > PRIORITY.get(existing["type"], 0):
                        merged[i] = entity
                    break

            if not overlapped:
                merged.append(entity)

        # 按起始位置重新排序
        merged.sort(key=lambda x: x["start"])

        return merged

    def predict(self, text: str) -> tuple[List[Dict], float]:
        """
        执行NER识别
        返回: (实体列表, 处理时间)
        """
        if not self.pipeline:
            raise RuntimeError("模型未加载，请先调用load_model()")

        start_time = time.time()

        # 文本长度保护：模型最大支持512 token，约350-400个中文字
        # 超长文本自动截断，避免推理时tensor维度不匹配报错
        MAX_TEXT_LENGTH = 400
        original_length = len(text)
        if original_length > MAX_TEXT_LENGTH:
            text = text[:MAX_TEXT_LENGTH]
            print(f"⚠️ 输入文本过长({original_length}字)，已自动截断至{MAX_TEXT_LENGTH}字")

        # 执行推理
        result = self.pipeline(text)
        raw_entities = result.get("output", [])

        # NER模型后处理
        ner_entities = self._post_process_entities(text, raw_entities)

        # 正则提取结构化信息
        pattern_entities = self._extract_patterns(text)

        # 合并两种识别结果
        entities = self._merge_entities(ner_entities, pattern_entities)

        processing_time = time.time() - start_time

        return entities, processing_time


# 全局单例
ner_engine = NEREngine()
