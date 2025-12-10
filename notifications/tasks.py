from celery import shared_task
from notifications.services.dispacher import NotificationDispatcher


@shared_task(bind=True, max_retries=3, default_retry_delay=10)
def dispatch_notification_task(self, notification_id: int):
    dispatcher = NotificationDispatcher()
    try:
        dispatcher.dispatch(notification_id)
    except Exception as exc:
        raise self.retry(exc=exc)