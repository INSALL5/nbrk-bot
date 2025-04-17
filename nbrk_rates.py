import pandas as pd
import requests
from datetime import datetime
from dotenv import load_dotenv
import os
import logging

if os.path.exists("log.txt") and os.path.getsize("log.txt") > 1_000_000:
    os.remove("log.txt")

logging.basicConfig(
    filename="log.txt",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

load_dotenv()
TOKEN = os.getenv("TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

today = datetime.today().strftime("%d.%m.%Y")
url = f"https://nationalbank.kz/rss/get_rates.cfm?fdate={today}"

try:
    response = requests.get(url)
    response.raise_for_status()
    df = pd.read_xml(response.content)

    file_name = f"курсы_валют_НБРК_{today.replace('.', '-')}.xlsx"
    df.to_excel(file_name, index=False)

    logging.info(f"Файл {file_name} успешно сохранён.")
    print(f"Файл сохранён: {file_name}")

    # Отправка текстового уведомления
    msg = f"📥 Курсы валют на {today} загружены. Отправка файла..."
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
    print("‼️ Ошибка в nbrk_rates.py:", e)
    logging.error(f"‼️ Ошибка: {e}")
