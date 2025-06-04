import requests
from django.conf import settings


class TelegramNotificationService:
    """Service for sending messages to Telegram via bot API."""

    def __init__(self):
        self.token = settings.TELEGRAM_TOKEN
        self.chat_id = settings.TELEGRAM_CHAT_ID

    def send_message(self, message: str) -> bool:
        url = f"https://api.telegram.org/bot{self.token}/sendMessage"
        data = {
            "chat_id": self.chat_id,
            "text": message,
            "parse_mode": "Markdown"
        }
        resp = requests.post(url, data=data, timeout=10)
        return resp.status_code == 200
