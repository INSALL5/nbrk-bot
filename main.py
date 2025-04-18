from flask import Flask, Response
import subprocess
import threading
import traceback

app = Flask(__name__)
is_running = False  # защита от двойного запуска

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
        print("Ошибка при запуске скрипта:", e)
        traceback.print_exc()
    finally:
        is_running = False

@app.route("/")
def index():
    threading.Thread(target=run_script).start()
    return Response(status=204)  # Пустой ответ, чтобы cron не падал
