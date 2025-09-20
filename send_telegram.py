import os, requests

def send_telegram(token: str, chat_id: str, text: str):
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    resp = requests.get(url, params={"chat_id": chat_id, "text": text})
    try:
        resp.raise_for_status()
    except Exception as e:
        print("Telegram error:", e)

if __name__ == "__main__":
    token = os.getenv("TELEGRAM_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    if token and chat_id:
        send_telegram(token, chat_id, "Test PPB GitHub Actions Runner ✓")