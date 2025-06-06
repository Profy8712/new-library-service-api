import pytest
from unittest.mock import patch
from notifications.services import TelegramNotificationService
from notifications.tasks import send_telegram_notification_task

@pytest.mark.django_db
@patch("notifications.services.requests.post")
def test_service_send_message(mock_post):
    mock_post.return_value.status_code = 200
    service = TelegramNotificationService()
    result = service.send_message("Hello!")
    assert result
    mock_post.assert_called_once()


@patch("notifications.services.TelegramNotificationService.send_message")
def test_celery_task_triggers_service(mock_send):
    mock_send.return_value = True
    send_telegram_notification_task("Test message")
    mock_send.assert_called_once_with("Test message")
