#!/bin/bash

# Sentient Trader 開發環境停止腳本

echo "🛑 停止 Sentient Trader 開發環境..."

# 停止前端服務
echo "🎨 停止前端服務..."
pkill -f "streamlit run frontend/main.py" 2>/dev/null
echo "✅ 前端服務已停止"

# 停止後端 API 服務
echo "🔧 停止後端 API 服務..."
pkill -f "uvicorn app.main:app" 2>/dev/null
echo "✅ 後端 API 服務已停止"

# 停止資料庫服務（如果使用 Docker）
if command -v docker &> /dev/null && command -v docker-compose &> /dev/null; then
    echo "🐳 停止資料庫服務..."
    docker-compose down 2>/dev/null
    echo "✅ 資料庫服務已停止"
fi

echo ""
echo "✅ 所有服務已停止"
echo ""
echo "📝 提示："
echo "   • 要重新啟動服務，運行: ./start_dev.sh"
echo "   • 要清理 Docker 容器，運行: docker-compose down -v"
echo "   • 要清理虛擬環境，刪除 venv/ 目錄" 