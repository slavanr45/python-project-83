import os  # доступ к переменным окружения
from dotenv import load_dotenv  # загрузка переменных окружения
import validators  # проверка url
from urllib.parse import urlparse  # парсинг url
from datetime import date
import psycopg2
from psycopg2.extras import NamedTupleCursor
from psycopg2 import Error
from contextlib import closing  # расш функционал контекстного меню
from flask import (
    Flask,
    redirect,
    render_template,
    request,
    flash,
    get_flashed_messages,
    url_for
)

app = Flask(__name__)
# удалить тестилку
test1 = 'test1'
# загрузка переменных окружения из скрытого файла
load_dotenv()
app.secret_key = os.getenv('SECRET')
DATABASE_URL = os.getenv('DATABASE_URL')


# стартовая страница
@app.route('/')
def index():
    mes = get_flashed_messages(with_categories=True)
    return render_template(
        'index.html', messages=mes)


# Создание сущности (Create). Обработка данных формы от index.html
@app.route('/urls', methods=['post'])
def urls_post():
    url_raw = request.form.get('url', '')
    err = validate(url_raw)  # проверка корректности url
    if err:  # при ошибке возврат на стартовую страницу с выводом ошибки
        flash(err, "alert alert-danger")
        return redirect(url_for('index'))
    # если ошибок нет, то добавляем URL в БД и редирект
    url = f'{urlparse(url_raw).scheme}://{urlparse(url_raw).hostname}'
    try:
        # коннект к существуюей базе данных с помощью DB_URL
        with closing(psycopg2.connect(DATABASE_URL)) as connection:
            with connection.cursor(cursor_factory=NamedTupleCursor) as cur:
                dt = date.today()
                sql_query = '''INSERT INTO urls (name, created_at)
                                VALUES (%s, %s)
                                RETURNING id'''
                cur.execute(sql_query, (url, dt))
                connection.commit()  # подтверждение изменения
                id = cur.fetchone().id
    except (Exception, Error) as error:
        print('Can`t establish connection to database', error)
    flash('Страница успешно добавлена', "alert alert-success")
    return redirect(url_for('url_get', id=id))


def validate(url: str) -> str:
    err = ''
    if not url:
        err = 'URL обязателен'
    elif len(url) > 255 or not validators.url(url):
        err = 'Некорректный URL'
    return err


# Список проверенных сайтов (Read)
@app.route('/urls')
def urls_get():
    try:
        # коннект к существуюей базе данных с помощью DB_URL
        with closing(psycopg2.connect(DATABASE_URL)) as connection:
            with connection.cursor(cursor_factory=NamedTupleCursor) as cur:
                sql_query = """SELECT *
                                FROM urls
                                ORDER BY id DESC"""
                cur.execute(sql_query)
                data = cur.fetchall()
    except (Exception, Error) as error:
        print('Can`t establish connection to database', error)
    return render_template(
        'urls/index.html',
        data=data)


# Отображение (show.html)  -  cRud
@app.route('/urls/<int:id>')
def url_get(id):
    try:
        # коннект к существуюей базе данных с помощью DB_URL
        with closing(psycopg2.connect(DATABASE_URL)) as connection:
            with connection.cursor(cursor_factory=NamedTupleCursor) as cur:
                sql_query = """SELECT *
                                FROM urls
                                WHERE id = (%s)"""
                cur.execute(sql_query, (id,))
                curent_url = cur.fetchone()
                print(curent_url)
    except (Exception, Error) as error:
        print('Can`t establish connection to database', error)
    mes = get_flashed_messages(with_categories=True)
    return render_template(
        'urls/show.html',
        curent_url=curent_url,
        messages=mes)
