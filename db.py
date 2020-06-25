from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import QueuePool
from pyrogram import Client, Filters
from json import loads

with open("./config.json", "r") as f:
    cfg = loads(f.read())
botID = cfg["botID"]
api_id = cfg["api_id"]
api_hash = cfg["api_hash"]
dbLink = cfg["dbLink"]

app = Client("my_account", api_id, api_hash)
engine = create_engine(dbLink)
base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

class Entry(base):
    __tablename__ = 'telegram'
    index = Column(Integer, primary_key=True)
    name = Column(String(128))
    fname = Column(String(128))
    phone = Column(String(128))
    uid = Column(String(128))
    nik = Column(String(128))
    wo = Column(String(128))

    def __init__(self, name, fname, phone, uid, nik, wo):
        self.name = name
        self.fname = fname
        self.phone = phone
        self.uid = uid
        self.nik = nik
        self.wo = wo

base.metadata.create_all(engine)

@app.on_message(Filters.new_chat_members)
def leaveUnauthChat(client, message):
    if message["new_chat_members"][0]["id"] == botID:
        app.send_message(chat_id=message.chat.id, text="Этот бот работает только в ЛС. Напишите этому боту, чтобы узнать, если вы находитесь в базе.")
        app.leave_chat(message["chat"]["id"])

@app.on_message(Filters.command("start"))
def start(client, message):
    if message["chat"]["type"] == "private":
        looking = app.send_message(chat_id=message.chat.id, text="Ищем в базе...")
        obj = session.query(Entry).filter(Entry.uid == str(message["from_user"]["id"])).all()
        if len(obj) == 0:
            app.edit_message_text(chat_id=message.chat.id, message_id=looking.message_id, text="Поздравляем, вас нет в базе!\n\nДля вашей безопасности выключите возможность нахождения вас по номеру телефона.\n\nНастройки > кто видит мой номер телефона > никто > кто может найти меня по номеру телефона > мои контакты (наглядно [тут](https://t.me/tginfo/2217)).", parse_mode="markdown")
        else:
            n = len(obj)
            raz = 'раз'
            if n % 10 == 2 or n % 10 == 3 or n % 10 == 4:
                raz = 'раза'
            if n % 100 == 12 or n % 100 == 13 or n % 100 == 14:
                raz = 'раз'
            toUser = f"Увы, вы найдены в базе {n} {raz}! Вот ваши данные..."
            for mention in obj:
                if mention.wo == "" or mention.wo == " ":
                    date = ""
                else:
                    date = datetime.fromtimestamp(int(mention.wo.strip("0")))
                toUser = toUser + f"\n\nИмя: `{mention.name}`\nФамилия: `{mention.fname}`\nТелефонный номер: `{mention.phone}`\nУникальный ID в Telegram: `{mention.uid}`\nИмя пользователя: `{mention.nik}`\nВремя последней сетевой активности: `{date}`"
            toUser = toUser + "\n\nДля вашей безопасности выключите возможность нахождения вас по номеру телефона.\n\nНастройки > кто видит мой номер телефона > никто > кто может найти меня по номеру телефона > мои контакты (наглядно [тут](https://t.me/tginfo/2217))."    
            app.edit_message_text(chat_id=message.chat.id, message_id=looking.message_id, text=toUser, parse_mode="markdown")

app.run()