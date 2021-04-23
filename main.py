from pyrogram import Client, filters
from pyrogram.errors import FloodWait

from time import sleep
import random

app = Client("my_account")

@app.on_message(filters.text & filters.reply & filters.me & filters.command("duel", prefixes="."))
def StartDuel(client, message):
    Oldmessage = app.get_messages(message.chat.id, reply_to_message_ids=message.message_id)
    max = int(message.text.split(".duel", maxsplit=1)[1])
    count = 0
    while(count < max):
        message.reply_text("Реанимировать жабу", quote=False)
        message.reply_text("дуэль", reply_to_message_id = Oldmessage.message_id)
        sleep(15)  # 43200
        count += 1


@app.on_message(filters.command("delete", prefixes=".") & filters.me)
def DeleteMessages(client, message):
    enteredText = message.text.split(".delete ", maxsplit=1)[1]
    message.delete()
    for msg in app.iter_history(message.chat.id, limit=100):
        if msg.text == enteredText:
            app.delete_messages(message.chat.id, msg.message_id, True)


# Покормить жабу
# .eat [к-во запусков]

@app.on_message(filters.command("eat", prefixes=".") & filters.me)
def Eat(_, msg):
    start = True

    try:
        max = int(msg.text.split(".eat ", maxsplit=1)[1])
        if max > 10 and max < 1:
            start = False
            app.send_message("me", "num can't be > 50 and < 0")
    except:
        app.send_message("me", "Введи еще число")
        start = False

    msg.delete()
    count = 0
    while (start):
        if count == max:
            break
        msg.reply_text("Откормить жабу")
        sleep(14410)  # 43200

        count += 1


# Отправить жабу на работу
# .work [к-во запусков]
@app.on_message(filters.command("work", prefixes=".") & filters.me)
def Work(_, msg):
    start = True

    try:
        max = int(msg.text.split(".work ", maxsplit=1)[1])
        if max > 10 and max < 1:
            start = False
            app.send_message("me", "num can't be > 50 and < 0")
    except:
        app.send_message("me", "Введи еще число")
        start = False

    count = 0
    msg.delete()
    while (start):
        if (count == max):
            break
        msg.reply_text("Завершить работу")
        msg.reply_text("Реанимировать жабу")
        msg.reply_text("Работа грабитель")
        # кд до след работы
        sleep(28820)  # 21600

        count += 1


@app.on_message(filters.command("type", prefixes=".") & filters.me)
def type(_, msg):
    orig_text = msg.text.split(".type ", maxsplit=1)[1]
    text = orig_text
    tbp = ""
    typing_symbol = "#"

    while (tbp != orig_text):
        try:
            msg.edit(tbp + typing_symbol)
            sleep(0.1)
            tbp = tbp + text[0]
            text = text[1:]

            msg.edit(tbp)
            sleep(0.1)

        except FloodWait as e:
            sleep(e.x)


@app.on_message(filters.command("ass", prefixes=".") & filters.me)
def hack(_, msg):
    perc = 0

    while (perc < 100):
        try:
            text = "Взлом жопы в процессе ..." + str(perc) + "%"
            msg.edit(text)

            perc += random.randint(1, 3)
            sleep(0.1);

        except FloodWait as e:
            sleep(e.x)

    msg.edit("Жопа успешно взломана!")


@app.on_message(filters.command("pidor", prefixes=".") & filters.me)
def FindPidoras(_, message):
    members = app.get_chat_members(message.chat.id)
    indexOfPidor = random.randrange(0, len(members), 1)
    pidorUser = members[indexOfPidor].user
    pidorUserName = pidorUser.username

    perc = 0

    while (perc < 100):
        try:
            text = "Ищу пидора ..." + str(perc) + "%"
            message.edit(text)

            perc += random.randint(3, 6)
            sleep(0.1);

        except FloodWait as e:
            sleep(e.x)

    message.edit(f"Пидором является: @{pidorUserName}")


@app.on_message(filters.command("reply", prefixes=".") & filters.me)
def echo(_, msg):
    count = 0
    orig_text = msg.text.split(maxsplit=2)[2]
    max = int(msg.text.split(maxsplit=2)[1])

    msg.delete()
    while (max != count):
        msg.reply_text(orig_text)
        count += 1


app.run()

