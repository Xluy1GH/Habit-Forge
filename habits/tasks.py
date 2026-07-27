from celery import shared_task

from django.shortcuts import render
import requests

@shared_task
def send_telegram_message():
    "Sends a message on Telegram and show status code and text of post"
    
    token = "8960963061:AAGfVTatJOld3KN747avADKvF3Kg2NjHFGc"
    chat_id = "5934202258"
    text = "Пора бы выполнить привычку!"
    
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {"chat_id": chat_id, "text": text}

    response = requests.post(url, data=payload)