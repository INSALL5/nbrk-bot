import pandas as pd
import requests
from datetime import datetime
from dotenv import load_dotenv
import os
import logging

# Удаление лога, если больше 1 МБ
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

today = datetime.today().strftime("%d.%m.%Y")
url = f"https://nationalbank.kz/rss/get_rates.cfm?fdate={today}"

try:
    response = requests.get(url)
    response.raise_for_status()
    df = pd.read_xml(response.content)

    if df.empty:
        logging.warning("⚠️ DataFrame пустой. Возможно, проблема с XML.")
    else:
        file_name = f"курсы_валют_НБРК_{today.replace('.', '-')}.xlsx"
        df.to_excel(file_name, index=False)
        logging.info(f"✅ Файл {file_name} сохранён.")

        # Отправка текстового уведомления
        requests.post(
            f"https://api.telegram.org/bot{TOKEN}/sendMessage",
            data={
                "chat_id": CHAT_ID,
                "text": f"📥 Курсы валют на {today} загружены. Файл отправляется..."
            }
        )

        # Отправка Excel файла
        with open(file_name, "rb") as file:
            send_resp = requests.post(
                f"https://api.telegram.org/bot{TOKEN}/sendDocument",
                data={"chat_id": CHAT_ID},
                files={"document": file}
            )

        if send_resp.status_code == 200:
            logging.info("✅ Файл отправлен в Telegram.")
        else:
            logging.error(f"❌ Ошибка Telegram API: {send_resp.status_code} - {send_resp.text}")

except Exception as e:
    logging.error(f"‼️ Ошибка: {e}")
    print("‼️ Ошибка в nbrk_rates.py:", e)
