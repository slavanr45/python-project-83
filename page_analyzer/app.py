import os  # access to environment variables
from dotenv import load_dotenv  # load environment variables
from urllib.parse import urlparse
from datetime import date
import psycopg2
from psycopg2.extras import NamedTupleCursor
from psycopg2 import Error
import requests  # check url status_code
from contextlib import closing  # improving functional context menu
from flask import (
    Flask,
    redirect,
    render_template,
    request,
    flash,
    url_for)
from page_analyzer.validator import validate
from page_analyzer.search import search_data


# load environment variables from hidden file
load_dotenv()
app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')
DATABASE_URL = os.getenv('DATABASE_URL')


# starting page
@app.route('/')
def index():
    return render_template(
        'index.html')


# Create entity (Crud). Processing data form index.html
@app.route('/urls', methods=['post'])
def urls_post():
    url_raw = request.form.get('url', '')
    err = validate(url_raw)  # validating url
    if err:  # if error -> returinig to start page
        flash(err, 'alert alert-danger')
        return render_template(
            'index.html'), 422
    # if no error -> add URL to DataBase and redirect
    url = f'{urlparse(url_raw).scheme}://{urlparse(url_raw).netloc}'
    try:
        with closing(psycopg2.connect(DATABASE_URL)) as connection:
            with connection.cursor(cursor_factory=NamedTupleCursor) as cur:
                sql_query = """SELECT id
                               FROM urls
                               WHERE name = (%s)"""
                cur.execute(sql_query, (url,))
                query_data = cur.fetchone()
                if query_data is not None:
                    id = query_data.id
                    flash('Страница уже существует', 'alert alert-info')
                else:
                    dt = date.today()
                    sql_query = '''INSERT INTO urls (name, created_at)
                                   VALUES (%s, %s)
                                   RETURNING id'''
                    cur.execute(sql_query, (url, dt))
                    connection.commit()  # confirmation of change in DB
                    id = cur.fetchone().id
                    flash('Страница успешно добавлена', 'alert alert-success')
    except (Exception, Error) as error:
        print('Can`t establish connection to database', error)
    return redirect(url_for('url_get', id=id))


# View list of checked sites (cRud)
@app.route('/urls')
def urls_get():
    try:
        with closing(psycopg2.connect(DATABASE_URL)) as connection:
            with connection.cursor(cursor_factory=NamedTupleCursor) as cur:
                sql_query = """SELECT DISTINCT ON (urls.id)
                                    urls.id,
                                    urls.name,
                                    url_checks.status_code,
                                    url_checks.created_at
                               FROM urls LEFT JOIN url_checks
                               ON urls.id = url_checks.url_id
                               ORDER BY urls.id DESC;"""
                cur.execute(sql_query)
                data = cur.fetchall()
    except (Exception, Error) as error:
        print('Can`t establish connection to database', error)
    return render_template(
        'list.html',
        data=data)


# Display specific site in show.html (cRud)
@app.route('/urls/<int:id>')
def url_get(id):
    try:
        with closing(psycopg2.connect(DATABASE_URL)) as connection:
            with connection.cursor(cursor_factory=NamedTupleCursor) as cur:
                sql_query = """SELECT *
                               FROM urls
                               WHERE id = (%s)"""
                cur.execute(sql_query, (id,))
                curent_url = cur.fetchone()
                sql_query = """SELECT *
                               FROM url_checks
                               WHERE url_id = (%s)
                               ORDER BY id DESC"""
                cur.execute(sql_query, (id,))
                url_check = cur.fetchall()
    except (Exception, Error) as error:
        print('Can`t establish connection to database', error)
    return render_template(
        'show.html',
        curent_url=curent_url,
        url_check=url_check)


# Update of entity (crUd). Processing data form show.html
@app.route('/urls/<int:id>/checks', methods=['post'])
def url_post(id):
    try:
        with closing(psycopg2.connect(DATABASE_URL)) as connection:
            with connection.cursor(cursor_factory=NamedTupleCursor) as cur:
                sql_query = """SELECT *
                               FROM urls
                               WHERE id = (%s)"""
                cur.execute(sql_query, (id,))
                query_data = cur.fetchone()
                try:
                    # make get request
                    responce = requests.get(query_data.name, timeout=4)
                    responce.raise_for_status()
                except requests.RequestException:
                    flash('Произошла ошибка при проверке', 'alert alert-danger')
                    return redirect(url_for('url_get', id=id))
                status_code = responce.status_code  # check site status code
                # using BeutifilSoup for checking html code and collect data
                h1, title, descr = search_data(responce)
                dt = date.today()
                sql_query = '''INSERT INTO url_checks
                                (url_id, status_code, h1,
                                title, description, created_at)
                               VALUES (%s, %s, %s, %s, %s, %s)'''
                cur.execute(sql_query, (id, status_code, h1, title, descr, dt))
                connection.commit()  # подтверждение изменения
                flash('Страница успешно проверена', 'alert alert-success')
    except (Exception, Error) as error:
        print('Can`t establish connection to database', error)
    return redirect(url_for('url_get', id=id))
