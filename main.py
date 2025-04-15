
from flask import Flask
import subprocess

app = Flask(__name__)

@app.route("/")
def run_script():
    subprocess.run(["python3", "nbrk_rates.py"])
    return "Курсы валют обновлены!"

app.run(host="0.0.0.0", port=8080)
