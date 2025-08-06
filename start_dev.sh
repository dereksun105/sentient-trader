#!/bin/bash

# Sentient Trader 開發環境啟動腳本

echo "🚀 啟動 Sentient Trader 開發環境..."

# 檢查是否安裝了必要的工具
check_requirements() {
    echo "📋 檢查系統要求..."
    
    if ! command -v python3 &> /dev/null; then
        echo "❌ Python 3 未安裝"
        exit 1
    fi
    
    if ! command -v pip3 &> /dev/null; then
        echo "❌ pip3 未安裝"
        exit 1
    fi
    
    echo "✅ 系統要求檢查通過"
}

# 設置虛擬環境
setup_venv() {
    echo "🐍 設置 Python 虛擬環境..."
    
    if [ ! -d "venv" ]; then
        python3 -m venv venv
        echo "✅ 虛擬環境創建完成"
    else
        echo "✅ 虛擬環境已存在"
    fi
    
    source venv/bin/activate
    echo "✅ 虛擬環境已激活"
}

# 安裝依賴
install_dependencies() {
    echo "📦 安裝 Python 依賴..."
    pip install -r requirements.txt
    echo "✅ 依賴安裝完成"
}

# 設置環境變數
setup_env() {
    echo "🔧 設置環境變數..."
    
    if [ ! -f ".env" ]; then
        cp env.example .env
        echo "✅ 環境變數文件已創建，請編輯 .env 文件填入必要的 API 金鑰"
    else
        echo "✅ 環境變數文件已存在"
    fi
}

# 啟動資料庫服務
start_database() {
    echo "🗄️ 啟動資料庫服務..."
    
    # 檢查 Docker 是否可用
    if command -v docker &> /dev/null && command -v docker-compose &> /dev/null; then
        echo "🐳 使用 Docker 啟動資料庫..."
        docker-compose up -d postgres redis
        echo "✅ 資料庫服務已啟動"
    else
        echo "⚠️ Docker 不可用，請手動啟動 PostgreSQL 和 Redis"
        echo "PostgreSQL 應該運行在 localhost:5432"
        echo "Redis 應該運行在 localhost:6379"
    fi
}

# 啟動後端 API
start_backend() {
    echo "🔧 啟動後端 API..."
    
    # 在背景啟動 API 服務
    python -m uvicorn app.main:app --reload --port 8000 &
    API_PID=$!
    echo "✅ 後端 API 已啟動 (PID: $API_PID)"
    
    # 等待 API 啟動
    echo "⏳ 等待 API 服務啟動..."
    sleep 5
    
    # 檢查 API 是否正常運行
    if curl -f http://localhost:8000/health &> /dev/null; then
        echo "✅ API 服務運行正常"
    else
        echo "❌ API 服務啟動失敗"
        exit 1
    fi
}

# 啟動前端
start_frontend() {
    echo "🎨 啟動前端..."
    
    # 在背景啟動 Streamlit
    streamlit run frontend/main.py --server.port 8501 &
    FRONTEND_PID=$!
    echo "✅ 前端已啟動 (PID: $FRONTEND_PID)"
    
    # 等待前端啟動
    echo "⏳ 等待前端服務啟動..."
    sleep 3
}

# 顯示服務資訊
show_services() {
    echo ""
    echo "🎉 Sentient Trader 開發環境啟動完成！"
    echo ""
    echo "📊 服務資訊："
    echo "   • 前端: http://localhost:8501"
    echo "   • 後端 API: http://localhost:8000"
    echo "   • API 文檔: http://localhost:8000/docs"
    echo "   • 資料庫: localhost:5432"
    echo "   • Redis: localhost:6379"
    echo ""
    echo "🛑 停止服務："
    echo "   • 按 Ctrl+C 停止所有服務"
    echo "   • 或運行: ./stop_dev.sh"
    echo ""
    echo "📝 日誌："
    echo "   • API 日誌會顯示在終端"
    echo "   • 前端日誌會顯示在瀏覽器"
    echo ""
}

# 清理函數
cleanup() {
    echo ""
    echo "🛑 正在停止服務..."
    
    if [ ! -z "$API_PID" ]; then
        kill $API_PID 2>/dev/null
        echo "✅ 後端 API 已停止"
    fi
    
    if [ ! -z "$FRONTEND_PID" ]; then
        kill $FRONTEND_PID 2>/dev/null
        echo "✅ 前端已停止"
    fi
    
    echo "✅ 所有服務已停止"
    exit 0
}

# 設置信號處理
trap cleanup SIGINT SIGTERM

# 主函數
main() {
    check_requirements
    setup_venv
    install_dependencies
    setup_env
    start_database
    start_backend
    start_frontend
    show_services
    
    # 保持腳本運行
    echo "🔄 服務運行中... 按 Ctrl+C 停止"
    wait
}

# 運行主函數
main 