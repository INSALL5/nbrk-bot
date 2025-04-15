
import pandas as pd
import requests
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()

today = datetime.today().strftime("%d.%m.%Y")
url = f"https://nationalbank.kz/rss/get_rates.cfm?fdate={today}"

response = requests.get(url)
response.raise_for_status()

df = pd.read_xml(response.content)
file_name = f"курсы_валют_НБРК_{today.replace('.', '-')}.xlsx"
df.to_excel(file_name, index=False)
print(f"Файл сохранён: {file_name}")

TOKEN = os.getenv("TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

with open(file_name, "rb") as file:
    requests.post(
        f"https://api.telegram.org/bot{TOKEN}/sendDocument",
        data={"chat_id": CHAT_ID},
        files={"document": file}
    )
