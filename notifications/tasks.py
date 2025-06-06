from celery import shared_task
from .services import TelegramNotificationService


@shared_task
def send_telegram_notification_task(message: str) -> None:
    service = TelegramNotificationService()
    service.send_message(message)
