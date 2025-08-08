import os
import requests
from dotenv import load_dotenv

# 读取 .env
load_dotenv()

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def _ensure():
    if not BOT_TOKEN or not CHAT_ID:
        raise ValueError("Telegram Bot Token 或 Chat ID 未配置（检查 .env）")

def send_message(text: str):
    _ensure()
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": text}
    return requests.post(url, data=data, timeout=15).json()

def send_file(file_path: str):
    _ensure()
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendDocument"
    with open(file_path, "rb") as f:
        files = {"document": f}
        data = {"chat_id": CHAT_ID}
        return requests.post(url, files=files, data=data, timeout=60).json()
