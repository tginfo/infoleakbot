# Leak Info Bot

## О боте

[Бот](https://t.me/infoleakbot) ищет в базе ID пользователя и возвращает, есть ли в ней ID или нет.

## Что надо установить

* PostgreSQL 12+ (работает на 12.3)
* Python 3+ (работает на 3.8)
* pip3
* python3-psycopg2. На Ubuntu/Debian пропишите `$ apt install python3-psycopg2`

## Установить зависимости

```
$ pip3 install -r requirements.txt
```

## Подготовка бота

1. Создайте базу для проверке по ней и мигрируйте её в PostgreSQL. Если база находится в формате SQLite, можно установить `pgloader`, отредактировать файл `pgmig` для своих нужд, и использовать команду `$ pgloader pgmig`
2. Отредактируйте `config.json` и установите: ID бота (необязательно), API ID и API Hash приложения (можно его получить [здесь](https://my.telegram.org)), и ссылку на БД.
3. (Рекомендуемо) Зайдите с помощью `psql` в базу, и пропишите `CREATE INDEX uid_1 ON telegram(uid);`. Это оптимизирует базу.

## Запуск бота

Я использую `tmux` для бота.

```
$ tmux new -s leakbot
$ python3 db.py
```

Во время первого запуска надо прописать API ключ бота.

## Q&A

Q: У меня бот очень долго ищет пользователей!<br>
A: Выполните этап №3 в параграфе "Подготовка бота".

Q: Я не хочу устанавливать PostgreSQL...<br>
A: Можно в этом случае использовать Docker.

```
$ docker pull postgres
$ docker run --name postgres -e POSTGRES_PASSWORD=docker -d -p 5432:5432 postgres
```

Q: Что-то сломалось!<br>
A: Пишите [veewo](https://t.me/veewo) с дебаг-логом от скрипта.

## Спасибо

- [Loskir](https://t.me/Loskirs) за помощью с оптимизацией базы!
- [tginfo](https://t.me/tginfo) за возможность испытать такого бота.