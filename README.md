# Sentient Trader

一個 AI 驅動的金融情報平台，透過即時監控 KOL 和新聞來源來分析市場情緒。

## 專案願景

Sentient Trader 旨在橋接市場情緒數據與交易決策之間的差距。我們的平台提供：

- **即時 KOL 監控**: 24/7 監控影響力人物的社交媒體動態
- **情緒分析**: 使用先進 NLP 技術分析通訊內容的情緒和上下文
- **市場關聯**: 將情緒洞察與市場數據視覺化，將抽象情緒轉化為可操作的智能

## 技術架構

### 前端
- **框架**: Streamlit - 快速開發數據中心儀表板
- **視覺化**: Plotly, Altair - 與 Streamlit 完美整合
- **即時更新**: WebSocket 連接

### 後端
- **框架**: FastAPI - 高性能、異步處理
- **API 文檔**: 自動生成 OpenAPI 文檔
- **即時通訊**: WebSocket 支援

### AI/NLP
- **核心庫**: Hugging Face Transformers, Pandas, NumPy
- **RAG 框架**: LangChain
- **LLM 整合**: Google Gemini, OpenAI API

### 資料庫
- **主要資料庫**: PostgreSQL (含 pgvector 擴展)
- **快取**: Redis
- **向量資料庫**: Pinecone (可選)

## 快速開始

### 環境設置

1. 克隆專案：
```bash
git clone <repository-url>
cd Setient_trader
```

2. 建立虛擬環境：
```bash
python -m venv venv
source venv/bin/activate  # macOS/Linux
# 或
venv\Scripts\activate  # Windows
```

3. 安裝依賴：
```bash
pip install -r requirements.txt
```

4. 設置環境變數：
```bash
cp .env.example .env
# 編輯 .env 文件，填入必要的 API 金鑰
```

5. 啟動開發服務器：
```bash
# 啟動後端 API
python -m uvicorn app.main:app --reload --port 8000

# 啟動前端 Streamlit
streamlit run frontend/main.py --server.port 8501
```

## 專案結構

```
Setient_trader/
├── app/                    # FastAPI 後端
│   ├── api/               # API 路由
│   ├── core/              # 核心配置
│   ├── models/            # 資料模型
│   ├── services/          # 業務邏輯
│   └── utils/             # 工具函數
├── frontend/              # Streamlit 前端
│   ├── pages/             # 頁面組件
│   ├── components/        # 可重用組件
│   └── utils/             # 前端工具
├── ai/                    # AI/NLP 模組
│   ├── models/            # AI 模型
│   ├── sentiment/         # 情緒分析
│   └── rag/               # RAG 實現
├── data/                  # 資料處理
│   ├── fetchers/          # 資料獲取器
│   └── processors/        # 資料處理器
├── tests/                 # 測試文件
├── docker/                # Docker 配置
└── docs/                  # 文檔
```

## MVP 功能

1. **即時 KOL 監控牆**: 多欄位儀表板顯示指定 KOL 的即時社交媒體動態
2. **情緒與價格時間軸**: 互動式圖表，將股票價格與對應情緒指數疊加
3. **智能警報系統**: 可配置的通知系統，基於觸發條件
4. **關聯分析器**: 計算 KOL 情緒分數與股票價格的皮爾遜相關係數

## 開發階段

- [x] Phase 1: 定義 MVP 和原型設計
- [ ] Phase 2: 後端和 AI 核心開發
- [ ] Phase 3: 前端開發
- [ ] Phase 4: 測試和部署

## 貢獻指南

請參考 `CONTRIBUTING.md` 了解如何參與專案開發。

## 授權

本專案採用 MIT 授權 - 詳見 `LICENSE` 文件。 