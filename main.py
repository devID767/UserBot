from pyrogram import Client, filters
from pyrogram.errors import FloodWait

from time import sleep
import random

app = Client("my_account")

IsWorking = False
IsEating = False
IsDueling = False

@app.on_message(filters.text & filters.me & filters.command("help", prefixes="."))
def Help(client, message):
    message.delete()
    message.reply_text(".status\n"
                       ".delete [message]\n"
                       ".eat [start/stop]\n"
                       ".work [start/delete]\n"
                       ".duel [start/delete]\n"
                       ".type [message]\n"
                       ".ass\n"
                       ".pidor\n"
                       ".echo [num] [message]\n\n"
                       "Also can duel, eat and work")


@app.on_message(filters.text & filters.me & filters.command("status", prefixes="."))
def Status(client, message):
    message.delete()
    message.reply_text(f"IsWorking = {IsWorking}\n"
                       f"IsEating = {IsEating}\n"
                       f"IsDueling = {IsDueling}")

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
    global IsEating
    if command == "start":
        IsEating = True
        message.reply_text("Eat started")
    elif command == "stop":
        IsEating = False
        message.reply_text("Eat stopped")
    else:
        message.reply_text("Error")

@app.on_message(filters.command("work", prefixes=".") & filters.me)
def WorkCommand(client, message):
    command = message.text.split(".work ", maxsplit=1)[1]
    message.delete()
    global IsWorking
    if command == "start":
        IsWorking = True
        message.reply_text("Work started")
    elif command == "stop":
        IsWorking = False
        message.reply_text("Work stopped")
    else:
        message.reply_text("Error")


@app.on_message(filters.command("duel", prefixes=".") & filters.me)
def DuelCommand(client, message):
    command = message.text.split(".duel ", maxsplit=1)[1]
    message.delete()
    global IsDueling
    if command == "start":
        IsDueling = True
        message.reply_text("Duel started")
    elif command == "stop":
        IsDueling = False
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
def StartDuel(client, message):
    if message.text.lower() == "дуэль принять":
        Oldmessage = app.get_messages(message.chat.id, reply_to_message_ids=message.message_id)
        if Oldmessage.from_user.is_self and IsDueling:
            sleep(15)
            message.reply_text("Реанимировать жабу", quote=False)
            message.reply_text("дуэль", quote=True)


@app.on_message(filters.text & filters.me)
def StartCommand(client, message):
    if IsWorking and message.text == "Поход в столовую":
        message.reply_text("запущенно")
        sleep(7210)  # 7200
        message.reply_text("Завершить работу")
        sleep(21610)  # 21600
        message.reply_text("Выйти из подземелья")
        message.reply_text("Реанимировать жабу")
        message.reply_text("Поход в столовую")
    elif IsEating and message.text == "Откормить жабу":
        message.reply_text("Откормить жабу")
        sleep(14410)  #14400
        message.reply_text("Откормить жабу")

app.run()

