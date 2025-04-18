from flask import Flask, request, Response
import subprocess
import threading
import traceback
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
is_running = False
SECRET_KEY = os.getenv("TRIGGER_KEY")  # ключ

def run_script():
    global is_running
    if is_running:
        print("Запуск уже идёт — пропускаем")
        return

    is_running = True
    try:
        print("Запуск скрипта nbrk_rates.py")
        subprocess.run(["python3", "nbrk_rates.py"])
        print("Скрипт завершён")
    except Exception as e:
        print("‼️ Ошибка при запуске скрипта:", e)
        traceback.print_exc()
    finally:
        is_running = False

@app.route("/")
def root():
    return "OK"  # для UptimeRobot

@app.route("/trigger")
def trigger():
    key = request.args.get("key")
    if key != SECRET_KEY:
        return Response("Доступ запрещён", status=403)
    
    threading.Thread(target=run_script).start()
    return "Скрипт запущен"
