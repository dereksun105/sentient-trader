"""
Sentient Trader - 情緒分析服務
使用 Hugging Face Transformers 進行文本情緒分析
"""

from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification
import torch
import numpy as np
from typing import Dict, List, Any, Optional
import structlog
from datetime import datetime

from app.core.config import settings

logger = structlog.get_logger()


class SentimentAnalyzer:
    """
    情緒分析器類
    使用預訓練模型進行文本情緒分析
    """
    
    def __init__(self, model_name: str = None):
        """
        初始化情緒分析器
        
        Args:
            model_name: 模型名稱，如果為 None 則使用配置中的默認模型
        """
        self.model_name = model_name or settings.SENTIMENT_MODEL
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        
        logger.info(f"初始化情緒分析器: {self.model_name} on {self.device}")
        
        try:
            # 載入模型和分詞器
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
            self.model = AutoModelForSequenceClassification.from_pretrained(self.model_name)
            
            # 移動到 GPU（如果可用）
            self.model.to(self.device)
            
            # 創建 pipeline
            self.pipeline = pipeline(
                "sentiment-analysis",
                model=self.model,
                tokenizer=self.tokenizer,
                device=0 if self.device == "cuda" else -1
            )
            
            logger.info("情緒分析器初始化成功")
            
        except Exception as e:
            logger.error(f"情緒分析器初始化失敗: {e}")
            raise
    
    def analyze_text(self, text: str) -> Dict[str, Any]:
        """
        分析單個文本的情緒
        
        Args:
            text: 要分析的文本
            
        Returns:
            包含情緒分析結果的字典
        """
        try:
            # 使用 pipeline 進行分析
            result = self.pipeline(text)[0]
            
            # 標準化情緒分數到 -1 到 1 範圍
            sentiment_score = self._normalize_sentiment_score(result)
            
            # 確定情緒標籤
            sentiment_label = self._get_sentiment_label(sentiment_score)
            
            # 計算置信度
            confidence_score = result.get('score', 0.0)
            
            return {
                'sentiment_score': sentiment_score,
                'sentiment_label': sentiment_label,
                'confidence_score': confidence_score,
                'raw_result': result,
                'model_used': self.model_name,
                'analysis_timestamp': datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"情緒分析失敗: {e}")
            return {
                'sentiment_score': 0.0,
                'sentiment_label': 'neutral',
                'confidence_score': 0.0,
                'error': str(e),
                'model_used': self.model_name,
                'analysis_timestamp': datetime.utcnow().isoformat()
            }
    
    def analyze_batch(self, texts: List[str]) -> List[Dict[str, Any]]:
        """
        批量分析文本情緒
        
        Args:
            texts: 要分析的文本列表
            
        Returns:
            情緒分析結果列表
        """
        results = []
        
        for text in texts:
            result = self.analyze_text(text)
            results.append(result)
        
        return results
    
    def _normalize_sentiment_score(self, result: Dict[str, Any]) -> float:
        """
        將模型輸出標準化到 -1 到 1 範圍
        
        Args:
            result: 模型原始輸出
            
        Returns:
            標準化的情緒分數
        """
        label = result.get('label', '').lower()
        score = result.get('score', 0.0)
        
        # 根據模型輸出調整標準化邏輯
        if 'positive' in label:
            return score
        elif 'negative' in label:
            return -score
        elif 'neutral' in label:
            return 0.0
        else:
            # 對於其他標籤，使用分數作為基礎
            return (score - 0.5) * 2  # 將 0-1 範圍轉換為 -1 到 1
    
    def _get_sentiment_label(self, sentiment_score: float) -> str:
        """
        根據情緒分數確定情緒標籤
        
        Args:
            sentiment_score: 情緒分數
            
        Returns:
            情緒標籤
        """
        if sentiment_score > 0.1:
            return 'positive'
        elif sentiment_score < -0.1:
            return 'negative'
        else:
            return 'neutral'
    
    def get_model_info(self) -> Dict[str, Any]:
        """
        獲取模型資訊
        
        Returns:
            模型資訊字典
        """
        return {
            'model_name': self.model_name,
            'device': self.device,
            'model_type': type(self.model).__name__,
            'tokenizer_type': type(self.tokenizer).__name__,
            'max_length': self.tokenizer.model_max_length if hasattr(self.tokenizer, 'model_max_length') else None
        }


class NamedEntityRecognizer:
    """
    命名實體識別器
    用於識別文本中的公司名稱和股票代碼
    """
    
    def __init__(self, model_name: str = None):
        """
        初始化命名實體識別器
        
        Args:
            model_name: 模型名稱，如果為 None 則使用配置中的默認模型
        """
        self.model_name = model_name or settings.NER_MODEL
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        
        logger.info(f"初始化命名實體識別器: {self.model_name}")
        
        try:
            # 載入 NER pipeline
            self.pipeline = pipeline(
                "ner",
                model=self.model_name,
                device=0 if self.device == "cuda" else -1
            )
            
            logger.info("命名實體識別器初始化成功")
            
        except Exception as e:
            logger.error(f"命名實體識別器初始化失敗: {e}")
            raise
    
    def extract_entities(self, text: str) -> Dict[str, List[str]]:
        """
        從文本中提取實體
        
        Args:
            text: 要分析的文本
            
        Returns:
            包含提取實體的字典
        """
        try:
            entities = self.pipeline(text)
            
            # 分類實體
            companies = []
            stocks = []
            locations = []
            persons = []
            
            for entity in entities:
                entity_text = entity['word']
                entity_type = entity['entity']
                
                if entity_type in ['ORG', 'MISC']:
                    # 檢查是否為股票代碼（大寫字母，通常 1-5 個字符）
                    if entity_text.isupper() and len(entity_text) <= 5:
                        stocks.append(entity_text)
                    else:
                        companies.append(entity_text)
                elif entity_type == 'LOC':
                    locations.append(entity_text)
                elif entity_type == 'PER':
                    persons.append(entity_text)
            
            return {
                'companies': list(set(companies)),
                'stocks': list(set(stocks)),
                'locations': list(set(locations)),
                'persons': list(set(persons))
            }
            
        except Exception as e:
            logger.error(f"實體提取失敗: {e}")
            return {
                'companies': [],
                'stocks': [],
                'locations': [],
                'persons': []
            }


class SentimentAnalysisService:
    """
    情緒分析服務
    整合情緒分析和實體識別功能
    """
    
    def __init__(self):
        """
        初始化情緒分析服務
        """
        self.sentiment_analyzer = SentimentAnalyzer()
        self.entity_recognizer = NamedEntityRecognizer()
        
        logger.info("情緒分析服務初始化完成")
    
    def analyze_social_media_post(self, text: str, kol_id: int, post_id: int) -> Dict[str, Any]:
        """
        分析社交媒體貼文
        
        Args:
            text: 貼文內容
            kol_id: KOL ID
            post_id: 貼文 ID
            
        Returns:
            完整的分析結果
        """
        try:
            # 情緒分析
            sentiment_result = self.sentiment_analyzer.analyze_text(text)
            
            # 實體識別
            entities = self.entity_recognizer.extract_entities(text)
            
            # 組合結果
            analysis_result = {
                'post_id': post_id,
                'kol_id': kol_id,
                'sentiment_score': sentiment_result['sentiment_score'],
                'sentiment_label': sentiment_result['sentiment_label'],
                'confidence_score': sentiment_result['confidence_score'],
                'mentioned_stocks': entities['stocks'],
                'mentioned_companies': entities['companies'],
                'model_used': sentiment_result['model_used'],
                'analysis_timestamp': datetime.utcnow().isoformat()
            }
            
            logger.info(f"完成貼文分析: post_id={post_id}, sentiment={sentiment_result['sentiment_label']}")
            return analysis_result
            
        except Exception as e:
            logger.error(f"貼文分析失敗: {e}")
            return {
                'post_id': post_id,
                'kol_id': kol_id,
                'sentiment_score': 0.0,
                'sentiment_label': 'neutral',
                'confidence_score': 0.0,
                'mentioned_stocks': [],
                'mentioned_companies': [],
                'error': str(e),
                'model_used': self.sentiment_analyzer.model_name,
                'analysis_timestamp': datetime.utcnow().isoformat()
            }
    
    def get_service_info(self) -> Dict[str, Any]:
        """
        獲取服務資訊
        
        Returns:
            服務資訊字典
        """
        return {
            'sentiment_model': self.sentiment_analyzer.get_model_info(),
            'ner_model': self.entity_recognizer.model_name,
            'device': self.sentiment_analyzer.device
        } 