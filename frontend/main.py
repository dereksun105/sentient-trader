"""
Sentient Trader - Streamlit 前端主頁面
AI 驅動的金融情報平台前端
"""

import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import time
from typing import Dict, List, Any
import json

# 頁面配置
st.set_page_config(
    page_title="Sentient Trader",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 自定義 CSS - 支援深色模式
st.markdown("""
<style>
    /* 主要標題 */
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    /* 指標卡片 - 支援深色模式 */
    .metric-card {
        background-color: rgba(240, 242, 246, 0.1);
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    /* 深色模式下的指標卡片 */
    @media (prefers-color-scheme: dark) {
        .metric-card {
            background-color: rgba(30, 30, 30, 0.8);
            border: 1px solid rgba(255, 255, 255, 0.2);
            color: #ffffff;
        }
    }
    
    /* 情緒顏色 */
    .sentiment-positive {
        color: #28a745 !important;
    }
    .sentiment-negative {
        color: #dc3545 !important;
    }
    .sentiment-neutral {
        color: #6c757d !important;
    }
    
    /* 深色模式下的文字顏色 */
    @media (prefers-color-scheme: dark) {
        .metric-card h4 {
            color: #ffffff !important;
        }
        .metric-card h2 {
            color: #ffffff !important;
        }
        .metric-card p {
            color: #ffffff !important;
        }
    }
    
    /* 確保所有文字在深色模式下可見 */
    .stMarkdown, .stText, .stMetric {
        color: inherit !important;
    }
    
    /* 深色模式下的圖表背景 */
    .js-plotly-plot {
        background-color: transparent !important;
    }
    
    /* 深色模式下的表格樣式 */
    .dataframe {
        background-color: transparent !important;
    }
    
    /* 深色模式下的選擇器樣式 */
    .stSelectbox, .stTextInput, .stSlider {
        background-color: rgba(255, 255, 255, 0.1) !important;
        color: #ffffff !important;
    }
    
    /* 深色模式下的按鈕樣式 */
    .stButton > button {
        background-color: #1f77b4 !important;
        color: #ffffff !important;
        border: none !important;
    }
    
    .stButton > button:hover {
        background-color: #1565c0 !important;
    }
    
    /* 深色模式下的聊天界面 */
    .stChatMessage {
        background-color: rgba(255, 255, 255, 0.1) !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
    }
    
    /* 深色模式下的展開器樣式 */
    .streamlit-expanderHeader {
        background-color: rgba(255, 255, 255, 0.1) !important;
        color: #ffffff !important;
    }
    
    /* 深色模式下的側邊欄 */
    .css-1d391kg {
        background-color: rgba(30, 30, 30, 0.9) !important;
    }
    
    /* 深色模式下的主內容區域 */
    .main .block-container {
        background-color: transparent !important;
    }
</style>
""", unsafe_allow_html=True)

# API 配置
API_BASE_URL = "http://localhost:8000/api/v1"


def call_api(endpoint: str, method: str = "GET", data: Dict = None) -> Dict:
    """
    調用後端 API
    """
    try:
        url = f"{API_BASE_URL}/{endpoint}"
        if method == "GET":
            response = requests.get(url)
        elif method == "POST":
            response = requests.post(url, json=data)
        elif method == "PUT":
            response = requests.put(url, json=data)
        else:
            return {"error": "不支援的 HTTP 方法"}
        
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"API 錯誤: {response.status_code}"}
    except requests.exceptions.RequestException as e:
        return {"error": f"連接錯誤: {str(e)}"}


def get_mock_kols_data():
    """
    獲取模擬 KOL 數據
    """
    return {
        "kols": [
            {
                "id": 1,
                "name": "Elon Musk",
                "platform": "Twitter",
                "username": "@elonmusk",
                "influence_score": 0.95,
                "followers_count": 150000000,
                "is_active": True
            },
            {
                "id": 2,
                "name": "Cathie Wood",
                "platform": "Twitter",
                "username": "@CathieDWood",
                "influence_score": 0.85,
                "followers_count": 2500000,
                "is_active": True
            },
            {
                "id": 3,
                "name": "Chamath Palihapitiya",
                "platform": "Twitter",
                "username": "@chamath",
                "influence_score": 0.78,
                "followers_count": 1200000,
                "is_active": True
            },
            {
                "id": 4,
                "name": "Mark Cuban",
                "platform": "Twitter",
                "username": "@mcuban",
                "influence_score": 0.72,
                "followers_count": 8500000,
                "is_active": True
            },
            {
                "id": 5,
                "name": "Warren Buffett",
                "platform": "News",
                "username": "Berkshire Hathaway",
                "influence_score": 0.88,
                "followers_count": 5000000,
                "is_active": False
            }
        ]
    }


def get_mock_posts_data():
    """
    獲取模擬貼文數據
    """
    return {
        "posts": [
            {
                "id": 1,
                "kol_id": 1,
                "content": "Tesla stock looking strong today! 🚀",
                "sentiment_score": 0.8,
                "created_at": "2024-01-15T10:30:00Z"
            },
            {
                "id": 2,
                "kol_id": 2,
                "content": "ARKK continues to show resilience in this market environment",
                "sentiment_score": 0.6,
                "created_at": "2024-01-15T09:15:00Z"
            },
            {
                "id": 3,
                "kol_id": 1,
                "content": "SpaceX making incredible progress with Starship",
                "sentiment_score": 0.9,
                "created_at": "2024-01-15T08:45:00Z"
            }
        ]
    }


def get_mock_dashboard_data():
    """
    獲取模擬儀表板數據
    """
    return {
        "active_kols": 4,
        "today_posts": 12,
        "avg_sentiment": 0.65,
        "active_alerts": 3,
        "greed_fear_index": 72,  # 0-100, 0=極度恐懼, 100=極度貪婪
        "market_sentiment": "貪婪"
    }


def display_header():
    """
    顯示頁面標題
    """
    st.markdown('<h1 class="main-header">📈 Sentient Trader</h1>', unsafe_allow_html=True)
    st.markdown("### AI 驅動的金融情報平台")
    st.markdown("---")


def display_metrics():
    """
    顯示關鍵指標
    """
    st.subheader("📊 關鍵指標")
    
    # 使用模擬數據
    dashboard_data = get_mock_dashboard_data()
    
    # 創建指標卡片
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <h4>活躍 KOL</h4>
            <h2>{dashboard_data['active_kols']}</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <h4>今日貼文</h4>
            <h2>{dashboard_data['today_posts']}</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <h4>平均情緒</h4>
            <h2>{dashboard_data['avg_sentiment']:.2f}</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <h4>活躍警報</h4>
            <h2>{dashboard_data['active_alerts']}</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col5:
        # 貪婪恐懼指數
        greed_fear = dashboard_data['greed_fear_index']
        sentiment = dashboard_data['market_sentiment']
        
        # 根據指數決定顏色
        if greed_fear >= 75:
            color = "#dc3545"  # 紅色 - 極度貪婪
            emoji = "😱"
        elif greed_fear >= 60:
            color = "#ffc107"  # 黃色 - 貪婪
            emoji = "😰"
        elif greed_fear >= 40:
            color = "#28a745"  # 綠色 - 中性
            emoji = "😐"
        elif greed_fear >= 25:
            color = "#17a2b8"  # 藍色 - 恐懼
            emoji = "😨"
        else:
            color = "#6f42c1"  # 紫色 - 極度恐懼
            emoji = "😱"
        
        st.markdown(f"""
        <div class="metric-card">
            <h4>貪婪恐懼指數 {emoji}</h4>
            <h2 style="color: {color};">{greed_fear}</h2>
            <p style="color: {color}; font-size: 0.9em;">{sentiment}</p>
        </div>
        """, unsafe_allow_html=True)


def display_kol_monitoring():
    """
    顯示 KOL 監控牆
    """
    st.subheader("👥 KOL 監控牆")
    
    # 使用模擬數據
    kols_data = get_mock_kols_data()
    
    # 顯示 KOL 列表
    for kol in kols_data["kols"][:5]:  # 只顯示前 5 個
        with st.expander(f"@{kol.get('username', 'Unknown')} - {kol.get('name', 'Unknown')}"):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.write(f"**平台:** {kol.get('platform', 'Unknown')}")
                st.write(f"**粉絲數:** {kol.get('followers_count', 0):,}")
            
            with col2:
                st.write(f"**影響力評分:** {kol.get('influence_score', 0.0):.3f}")
                status = "活躍" if kol.get('is_active', False) else "非活躍"
                st.write(f"**狀態:** {status}")
            
            with col3:
                if st.button(f"查看詳情", key=f"kol_{kol.get('id')}"):
                    st.write("詳細資訊將在未來版本中實現")


def display_sentiment_timeline():
    """
    顯示情緒與價格時間軸（蠟燭圖）
    """
    st.subheader("📈 情緒與價格時間軸")
    
    # 股票選擇器和時間框架
    col1, col2, col3 = st.columns(3)
    
    with col1:
        stock_symbol = st.text_input("股票代碼", value="AAPL", placeholder="例如: AAPL, TSLA, MSFT")
    
    with col2:
        timeframe = st.selectbox(
            "時間框架",
            ["1D", "1W", "1M", "3M", "6M", "1Y"],
            index=2  # 默認選擇 1M
        )
    
    with col3:
        # 根據時間框架設置默認天數
        timeframe_days = {
            "1D": 1,
            "1W": 7,
            "1M": 30,
            "3M": 90,
            "6M": 180,
            "1Y": 365
        }
        days = st.slider("時間範圍（天）", min_value=1, max_value=365, value=timeframe_days[timeframe])
    
    if st.button("生成圖表"):
        # 根據時間框架調整數據頻率
        if timeframe == "1D":
            freq = 'H'  # 小時
            base_price = 150
        elif timeframe == "1W":
            freq = '4H'  # 4小時
            base_price = 150
        elif timeframe == "1M":
            freq = 'D'  # 天
            base_price = 150
        elif timeframe == "3M":
            freq = 'W'  # 週
            base_price = 150
        elif timeframe == "6M":
            freq = 'W'  # 週
            base_price = 145
        else:  # 1Y
            freq = 'M'  # 月
            base_price = 140
        
        # 生成日期範圍
        dates = pd.date_range(start=datetime.now() - timedelta(days=days), end=datetime.now(), freq=freq)
        
        # 生成蠟燭圖數據 (OHLC)
        import random
        random.seed(42)  # 固定隨機種子以保持一致性
        
        ohlc_data = []
        sentiment_data = []
        current_price = base_price
        
        for i, date in enumerate(dates):
            # 生成開盤價
            if i == 0:
                open_price = current_price
            else:
                open_price = ohlc_data[-1]['close']
            
            # 生成高低收盤價
            volatility = 0.02 if timeframe in ["1D", "1W"] else 0.015 if timeframe in ["1M", "3M"] else 0.01
            price_change = random.uniform(-volatility, volatility) * open_price
            
            close_price = open_price + price_change
            high_price = max(open_price, close_price) + random.uniform(0, volatility * open_price * 0.5)
            low_price = min(open_price, close_price) - random.uniform(0, volatility * open_price * 0.5)
            
            # 確保低價不會為負
            low_price = max(low_price, open_price * 0.95)
            
            ohlc_data.append({
                'date': date,
                'open': round(open_price, 2),
                'high': round(high_price, 2),
                'low': round(low_price, 2),
                'close': round(close_price, 2)
            })
            
            # 生成情緒數據
            sentiment = random.uniform(-0.5, 0.5)
            sentiment_data.append(round(sentiment, 3))
            
            current_price = close_price
        
        # 創建蠟燭圖
        fig = go.Figure()
        
        # 添加蠟燭圖
        fig.add_trace(go.Candlestick(
            x=[d['date'] for d in ohlc_data],
            open=[d['open'] for d in ohlc_data],
            high=[d['high'] for d in ohlc_data],
            low=[d['low'] for d in ohlc_data],
            close=[d['close'] for d in ohlc_data],
            name=f'{stock_symbol} 股價',
            increasing_line_color='#26a69a',  # 綠色 - 上漲
            decreasing_line_color='#ef5350',   # 紅色 - 下跌
            increasing_fillcolor='#26a69a',
            decreasing_fillcolor='#ef5350'
        ))
        
        # 添加情緒線（在次座標軸）
        fig.add_trace(go.Scatter(
            x=[d['date'] for d in ohlc_data],
            y=sentiment_data,
            name='情緒分數',
            yaxis='y2',
            line=dict(color='#2196F3', width=2),
            mode='lines+markers',
            marker=dict(size=4)
        ))
        
        # 添加移動平均線
        if len(ohlc_data) > 5:
            ma_period = min(5, len(ohlc_data) // 4)
            ma_values = []
            for i in range(len(ohlc_data)):
                if i < ma_period - 1:
                    ma_values.append(None)
                else:
                    ma = sum(ohlc_data[j]['close'] for j in range(i - ma_period + 1, i + 1)) / ma_period
                    ma_values.append(round(ma, 2))
            
            fig.add_trace(go.Scatter(
                x=[d['date'] for d in ohlc_data],
                y=ma_values,
                name=f'{ma_period}期移動平均',
                line=dict(color='#FF9800', width=2, dash='dash')
            ))
        
        # 更新佈局 - 支援深色模式
        fig.update_layout(
            title=f"{stock_symbol} 股價蠟燭圖與情緒分析 ({timeframe})",
            xaxis_title="日期",
            yaxis_title="股價 ($)",
            yaxis2=dict(
                title="情緒分數",
                side="right",
                overlaying="y",
                range=[-1, 1],
                gridcolor='rgba(255,255,255,0.1)',
                zerolinecolor='rgba(255,255,255,0.1)'
            ),
            hovermode='x unified',
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            ),
            height=600,
            # 深色模式支援
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#ffffff'),
            xaxis=dict(
                gridcolor='rgba(255,255,255,0.1)',
                zerolinecolor='rgba(255,255,255,0.1)'
            ),
            yaxis=dict(
                gridcolor='rgba(255,255,255,0.1)',
                zerolinecolor='rgba(255,255,255,0.1)'
            )
        )
        
        # 添加成交量（模擬）
        if timeframe in ["1D", "1W", "1M"]:
            volume_data = [random.randint(1000000, 5000000) for _ in range(len(ohlc_data))]
            
            # 創建成交量圖
            volume_fig = go.Figure()
            volume_fig.add_trace(go.Bar(
                x=[d['date'] for d in ohlc_data],
                y=volume_data,
                name='成交量',
                marker_color='#9E9E9E',
                opacity=0.7
            ))
            
            volume_fig.update_layout(
                title=f"{stock_symbol} 成交量 ({timeframe})",
                xaxis_title="日期",
                yaxis_title="成交量",
                height=300,
                # 深色模式支援
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#ffffff'),
                xaxis=dict(
                    gridcolor='rgba(255,255,255,0.1)',
                    zerolinecolor='rgba(255,255,255,0.1)'
                ),
                yaxis=dict(
                    gridcolor='rgba(255,255,255,0.1)',
                    zerolinecolor='rgba(255,255,255,0.1)'
                )
            )
            
            # 顯示圖表
            st.plotly_chart(fig, use_container_width=True)
            st.plotly_chart(volume_fig, use_container_width=True)
        else:
            st.plotly_chart(fig, use_container_width=True)
        
        # 顯示統計信息
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            latest_price = ohlc_data[-1]['close']
            price_change = latest_price - ohlc_data[0]['close']
            price_change_pct = (price_change / ohlc_data[0]['close']) * 100
            color = "#26a69a" if price_change >= 0 else "#ef5350"
            st.metric(
                "當前價格", 
                f"${latest_price:.2f}",
                f"{price_change:+.2f} ({price_change_pct:+.2f}%)",
                delta_color="normal"
            )
        
        with col2:
            high_price = max(d['high'] for d in ohlc_data)
            st.metric("最高價", f"${high_price:.2f}")
        
        with col3:
            low_price = min(d['low'] for d in ohlc_data)
            st.metric("最低價", f"${low_price:.2f}")
        
        with col4:
            avg_sentiment = sum(sentiment_data) / len(sentiment_data)
            sentiment_emoji = "📈" if avg_sentiment > 0 else "📉" if avg_sentiment < 0 else "➡️"
            st.metric(
                "平均情緒", 
                f"{avg_sentiment:.3f}",
                f"{sentiment_emoji} {'正面' if avg_sentiment > 0 else '負面' if avg_sentiment < 0 else '中性'}"
            )


def display_alerts():
    """
    顯示警報系統
    """
    st.subheader("🚨 智能警報系統")
    
    # 警報配置
    with st.expander("創建新警報"):
        alert_name = st.text_input("警報名稱")
        alert_type = st.selectbox("警報類型", ["情緒閾值", "KOL 提及", "股票提及"])
        
        col1, col2 = st.columns(2)
        with col1:
            threshold = st.number_input("閾值", min_value=-1.0, max_value=1.0, value=0.5, step=0.1)
        with col2:
            kol_username = st.text_input("KOL 用戶名（可選）")
        
        if st.button("創建警報"):
            st.success("警報創建成功！")
    
    # 現有警報列表
    st.write("**現有警報:**")
    
    # 模擬警報數據
    alerts = [
        {"name": "Tesla 高情緒警報", "type": "情緒閾值", "status": "活躍", "triggered": 3},
        {"name": "Elon Musk 提及警報", "type": "KOL 提及", "status": "活躍", "triggered": 5},
        {"name": "AAPL 價格波動警報", "type": "股票提及", "status": "非活躍", "triggered": 0}
    ]
    
    for alert in alerts:
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.write(f"**{alert['name']}**")
        with col2:
            st.write(alert['type'])
        with col3:
            status_color = "🟢" if alert['status'] == "活躍" else "🔴"
            st.write(f"{status_color} {alert['status']}")
        with col4:
            st.write(f"觸發: {alert['triggered']} 次")


def display_correlation_analyzer():
    """
    顯示關聯分析器
    """
    st.subheader("🔗 關聯分析器")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # KOL 選擇器
        kols_data = get_mock_kols_data()
        kol_options = {f"{kol['name']} (@{kol['username']})": kol['id'] for kol in kols_data["kols"]}
        selected_kol = st.selectbox("選擇 KOL", list(kol_options.keys()))
        kol_id = kol_options[selected_kol] if selected_kol else None
    
    with col2:
        stock_symbol = st.text_input("股票代碼", value="AAPL")
    
    time_period = st.slider("分析時間範圍（天）", min_value=7, max_value=365, value=30)
    
    if st.button("分析關聯"):
        if kol_id and stock_symbol:
            # 模擬關聯分析結果
            correlation_data = {
                "correlation_coefficient": 0.75,
                "sample_size": 150,
                "p_value": 0.001,
                "confidence_interval": [0.65, 0.85],
                "significance": "高度顯著"
            }
            
            st.success("關聯分析完成！")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("相關係數", f"{correlation_data['correlation_coefficient']:.3f}")
            with col2:
                st.metric("樣本數量", correlation_data['sample_size'])
            with col3:
                st.metric("P 值", f"{correlation_data['p_value']:.3f}")
            
            # 顯示詳細結果
            st.write("**詳細分析結果:**")
            st.write(f"- 置信區間: {correlation_data['confidence_interval'][0]:.3f} 到 {correlation_data['confidence_interval'][1]:.3f}")
            st.write(f"- 顯著性: {correlation_data['significance']}")
            
            # 顯示相關性解釋
            if correlation_data['correlation_coefficient'] > 0.7:
                st.info("💡 強正相關：該 KOL 的情緒與股票價格有強烈的正相關關係")
            elif correlation_data['correlation_coefficient'] > 0.3:
                st.info("💡 中等正相關：該 KOL 的情緒與股票價格有中等程度的正相關關係")
            elif correlation_data['correlation_coefficient'] < -0.7:
                st.info("💡 強負相關：該 KOL 的情緒與股票價格有強烈的負相關關係")
            else:
                st.info("💡 弱相關：該 KOL 的情緒與股票價格相關性較弱")
        else:
            st.warning("請填寫完整的分析參數")


def display_ai_chat():
    """
    顯示 AI 聊天區域
    """
    st.subheader("🤖 AI 智能助手")
    
    # 初始化聊天歷史
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    
    # 顯示聊天歷史
    chat_container = st.container()
    with chat_container:
        for message in st.session_state.chat_history:
            if message["role"] == "user":
                with st.chat_message("user"):
                    st.write(message["content"])
            else:
                with st.chat_message("assistant"):
                    st.write(message["content"])
    
    # 聊天輸入
    if prompt := st.chat_input("問我任何關於市場、KOL、股票或情緒分析的問題..."):
        # 添加用戶消息到歷史
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        
        # 模擬 AI 回應
        ai_response = generate_ai_response(prompt)
        st.session_state.chat_history.append({"role": "assistant", "content": ai_response})
        
        # 重新運行以顯示新消息
        st.rerun()


def generate_ai_response(prompt: str) -> str:
    """
    生成 AI 回應
    """
    prompt_lower = prompt.lower()
    
    # 根據問題類型生成回應
    if any(word in prompt_lower for word in ["tesla", "tsla", "特斯拉"]):
        return """📈 **Tesla (TSLA) 分析報告**

根據最新的情緒分析數據：

**市場情緒**: 正面 (0.75)
**KOL 提及**: Elon Musk 最近發布了關於 Tesla 的正面推文
**技術分析**: 股價在 $150-160 區間震盪
**建議**: 短期內可能會有小幅上漲，建議關注 Elon Musk 的社交媒體動態

*數據來源: Sentient Trader AI 分析引擎*"""
    
    elif any(word in prompt_lower for word in ["elon", "musk", "馬斯克"]):
        return """👤 **Elon Musk 影響力分析**

**影響力評分**: 0.95/1.0 (極高)
**粉絲數**: 1.5億
**最近活動**: 
- 發布 Tesla 相關推文
- SpaceX 進展更新
- 市場情緒影響: 強烈正面

**建議**: 密切關注其推文，對 Tesla 和相關股票有重大影響。"""
    
    elif any(word in prompt_lower for word in ["情緒", "sentiment", "市場情緒"]):
        return """📊 **市場情緒分析**

**當前貪婪恐懼指數**: 72 (貪婪)
**平均情緒分數**: 0.65
**市場狀態**: 投資者情緒偏向樂觀

**趨勢分析**:
- 短期: 情緒穩定上升
- 中期: 需關注可能的調整
- 長期: 整體樂觀

**建議**: 在貪婪區域保持謹慎，考慮分散投資。"""
    
    elif any(word in prompt_lower for word in ["kol", "影響者", "influencer"]):
        return """👥 **KOL 監控報告**

**活躍 KOL 數量**: 4
**主要影響者**:
1. Elon Musk (@elonmusk) - 影響力: 0.95
2. Cathie Wood (@CathieDWood) - 影響力: 0.85
3. Chamath Palihapitiya (@chamath) - 影響力: 0.78
4. Mark Cuban (@mcuban) - 影響力: 0.72

**今日提及熱門股票**: TSLA, ARKK, SPCE
**建議**: 關注這些 KOL 的最新動態，可能影響相關股票走勢。"""
    
    elif any(word in prompt_lower for word in ["警報", "alert", "提醒"]):
        return """🚨 **智能警報系統**

**活躍警報**: 3個
1. Tesla 高情緒警報 - 已觸發 3次
2. Elon Musk 提及警報 - 已觸發 5次  
3. AAPL 價格波動警報 - 非活躍

**最新警報**: Elon Musk 發布 Tesla 相關推文，觸發高情緒警報
**建議**: 檢查警報詳情，考慮相應的投資策略調整。"""
    
    elif any(word in prompt_lower for word in ["rag", "檢索", "retrieval"]):
        return """🔍 **RAG (檢索增強生成) 系統**

**功能**: 智能檢索相關數據並生成分析報告
**數據源**: 
- KOL 社交媒體貼文
- 新聞文章
- 市場情緒數據
- 股票價格數據

**使用方式**: 詢問特定股票或事件，系統會自動檢索相關信息並生成分析報告。

**示例問題**:
- "為什麼 Tesla 今天上漲？"
- "Elon Musk 最近的推文對市場有什麼影響？"
- "分析 AAPL 的情緒趨勢" """
    
    elif any(word in prompt_lower for word in ["mcp", "model", "模型"]):
        return """🤖 **MCP (Model Context Protocol) 系統**

**功能**: 多模態 AI 模型協作
**支持的模型**:
- 情緒分析模型
- 文本生成模型  
- 圖像識別模型
- 預測模型

**應用場景**:
- 自動分析社交媒體內容
- 生成市場報告
- 預測股票走勢
- 識別市場異常

**系統狀態**: 所有模型運行正常，實時處理市場數據。"""
    
    elif any(word in prompt_lower for word in ["幫助", "help", "功能"]):
        return """🤖 **Sentient Trader AI 助手**

我可以幫助你分析：

📈 **股票分析**
- 詢問任何股票代碼 (如: "分析 TSLA")
- 獲取技術分析和情緒數據

👤 **KOL 監控**  
- 查詢影響者動態 (如: "Elon Musk 最近怎麼樣？")
- 分析 KOL 對市場的影響

📊 **市場情緒**
- 獲取貪婪恐懼指數
- 分析市場情緒趨勢

🚨 **警報系統**
- 查看活躍警報
- 獲取市場異常提醒

🔍 **RAG 檢索**
- 智能檢索相關數據
- 生成分析報告

🤖 **MCP 模型**
- 多模態 AI 協作
- 自動化分析流程

**示例問題**:
- "Tesla 今天怎麼樣？"
- "市場情緒如何？"
- "有什麼警報嗎？"
- "分析 AAPL 的情緒" """
    
    else:
        return """🤖 **AI 助手回應**

我理解你的問題，但需要更多具體信息來提供準確的分析。

**建議問題類型**:
- 股票分析: "分析 TSLA"
- KOL 查詢: "Elon Musk 怎麼樣？"  
- 市場情緒: "市場情緒如何？"
- 警報查詢: "有什麼警報？"
- 功能說明: "你能做什麼？"

請提供更具體的問題，我會為你提供詳細的分析報告！ 📊"""


def main():
    """
    主函數
    """
    display_header()
    
    # 側邊欄
    with st.sidebar:
        st.title("📊 導航")
        page = st.selectbox(
            "選擇頁面",
            ["儀表板", "KOL 監控", "情緒分析", "警報系統", "關聯分析", "AI 聊天"]
        )
        
        st.markdown("---")
        st.markdown("### 快速操作")
        if st.button("刷新數據"):
            st.rerun()
        
        st.markdown("---")
        st.markdown("### 系統狀態")
        
        # 檢查後端連接
        try:
            health_check = requests.get("http://localhost:8000/health", timeout=2)
            if health_check.status_code == 200:
                st.success("✅ API 連接正常")
            else:
                st.warning("⚠️ API 連接異常")
        except:
            st.error("❌ API 連接失敗")
        
        st.markdown("---")
        st.markdown("### 平台資訊")
        st.write("**版本:** 1.0.0")
        st.write("**環境:** 開發模式")
        st.write("**最後更新:** 剛剛")
    
    # 主要內容區域
    if page == "儀表板":
        display_metrics()
        st.markdown("---")
        
        col1, col2 = st.columns(2)
        with col1:
            display_kol_monitoring()
        with col2:
            display_sentiment_timeline()
    
    elif page == "KOL 監控":
        display_kol_monitoring()
    
    elif page == "情緒分析":
        display_sentiment_timeline()
    
    elif page == "警報系統":
        display_alerts()
    
    elif page == "關聯分析":
        display_correlation_analyzer()
    
    elif page == "AI 聊天":
        display_ai_chat()


if __name__ == "__main__":
    main() 