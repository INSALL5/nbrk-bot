import pandas as pd
import requests
from datetime import datetime
from dotenv import load_dotenv
import os
import logging

# Удаление log.txt, если он слишком большой
if os.path.exists("log.txt") and os.path.getsize("log.txt") > 1_000_000:
    os.remove("log.txt")

# Настройка логов
logging.basicConfig(
    filename="log.txt",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

load_dotenv()
TOKEN = os.getenv("TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

# Уникальное имя файла по дате и времени
now = datetime.now()
timestamp = now.strftime("%d-%m-%Y_%H-%M")
file_name = f"курсы_валют_НБРК_{timestamp}.xlsx"

url = f"https://nationalbank.kz/rss/get_rates.cfm?fdate={now.strftime('%d.%m.%Y')}"

try:
    response = requests.get(url)
    response.raise_for_status()
    df = pd.read_xml(response.content)

    # Удалим старый файл если вдруг совпало
    if os.path.exists(file_name):
        os.remove(file_name)

    df.to_excel(file_name, index=False)

    logging.info(f"✅ Файл {file_name} сохранён.")
    print(f"✅ Файл {file_name} сохранён.")

    # Уведомление в Telegram
    msg = f"📥 Курсы валют на {now.strftime('%d.%m.%Y %H:%M')} загружены. Отправка файла..."
    send_msg = requests.post(
        f"https://api.telegram.org/bot{TOKEN}/sendMessage",
        data={"chat_id": CHAT_ID, "text": msg}
    )
    print("Ответ sendMessage:", send_msg.status_code, send_msg.text)
    logging.info(f"sendMessage: {send_msg.status_code} - {send_msg.text}")

    # Отправка файла
    with open(file_name, "rb") as file:
        send_doc = requests.post(
            f"https://api.telegram.org/bot{TOKEN}/sendDocument",
            data={"chat_id": CHAT_ID},
            files={"document": file}
        )

    print("Ответ sendDocument:", send_doc.status_code, send_doc.text)
    logging.info(f"sendDocument: {send_doc.status_code} - {send_doc.text}")

except Exception as e:
    logging.error(f"‼️ Ошибка: {e}")
    print("‼️ Ошибка в nbrk_rates.py:", e)
