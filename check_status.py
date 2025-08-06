#!/usr/bin/env python3
"""
Sentient Trader - 專案狀態檢查腳本
檢查所有組件是否正常運行
"""

import requests
import subprocess
import sys
import time
from datetime import datetime
import json

# 配置
API_BASE_URL = "http://localhost:8000"
FRONTEND_URL = "http://localhost:8501"
POSTGRES_HOST = "localhost"
POSTGRES_PORT = 5432
REDIS_HOST = "localhost"
REDIS_PORT = 6379


def check_api_health():
    """檢查 API 健康狀態"""
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=5)
        if response.status_code == 200:
            return True, "API 服務正常"
        else:
            return False, f"API 服務異常 (狀態碼: {response.status_code})"
    except requests.exceptions.RequestException as e:
        return False, f"API 服務無法連接: {str(e)}"


def check_frontend_health():
    """檢查前端健康狀態"""
    try:
        response = requests.get(f"{FRONTEND_URL}/_stcore/health", timeout=5)
        if response.status_code == 200:
            return True, "前端服務正常"
        else:
            return False, f"前端服務異常 (狀態碼: {response.status_code})"
    except requests.exceptions.RequestException as e:
        return False, f"前端服務無法連接: {str(e)}"


def check_database_connection():
    """檢查資料庫連接"""
    try:
        import psycopg2
        conn = psycopg2.connect(
            host=POSTGRES_HOST,
            port=POSTGRES_PORT,
            database="sentient_trader",
            user="sentient_user",
            password="sentient_password"
        )
        conn.close()
        return True, "PostgreSQL 連接正常"
    except Exception as e:
        return False, f"PostgreSQL 連接失敗: {str(e)}"


def check_redis_connection():
    """檢查 Redis 連接"""
    try:
        import redis
        r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)
        r.ping()
        return True, "Redis 連接正常"
    except Exception as e:
        return False, f"Redis 連接失敗: {str(e)}"


def check_docker_services():
    """檢查 Docker 服務狀態"""
    try:
        result = subprocess.run(
            ["docker-compose", "ps"],
            capture_output=True,
            text=True,
            timeout=10
        )
        if result.returncode == 0:
            return True, "Docker 服務正常"
        else:
            return False, f"Docker 服務異常: {result.stderr}"
    except Exception as e:
        return False, f"Docker 檢查失敗: {str(e)}"


def check_environment():
    """檢查環境變數"""
    try:
        import os
        from dotenv import load_dotenv
        
        load_dotenv()
        
        required_vars = [
            "DATABASE_URL",
            "REDIS_URL",
            "SECRET_KEY"
        ]
        
        missing_vars = []
        for var in required_vars:
            if not os.getenv(var):
                missing_vars.append(var)
        
        if missing_vars:
            return False, f"缺少環境變數: {', '.join(missing_vars)}"
        else:
            return True, "環境變數配置正常"
    except Exception as e:
        return False, f"環境檢查失敗: {str(e)}"


def check_dependencies():
    """檢查 Python 依賴"""
    try:
        import fastapi
        import streamlit
        import transformers
        import torch
        import pandas
        import plotly
        
        return True, "Python 依賴正常"
    except ImportError as e:
        return False, f"缺少 Python 依賴: {str(e)}"


def main():
    """主函數"""
    print("🔍 Sentient Trader 專案狀態檢查")
    print("=" * 50)
    print(f"檢查時間: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    checks = [
        ("環境變數", check_environment),
        ("Python 依賴", check_dependencies),
        ("Docker 服務", check_docker_services),
        ("PostgreSQL", check_database_connection),
        ("Redis", check_redis_connection),
        ("API 服務", check_api_health),
        ("前端服務", check_frontend_health),
    ]
    
    all_passed = True
    results = []
    
    for name, check_func in checks:
        print(f"檢查 {name}...", end=" ")
        try:
            passed, message = check_func()
            if passed:
                print("✅")
                results.append((name, True, message))
            else:
                print("❌")
                results.append((name, False, message))
                all_passed = False
        except Exception as e:
            print("❌")
            results.append((name, False, f"檢查失敗: {str(e)}"))
            all_passed = False
    
    print()
    print("📊 檢查結果摘要:")
    print("-" * 50)
    
    for name, passed, message in results:
        status = "✅" if passed else "❌"
        print(f"{status} {name}: {message}")
    
    print()
    if all_passed:
        print("🎉 所有檢查通過！專案狀態正常。")
        print()
        print("📋 服務資訊:")
        print(f"   • 前端: {FRONTEND_URL}")
        print(f"   • 後端 API: {API_BASE_URL}")
        print(f"   • API 文檔: {API_BASE_URL}/docs")
        print(f"   • 資料庫: {POSTGRES_HOST}:{POSTGRES_PORT}")
        print(f"   • Redis: {REDIS_HOST}:{REDIS_PORT}")
    else:
        print("⚠️ 部分檢查失敗，請檢查上述問題。")
        print()
        print("🔧 故障排除建議:")
        print("   1. 確保所有服務已啟動")
        print("   2. 檢查環境變數配置")
        print("   3. 確認資料庫連接")
        print("   4. 檢查防火牆設置")
    
    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main()) 