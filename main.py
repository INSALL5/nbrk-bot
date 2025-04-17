from flask import Flask
import subprocess
import threading

app = Flask(__name__)
is_running = False  # флаг для защиты

def run_script():
    global is_running
    if is_running:
        print("⏳ Запуск уже выполняется — пропуск")
        return

    is_running = True
    try:
        print("▶️ Запуск скрипта nbrk_rates.py")
        subprocess.run(["python3", "nbrk_rates.py"])
        print("✅ Завершено")
    except Exception as e:
        print("‼️ Ошибка:", e)
    finally:
        is_running = False

@app.route("/")
def index():
    threading.Thread(target=run_script).start()
    return "🕒 Обработка запущена"
