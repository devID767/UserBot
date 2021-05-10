from pyrogram import Client, filters
from pyrogram.errors import FloodWait

from time import sleep

import random

app = Client("my_account")

CanEat = False
CanWork = False
CanDuel = False

IsEating = False
IsWorking = False


@app.on_message(filters.text & filters.me & filters.command("help", prefixes="."))
def Help(client, message):
    message.delete()
    message.reply_text(".status\n"
                       ".settings\n"
                       ".delete [message]\n"
                       ".eat [on/name of command/stop]\n"
                       ".work [on/name of command/delete]\n"
                       ".duel [start/delete]\n"
                       ".type [message]\n"
                       ".ass\n"
                       ".pidor\n"
                       ".echo [num] [message]\n\n"
                       "Also can duel, eat and work")


@app.on_message(filters.text & filters.me & filters.command("status", prefixes="."))
def ShowStatus(client, message):
    message.delete()
    message.reply_text(f"IsEating = {IsEating}\n"
                       f"IsWorking = {IsWorking}")


@app.on_message(filters.text & filters.me & filters.command("settings", prefixes="."))
def Settings(client, message):
    message.delete()
    message.reply_text(f"CanEat = {CanEat}\n"
                       f"CanWork = {CanWork}\n"
                       f"CanDuel = {CanDuel}")


@app.on_message(filters.command("delete", prefixes=".") & filters.me)
def DeleteMessages(client, message):
    enteredText = message.text.split(".delete ", maxsplit=1)[1]
    message.delete()
    for msg in app.iter_history(message.chat.id, limit=100):
        if msg.text == enteredText:
            app.delete_messages(message.chat.id, msg.message_id, True)


@app.on_message(filters.command("eat", prefixes=".") & filters.me)
def EatCommand(client, message):
    command = message.text.split(".eat ", maxsplit=1)[1]
    message.delete()

    global CanEat
    global IsEating

    if command == "on":
        CanEat = True
        message.reply_text("Eat on")
    elif command.lower() == "покормить жабу" or command.lower() == "откормить жабу":
        Eating(message, command)
    elif command == "stop":
        CanEat = False
        IsEating = False
        message.reply_text("Eat stopped")
    else:
        message.reply_text("Error or incorrect eat")


def Eating(message, eat):
    global IsEating

    if not IsEating:
        IsEating = True
        while CanEat and IsEating:
            message.reply_text(eat, quote=False)
            sleep(5)  # 14400
        message.reply_text("Кормка завершена", quote=False)
        IsEating = False
    else:
        message.reply_text("Eating already started", qoute=False)


@app.on_message(filters.command("work", prefixes=".") & filters.me)
def WorkCommand(client, message):
    command = message.text.split(".work ", maxsplit=1)[1]
    message.delete()

    global CanWork
    global IsWorking

    if command == "on":
        CanWork = True
        message.reply_text("Work on")
    elif command.lower() == "поход в столовую" or command.lower() == "работа крупье" or command.lower() == "работа грабитель":
        Working(message, command)
    elif command == "stop":
        CanWork = False
        IsWorking = False
        message.reply_text("Work stopped")
    else:
        message.reply_text("Error or incorrect name of work")


def Working(message, work):
    global IsWorking

    if not IsWorking:
        IsWorking = True
        while CanWork and IsWorking:
            message.reply_text("Выйти из подземелья", quote=False)
            message.reply_text("Реанимировать жабу", quote=False)
            message.reply_text(work, quote=False)
            sleep(5)  # 7200
            if not IsWorking:
                break
            message.reply_text("Завершить работу", quote=False)
            sleep(10)  # 21600
        message.reply_text("Работа завершена", quote=False)
        IsWorking = False
    else:
        message.reply_text("Working already started")


@app.on_message(filters.command("duel", prefixes=".") & filters.me)
def DuelCommand(client, message):
    command = message.text.split(".duel ", maxsplit=1)[1]
    message.delete()
    global CanDuel
    if command == "start":
        CanDuel = True
        message.reply_text("Duel started")
    elif command == "stop":
        CanDuel = False
        message.reply_text("Duel stopped")
    else:
        message.reply_text("Error")


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
def ass(_, msg):
    perc = 0

    while (perc < 100):
        try:
            text = "Взлом жопы в процессе ..." + str(perc) + "%"
            msg.edit(text)

            perc += random.randint(3, 5)
            sleep(0.1);

        except FloodWait as e:
            sleep(e.x)

    msg.edit("Жопа успешно взломана!")


@app.on_message(filters.command("pidor", prefixes=".") & filters.me)
def FindPidor(_, message):
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


@app.on_message(filters.command("echo", prefixes=".") & filters.me)
def echo(_, msg):
    count = 0
    orig_text = msg.text.split(maxsplit=2)[2]
    max = int(msg.text.split(maxsplit=2)[1])

    msg.delete()
    while (max != count & max <= 100):
        msg.reply_text(orig_text)
        count += 1


@app.on_message(filters.text & filters.reply)
def Duel(client, message):
    if message.text.lower() == "дуэль принять":
        Oldmessage = app.get_messages(message.chat.id, reply_to_message_ids=message.message_id)
        if Oldmessage.from_user.is_self and CanDuel:
            sleep(15)
            message.reply_text("Реанимировать жабу", quote=False)
            message.reply_text("дуэль", quote=True)


app.run()
