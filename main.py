from flask import Flask, request, Response, jsonify
import subprocess
import threading
import traceback
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
is_running = False
SECRET_KEY = os.getenv("TRIGGER_KEY")

if not SECRET_KEY:
    print("⚠️ TRIGGER_KEY не задан в переменных окружения")

def run_script():
    global is_running
    if is_running:
        print("⚠️ Запуск уже идёт — пропускаем")
        return

    is_running = True
    try:
        print("▶️ Запуск скрипта nbrk_rates.py")
        subprocess.run(["python3", "nbrk_rates.py"])
        print("✅ Скрипт завершён")
    except Exception as e:
        print("‼️ Ошибка при запуске скрипта:", e)
        traceback.print_exc()
    finally:
        is_running = False

@app.route("/")
def root():
    return "OK"

@app.route("/trigger")
def trigger():
    key = request.args.get("key")
    if key != SECRET_KEY:
        return Response("🔒 Доступ запрещён", status=403)

    threading.Thread(target=run_script).start()
    return "🟢 Скрипт запущен"

@app.route("/status")
def status():
    print("📡 Вызов /status")
    try:
        if os.path.exists("log.txt"):
            modified = datetime.fromtimestamp(os.path.getmtime("log.txt"))
            with open("log.txt", "r", encoding="utf-8") as f:
                lines = f.readlines()
                last_line = lines[-1] if lines else "Лог пуст"
        else:
            modified = None
            last_line = "Файл log.txt не найден"

        return jsonify({
            "status": "🟢 OK",
            "last_updated": modified.strftime("%Y-%m-%d %H:%M:%S") if modified else "Нет данных",
            "last_log": last_line.strip()
        })

    except Exception as e:
        return jsonify({
            "status": "🔴 ERROR",
            "error": str(e)
        }), 500
