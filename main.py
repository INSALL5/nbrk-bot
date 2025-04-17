from flask import Flask
import subprocess
import threading
import traceback

app = Flask(__name__)

def run_script():
    try:
        print("▶️ Запуск скрипта nbrk_rates.py")
        subprocess.run(["python3", "nbrk_rates.py"])
        print("✅ Скрипт завершён")
    except Exception as e:
        print("‼️ Ошибка при запуске скрипта:", e)
        traceback.print_exc()

@app.route("/")
def index():
    threading.Thread(target=run_script).start()
    return "🕒 Обработка запущена"
