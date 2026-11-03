from django.shortcuts import render
import requests
from django.views.generic import TemplateView

def send_telegram_message(request):
    "Sends a message on Telegram and show status code and text of post"
    
    token = "8960963061:AAGfVTatJOld3KN747avADKvF3Kg2NjHFGc"
    chat_id = "5934202258"
    text = "Test message"
    
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {"chat_id": chat_id, "text": text}

    response = requests.post(url, data=payload)

    return render(request, "test_message.html", context={"status_code": response.status_code, "text": response.text})

class HomeView(TemplateView):
    template_name = "home.html"