from django.urls import path
from . import views

urlpatterns = [
    path("test_message", views.send_telegram_message, name="test_message"),
]