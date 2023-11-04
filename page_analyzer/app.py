import os
from flask import Flask
from dotenv import load_dotenv
import pathlib

app = Flask(__name__)
# загрузка переменных окружения из скрытого файла
dotenv_path = pathlib.Path(pathlib.Path.cwd(), ".env")
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)
    app.secret_key = os.getenv('SECRET')


@app.route('/')
def index():
    return 'Hello world!'
