#!/usr/bin/env bash

# Postgres позволяет подключиться к удаленной базе указав ссылку на нее после флага -d
# ссылка подгрузится из переменной окружения, которую нужно указать на сервисе деплоя
# дальше мы загружаем в поключенную базу наш sql-файл с таблицами
make install && psql -a -d postgres://postgres_rmev_user:wXSIbr4wkvtYeqF4wF3urGFVJiLZi6t1@dpg-clac5p62eqrc7398jsug-a/postgres_rmev -f database.sql