import os
from dotenv import load_dotenv
import pathlib
from flask import (
    Flask,
    render_template,
    get_flashed_messages,
)

app = Flask(__name__)
# загрузка переменных окружения из скрытого файла
dotenv_path = pathlib.Path(pathlib.Path.cwd(), ".env")
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)
    app.secret_key = os.getenv('SECRET')


@app.route('/')
def index():
    mes = get_flashed_messages(with_categories=True)
    return render_template(
        'index.html', messages=mes)
