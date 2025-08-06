"""
Sentient Trader - AI-Driven Financial Intelligence Platform
Deployment version for Streamlit Cloud
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
import time

# 設置頁面配置
st.set_page_config(
    page_title="Sentient Trader - AI 智能交易平台",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 自定義 CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #FF6B6B;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin: 0.5rem 0;
    }
    .metric-value {
        font-size: 2rem;
        font-weight: bold;
    }
    .metric-label {
        font-size: 0.9rem;
        opacity: 0.9;
    }
    .sidebar .sidebar-content {
        background-color: #f0f2f6;
    }
    @media (prefers-color-scheme: dark) {
        .metric-card {
            background: linear-gradient(135deg, #2c3e50 0%, #34495e 100%);
        }
        .sidebar .sidebar-content {
            background-color: #262730;
        }
        .stSelectbox, .stTextInput, .stSlider, .stButton {
            background-color: #262730 !important;
            color: #ffffff !important;
        }
        .stChatMessage {
            background-color: #262730 !important;
            color: #ffffff !important;
        }
        .streamlit-expanderHeader {
            background-color: #262730 !important;
            color: #ffffff !important;
        }
        .css-1d391kg {
            background-color: #262730 !important;
        }
        .main .block-container {
            background-color: #0e1117 !important;
        }
    }
</style>
""", unsafe_allow_html=True)

# 模擬數據函數
def get_mock_kols_data():
    """獲取模擬 KOL 數據"""
    return {
        "kols": [
            {
                "id": 1,
                "name": "Elon Musk",
                "username": "elonmusk",
                "platform": "Twitter",
                "followers": 150000000,
                "influence_score": 0.95,
                "last_post": "2024-01-15T10:30:00Z",
                "sentiment": 0.3
            },
            {
                "id": 2,
                "name": "Cathie Wood",
                "username": "CathieDWood",
                "platform": "Twitter",
                "followers": 2500000,
                "influence_score": 0.85,
                "last_post": "2024-01-15T09:15:00Z",
                "sentiment": -0.2
            },
            {
                "id": 3,
                "name": "Chamath Palihapitiya",
                "username": "chamath",
                "platform": "Twitter",
                "followers": 1200000,
                "influence_score": 0.75,
                "last_post": "2024-01-15T08:45:00Z",
                "sentiment": 0.1
            },
            {
                "id": 4,
                "name": "Mark Cuban",
                "username": "mcuban",
                "platform": "Twitter",
                "followers": 8500000,
                "influence_score": 0.80,
                "last_post": "2024-01-15T07:30:00Z",
                "sentiment": 0.4
            },
            {
                "id": 5,
                "name": "Chamath Palihapitiya",
                "username": "chamath",
                "platform": "Twitter",
                "followers": 1200000,
                "influence_score": 0.75,
                "last_post": "2024-01-15T06:20:00Z",
                "sentiment": -0.1
            }
        ]
    }

def get_mock_posts_data():
    """獲取模擬社交媒體帖子數據"""
    return {
        "posts": [
            {
                "id": 1,
                "kol_id": 1,
                "kol_name": "Elon Musk",
                "content": "Tesla's AI capabilities are advancing rapidly. The future of autonomous driving is here! 🚗🤖",
                "platform": "Twitter",
                "timestamp": "2024-01-15T10:30:00Z",
                "sentiment": 0.8,
                "likes": 45000,
                "retweets": 12000,
                "mentions": ["TSLA", "AI"]
            },
            {
                "id": 2,
                "kol_id": 2,
                "kol_name": "Cathie Wood",
                "content": "Market volatility creates opportunities for long-term investors. Stay focused on innovation. 📈",
                "platform": "Twitter",
                "timestamp": "2024-01-15T09:15:00Z",
                "sentiment": 0.2,
                "likes": 8500,
                "retweets": 2100,
                "mentions": ["ARKK", "innovation"]
            },
            {
                "id": 3,
                "kol_id": 3,
                "kol_name": "Chamath Palihapitiya",
                "content": "The Fed's policy decisions are creating uncertainty in the market. Investors need to be patient.",
                "platform": "Twitter",
                "timestamp": "2024-01-15T08:45:00Z",
                "sentiment": -0.3,
                "likes": 12000,
                "retweets": 3500,
                "mentions": ["FED", "market"]
            },
            {
                "id": 4,
                "kol_id": 4,
                "kol_name": "Mark Cuban",
                "content": "Crypto regulation is necessary for mainstream adoption. Clear rules benefit everyone. 🏛️",
                "platform": "Twitter",
                "timestamp": "2024-01-15T07:30:00Z",
                "sentiment": 0.5,
                "likes": 18000,
                "retweets": 4200,
                "mentions": ["crypto", "regulation"]
            },
            {
                "id": 5,
                "kol_id": 5,
                "kol_name": "Chamath Palihapitiya",
                "content": "SPAC market is showing signs of recovery. Quality companies will always find capital.",
                "platform": "Twitter",
                "timestamp": "2024-01-15T06:20:00Z",
                "sentiment": 0.1,
                "likes": 9500,
                "retweets": 1800,
                "mentions": ["SPAC", "capital"]
            }
        ]
    }

def get_mock_dashboard_data():
    """獲取模擬儀表板數據"""
    return {
        "market_sentiment": 0.65,
        "greed_fear_index": 72,
        "total_kols": 156,
        "active_alerts": 8,
        "correlation_score": 0.78
    }

def display_header():
    """顯示頁面標題"""
    st.markdown('<h1 class="main-header">📈 Sentient Trader</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; font-size: 1.2rem; color: #666;">AI 驅動的智能交易平台</p>', unsafe_allow_html=True)

def display_metrics():
    """顯示關鍵指標"""
    st.subheader("📊 市場指標")
    
    dashboard_data = get_mock_dashboard_data()
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        sentiment_color = "#26a69a" if dashboard_data["market_sentiment"] > 0 else "#ef5350"
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{dashboard_data["market_sentiment"]:.2f}</div>
            <div class="metric-label">市場情緒指數</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        # 貪婪恐懼指數
        greed_fear = dashboard_data["greed_fear_index"]
        if greed_fear >= 75:
            emoji = "😱"
            status = "極度貪婪"
        elif greed_fear >= 60:
            emoji = "😨"
            status = "貪婪"
        elif greed_fear >= 40:
            emoji = "😐"
            status = "中性"
        elif greed_fear >= 25:
            emoji = "😰"
            status = "恐懼"
        else:
            emoji = "😱"
            status = "極度恐懼"
        
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{emoji} {greed_fear}</div>
            <div class="metric-label">貪婪恐懼指數 - {status}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{dashboard_data["total_kols"]}</div>
            <div class="metric-label">監控 KOL</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{dashboard_data["active_alerts"]}</div>
            <div class="metric-label">活躍警報</div>
        </div>
        """, unsafe_allow_html=True)

def display_kol_monitoring():
    """顯示 KOL 監控牆"""
    st.subheader("👥 KOL 監控牆")
    
    kols_data = get_mock_kols_data()
    posts_data = get_mock_posts_data()
    
    # 顯示 KOL 列表
    st.markdown("### 活躍 KOL")
    for kol in kols_data["kols"][:5]:
        col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
        
        with col1:
            st.write(f"**{kol['name']}** (@{kol['username']})")
        
        with col2:
            influence_color = "#26a69a" if kol['influence_score'] > 0.8 else "#ff9800" if kol['influence_score'] > 0.6 else "#f44336"
            st.write(f"影響力: {kol['influence_score']:.2f}")
        
        with col3:
            sentiment_emoji = "📈" if kol['sentiment'] > 0 else "📉" if kol['sentiment'] < 0 else "➡️"
            st.write(f"情緒: {sentiment_emoji} {kol['sentiment']:.2f}")
        
        with col4:
            st.write(f"粉絲: {kol['followers']:,}")
    
    # 顯示最新帖子
    st.markdown("### 最新動態")
    for post in posts_data["posts"][:3]:
        with st.expander(f"{post['kol_name']} - {post['timestamp'][:10]}"):
            st.write(f"**內容:** {post['content']}")
            col1, col2, col3 = st.columns(3)
            with col1:
                sentiment_emoji = "📈" if post['sentiment'] > 0 else "📉" if post['sentiment'] < 0 else "➡️"
                st.write(f"情緒: {sentiment_emoji} {post['sentiment']:.2f}")
            with col2:
                st.write(f"👍 {post['likes']:,}")
            with col3:
                st.write(f"🔄 {post['retweets']:,}")

def display_sentiment_timeline():
    """顯示情緒與價格時間軸"""
    st.subheader("📈 情緒與價格時間軸")
    
    # 時間框架選擇
    timeframe = st.selectbox("選擇時間框架", ["1D", "1W", "1M", "3M", "6M", "1Y"])
    
    # 生成模擬數據
    if timeframe == "1D":
        dates = pd.date_range(start='2024-01-15', periods=24, freq='H')
        base_price = 150.0
    elif timeframe == "1W":
        dates = pd.date_range(start='2024-01-09', periods=7, freq='D')
        base_price = 150.0
    elif timeframe == "1M":
        dates = pd.date_range(start='2023-12-15', periods=30, freq='D')
        base_price = 145.0
    elif timeframe == "3M":
        dates = pd.date_range(start='2023-10-15', periods=90, freq='D')
        base_price = 140.0
    elif timeframe == "6M":
        dates = pd.date_range(start='2023-07-15', periods=180, freq='D')
        base_price = 130.0
    else:  # 1Y
        dates = pd.date_range(start='2023-01-15', periods=365, freq='D')
        base_price = 100.0
    
    # 生成股價數據
    np.random.seed(42)
    price_changes = np.random.normal(0, 0.02, len(dates))
    prices = [base_price]
    for change in price_changes[1:]:
        prices.append(prices[-1] * (1 + change))
    
    # 生成情緒數據
    sentiment_data = np.random.normal(0, 0.3, len(dates))
    sentiment_data = np.clip(sentiment_data, -1, 1)
    
    # 創建蠟燭圖數據
    ohlc_data = []
    for i, (date, price) in enumerate(zip(dates, prices)):
        high = price * (1 + abs(np.random.normal(0, 0.01)))
        low = price * (1 - abs(np.random.normal(0, 0.01)))
        open_price = prices[i-1] if i > 0 else price
        close_price = price
        
        ohlc_data.append({
            'date': date,
            'open': open_price,
            'high': high,
            'low': low,
            'close': close_price
        })
    
    # 創建圖表
    fig = go.Figure()
    
    # 添加蠟燭圖
    fig.add_trace(go.Candlestick(
        x=[d['date'] for d in ohlc_data],
        open=[d['open'] for d in ohlc_data],
        high=[d['high'] for d in ohlc_data],
        low=[d['low'] for d in ohlc_data],
        close=[d['close'] for d in ohlc_data],
        name="股價",
        yaxis="y"
    ))
    
    # 添加情緒線
    fig.add_trace(go.Scatter(
        x=dates,
        y=sentiment_data,
        name="情緒分數",
        yaxis="y2",
        line=dict(color='#FF6B6B', width=2)
    ))
    
    # 更新佈局
    fig.update_layout(
        title=f"TSLA 股價蠟燭圖與情緒分析 ({timeframe})",
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
    
    st.plotly_chart(fig, use_container_width=True)
    
    # 顯示統計信息
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        latest_price = ohlc_data[-1]['close']
        price_change = latest_price - ohlc_data[0]['close']
        price_change_pct = (price_change / ohlc_data[0]['close']) * 100
        st.metric(
            "當前價格", 
            f"${latest_price:.2f}",
            f"{price_change:+.2f} ({price_change_pct:+.2f}%)"
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
    """顯示警報系統"""
    st.subheader("🚨 智能警報系統")
    
    with st.expander("創建新警報"):
        alert_name = st.text_input("警報名稱")
        alert_type = st.selectbox("警報類型", ["情緒閾值", "KOL 提及", "股票提及"])
        
        col1, col2 = st.columns(2)
        with col1:
            threshold = st.number_input("閾值", min_value=-1.0, max_value=1.0, value=0.5, step=0.1)
        with col2:
            st.button("創建警報")
    
    # 顯示活躍警報
    st.markdown("### 活躍警報")
    alerts = [
        {"name": "TSLA 高情緒警報", "type": "情緒閾值", "status": "活躍", "triggered": "2小時前"},
        {"name": "Elon Musk 提及警報", "type": "KOL 提及", "status": "活躍", "triggered": "1小時前"},
        {"name": "市場恐慌警報", "type": "情緒閾值", "status": "活躍", "triggered": "30分鐘前"}
    ]
    
    for alert in alerts:
        col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
        with col1:
            st.write(f"**{alert['name']}**")
        with col2:
            st.write(alert['type'])
        with col3:
            st.write(f"🟢 {alert['status']}")
        with col4:
            st.write(alert['triggered'])

def display_correlation_analyzer():
    """顯示相關性分析器"""
    st.subheader("🔍 相關性分析器")
    
    kols_data = get_mock_kols_data()
    
    col1, col2 = st.columns(2)
    
    with col1:
        kol_options = {f"{kol['name']} (@{kol['username']})": kol['id'] for kol in kols_data["kols"]}
        selected_kol = st.selectbox("選擇 KOL", list(kol_options.keys()))
    
    with col2:
        stock_symbol = st.text_input("股票代碼", value="TSLA")
    
    if st.button("分析相關性"):
        # 模擬相關性分析
        correlation = random.uniform(0.3, 0.9)
        
        st.markdown(f"### 分析結果")
        st.markdown(f"**{selected_kol}** 與 **{stock_symbol}** 的相關性:")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("相關性係數", f"{correlation:.3f}")
        
        with col2:
            strength = "強" if correlation > 0.7 else "中等" if correlation > 0.4 else "弱"
            st.metric("相關性強度", strength)
        
        with col3:
            direction = "正相關" if correlation > 0 else "負相關"
            st.metric("相關性方向", direction)
        
        # 相關性圖表
        dates = pd.date_range(start='2023-01-01', periods=100, freq='D')
        kol_sentiment = np.random.normal(0, 0.3, 100)
        stock_price = correlation * kol_sentiment + np.random.normal(0, 0.2, 100)
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=dates, y=kol_sentiment, name="KOL 情緒", line=dict(color='#FF6B6B')))
        fig.add_trace(go.Scatter(x=dates, y=stock_price, name="股票價格", line=dict(color='#4ECDC4')))
        
        fig.update_layout(
            title=f"{selected_kol} 情緒 vs {stock_symbol} 價格",
            xaxis_title="日期",
            yaxis_title="標準化分數",
            height=400,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#ffffff'),
            xaxis=dict(gridcolor='rgba(255,255,255,0.1)'),
            yaxis=dict(gridcolor='rgba(255,255,255,0.1)')
        )
        
        st.plotly_chart(fig, use_container_width=True)

def display_ai_chat():
    """顯示 AI 聊天功能"""
    st.subheader("🤖 AI 智能助手")
    
    # 初始化聊天歷史
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # 顯示聊天歷史
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # 聊天輸入
    if prompt := st.chat_input("問我任何關於市場的問題..."):
        # 添加用戶消息
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # 生成 AI 回應
        with st.chat_message("assistant"):
            response = generate_ai_response(prompt)
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})

def generate_ai_response(prompt: str) -> str:
    """生成 AI 回應"""
    prompt_lower = prompt.lower()
    
    if any(word in prompt_lower for word in ["tesla", "tsla", "特斯拉"]):
        return "🚗 **Tesla 分析**: 根據最新數據，Tesla 的股價受到以下因素影響：\n\n• **技術創新**: FSD 進展良好\n• **市場份額**: 電動車市場領導地位穩固\n• **財務表現**: Q4 交付量超出預期\n\n建議：短期看漲，但需關注宏觀經濟風險。"
    
    elif any(word in prompt_lower for word in ["market", "市場", "大盤"]):
        return "📊 **市場分析**: 當前市場狀況：\n\n• **情緒指標**: 貪婪恐懼指數為 72 (貪婪)\n• **技術面**: 主要指數處於關鍵支撐位\n• **資金流**: 機構資金持續流入\n\n預測：短期可能出現技術性反彈。"
    
    elif any(word in prompt_lower for word in ["sentiment", "情緒", "情感"]):
        return "😊 **情緒分析**: 市場情緒指標：\n\n• **整體情緒**: 0.65 (正面)\n• **KOL 情緒**: 平均 0.42\n• **新聞情緒**: 0.58\n\n趨勢：情緒正在改善，有利於風險資產。"
    
    elif any(word in prompt_lower for word in ["alert", "警報", "提醒"]):
        return "🚨 **警報系統**: 當前活躍警報：\n\n• TSLA 高情緒警報 (觸發 2小時前)\n• Elon Musk 提及警報 (觸發 1小時前)\n• 市場恐慌警報 (觸發 30分鐘前)\n\n建議：關注這些警報的後續發展。"
    
    elif any(word in prompt_lower for word in ["kol", "意見領袖", "網紅"]):
        return "👥 **KOL 監控**: 熱門 KOL 動態：\n\n• **Elon Musk**: 最新推文情緒 0.8 (非常正面)\n• **Cathie Wood**: 對創新股持樂觀態度\n• **Chamath**: 關注 SPAC 市場復甦\n\n影響：KOL 情緒整體偏向樂觀。"
    
    else:
        return "🤖 **AI 助手**: 我是 Sentient Trader 的 AI 助手，可以幫助你分析：\n\n• 📈 股票價格和情緒\n• 👥 KOL 動態和影響\n• 🚨 市場警報和機會\n• 📊 相關性分析\n\n請告訴我你想了解什麼？"

def main():
    """主函數"""
    display_header()
    
    # 側邊欄導航
    st.sidebar.title("🧭 導航")
    page = st.sidebar.selectbox(
        "選擇功能",
        ["📊 儀表板", "👥 KOL 監控", "📈 情緒時間軸", "🚨 警報系統", "🔍 相關性分析", "🤖 AI 助手"]
    )
    
    if page == "📊 儀表板":
        display_metrics()
        display_kol_monitoring()
    
    elif page == "👥 KOL 監控":
        display_kol_monitoring()
    
    elif page == "📈 情緒時間軸":
        display_sentiment_timeline()
    
    elif page == "🚨 警報系統":
        display_alerts()
    
    elif page == "🔍 相關性分析":
        display_correlation_analyzer()
    
    elif page == "🤖 AI 助手":
        display_ai_chat()
    
    # 頁腳
    st.markdown("---")
    st.markdown(
        '<p style="text-align: center; color: #666;">Sentient Trader - AI 驅動的智能交易平台 | 版本 1.0</p>',
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main() 