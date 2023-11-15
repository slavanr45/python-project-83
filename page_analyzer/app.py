import os  # доступ к переменным окружения
from dotenv import load_dotenv  # загрузка переменных окружения
import psycopg2
from psycopg2.extras import NamedTupleCursor
from psycopg2 import Error
from contextlib import closing  # расш функционал контекстного меню
from flask import (
    Flask,
    render_template,
    get_flashed_messages,
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
            connection.commit()
            curs.execute('SELECT * FROM urls')
            # получение даных cursor.fetchall() - вернуть все строки
            data = curs.fetchall()
except (Exception, Error) as error:
    # в случае сбоя подключения будет выведено сообщение
    print('Can`t establish connection to database', error)


@app.route('/')
def index():
    if data:
        return f'{data}, {DATABASE_URL}'
    else:
        mes = get_flashed_messages(with_categories=True)
        return render_template(
            'index.html', messages=mes)
