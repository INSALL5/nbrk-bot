from flask import Flask
import subprocess
import threading

app = Flask(__name__)

def run_script():
    subprocess.run(["python3", "nbrk_rates.py"])

@app.route("/")
def index():
    threading.Thread(target=run_script).start()
    return "🕒 Обработка запущена"
