import os  # доступ к переменным окружения
from dotenv import load_dotenv  # загрузка переменных окружения
import validators  # проверка url
from urllib.parse import urlparse  # парсинг url
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


data = None
try:
    # коннект к существуюей базе данных с помощью DB_URL
    # Параметры соединения взяты из файла .env
    with closing(psycopg2.connect(DATABASE_URL)) as connection:
        print('Connection to database established!')
        # получение объекта cursor для доступа к БД.
        # Работаем через контекстный менеджер, для освобождения курсора
        with connection.cursor(cursor_factory=NamedTupleCursor) as curs:
            # выполняем SQL запрос
            # curs.execute('INSERT INTO urls (name, created_at) VALUES (%s,%s)', ('NewName', None))
            # connection.commit()
            curs.execute('SELECT * FROM urls')
            # получение даных cursor.fetchall() - вернуть все строки
            data = curs.fetchall()
except (Exception, Error) as error:
    # в случае сбоя подключения будет выведено сообщение
    print('Can`t establish connection to database', error)


# стартовая страница
@app.route('/')
def index():
    mes = get_flashed_messages(with_categories=True)
    return render_template(
        'index.html', messages=mes)


# Создание сущности (Create). Обработка данных формы от index.html
@app.route('/urls', methods=['post'])
def urls_post():
    url = request.form.get('url', '')
    err = validate(url)  # проверка корректности url
    if err:  # при ошибке возврат на стартовую страницу с выводом ошибки
        flash(err, "alert alert-danger")
        return redirect(url_for('index'))
    url = f'{urlparse(url).scheme}://{urlparse(url).hostname}'
    flash('Страница успешно добавлена', "alert alert-success")
    return redirect(url_for('urls_show'))


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
    mes = get_flashed_messages(with_categories=True)
    return render_template(
        'urls/index.html', messages=mes)


# Отображение (show.html)  -  cRud
@app.route('/urlss')
def urls_show():
    mes = get_flashed_messages(with_categories=True)
    return render_template(
        'urls/show.html', messages=mes)
