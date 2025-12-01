import os
import subprocess
import time
import sys
from google.colab import output
# 1. 輸入 Ngrok Token
# ------------------------------------------------------------------
NGROK_TOKEN = input("請輸入您的 Ngrok Authtoken: ")
if not NGROK_TOKEN:
    print("錯誤：必須輸入 Ngrok Token 才能進行外部連線。")
    sys.exit()
print("\n正在安裝依賴環境 (這可能需要幾分鐘)...")
# 2. 安裝 PyNgrok, Ollama 和 OpenWebUI
# ------------------------------------------------------------------
# 安裝 Ngrok Python 套件
!pip install pyngrok > /dev/null 2>&1
from pyngrok import ngrok, conf
# 安裝 OpenWebUI
!pip install open-webui > /dev/null 2>&1
# 安裝 Ollama (後端模型服務)
if not os.path.exists("/usr/local/bin/ollama"):
    !curl -fsSL https://ollama.com/install.sh | sh > /dev/null 2>&1
print("環境安裝完成。")
# 3. 設定與啟動 Ngrok (指向 Port 30000)
# ------------------------------------------------------------------
# 設定 Token
conf.get_default().auth_token = NGROK_TOKEN
# 關閉舊的通道
ngrok.kill()
# 【修改點 2】開啟 HTTP 通道指 OpenWebUI 的 Port 30000
public_url = ngrok.connect(30000).public_url
print("----------------------------------------------------------------")
print(f"您的 OpenWebUI 網址: {public_url}")
print("----------------------------------------------------------------")
# 4. 啟動後端服務 (Ollama)
# ------------------------------------------------------------------
print("正在啟動 Ollama 後端...")
# 在背景執行 Ollama serve
subprocess.Popen(["ollama", "serve"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
# 等待幾秒確保 Ollama 啟動
time.sleep(5)
# 【修改點 3】下載 Qwen VL 模型
# 目前 Ollama 上對應 2B 視覺模型的標籤通常是 qwen3-vl:2b
print("正在下載模型 (qwen3-vl:2b)...")
!ollama pull qwen3-vl:2b
# 5. 啟動 OpenWebUI (在 Port 30000)
# ------------------------------------------------------------------
print("\n正在啟動 OpenWebUI 伺服器 (Port 30000)...")
# 設定 Ollama Base URL
os.environ['OLLAMA_BASE_URL'] = 'http://127.0.0.1:11434'
# 啟動服務 設定 OpenWebUI 運行的 Port 為 30000
!open-webui serve --host 0.0.0.0 --port 30000