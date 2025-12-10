from django.urls import path
from .views import NotificationTriggerView

urlpatterns = [
    path("trigger/", NotificationTriggerView.as_view(), name="notification-trigger"),
]