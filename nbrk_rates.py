import pandas as pd
import requests
from datetime import datetime
from dotenv import load_dotenv
import os
import logging

# Удаляем log.txt, если превышает 1 МБ
if os.path.exists("log.txt") and os.path.getsize("log.txt") > 1_000_000:
    os.remove("log.txt")

# Настройка логирования
logging.basicConfig(
    filename="log.txt",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Загрузка переменных окружения
load_dotenv()
TOKEN = os.getenv("TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

# Получаем текущую дату и URL
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

    # Отправка файла в Telegram
    try:
        with open(file_name, "rb") as file:
            send_resp = requests.post(
                f"https://api.telegram.org/bot{TOKEN}/sendDocument",
                data={"chat_id": CHAT_ID},
                files={"document": file}
            )

        if send_resp.status_code == 200:
            logging.info(f"Файл {file_name} успешно отправлен в Telegram.")
        else:
            logging.error(f"Ошибка Telegram API: {send_resp.status_code} - {send_resp.text}")

    except Exception as e:
        logging.error(f"Ошибка при отправке файла в Telegram: {e}")

except Exception as e:
    logging.error(f"Ошибка при получении или обработке данных: {e}")
