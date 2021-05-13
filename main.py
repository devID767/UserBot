from pyrogram import Client, filters
from pyrogram.errors import FloodWait

from time import sleep

import Sending

app = Client("my_account")

Works = {}
Eats = {}
CanDuel = False

@app.on_message(filters.text & filters.me & filters.command("help", prefixes="."))
def Help(client, message):
    message.delete()
    message.reply_text(".status\n"
                       ".delete [message]\n"
                       ".eat [name of command/stop]\n"
                       ".work [name of command/stop]\n"
                       ".duel [start/stop]\n"
                       ".echo [num] [message]\n"
                       ".convert [kits] [lvl]\n"
                       "\nAlso can duel, eat and work")

@app.on_message(filters.text & filters.me & filters.command("status", prefixes="."))
def Status(client, message):
    message.delete()

    try:
        IsWorking = Works.get(message.chat.id).IsWorking
    except:
        IsWorking = False

    try:
        IsEating = Eats.get(message.chat.id).IsEating
    except:
        IsEating = False

    message.reply_text(f"IsEating = {IsEating}\n"
                       f"IsWorking = {IsWorking}\n"
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

    global Eats

    try:
        eat = Eats[message.chat.id]
    except:
        eat = Sending.Eat()
        Eats[message.chat.id] = eat

    if command.lower() == "покормить жабу" or command.lower() == "откормить жабу":
        eat.Eating(message, command)
    elif command == "stop":
        eat.IsEating = False
        eat.eatSleep.set()
        Eats.pop(message.chat.id)
        message.reply_text("Eat stopped")
    else:
        message.reply_text("Unknown command")

@app.on_message(filters.command("work", prefixes=".") & filters.me)
def WorkCommand(client, message):
    command = message.text.split(".work ", maxsplit=1)[1]
    message.delete()

    global Works

    try:
        work = Works[message.chat.id]
    except:
        work = Sending.Work()
        Works[message.chat.id] = work

    if command.lower() == "поход в столовую" or command.lower() == "работа крупье" or command.lower() == "работа грабитель":
        work.Working(message, command)
    elif command == "stop":
        work.IsWorking = False
        work.workSleep.set()
        Works.pop(message.chat.id)
        message.reply_text("Work stopped")
    else:
        message.reply_text("Unknown command")


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
        message.reply_text("Unknown command")

@app.on_message(filters.text & filters.reply)
def Duel(client, message):
    if message.text.lower() == "дуэль принять":
        Oldmessage = app.get_messages(message.chat.id, reply_to_message_ids=message.message_id)
        if Oldmessage.from_user.is_self and CanDuel:
            sleep(10)
            message.reply_text("Реанимировать жабу", quote=False)
            message.reply_text("дуэль", quote=True)


@app.on_message(filters.command("echo", prefixes=".") & filters.me)
def echo(_, msg):
    count = 0
    orig_text = msg.text.split(maxsplit=2)[2]
    max = int(msg.text.split(maxsplit=2)[1])

    msg.delete()
    while (max != count & max <= 100):
        msg.reply_text(orig_text)
        count += 1


@app.on_message(filters.text & filters.me & filters.command("convert", prefixes="."))
def Convert(client, message):
    kit = int(message.text.split(maxsplit=2)[1])
    lvl = int(message.text.split(maxsplit=2)[2])

    message.delete()
    message.reply_text(f"{kit} аптечек даст тебе {str(ConvertMethod(kit, lvl))} уровней")

def ConvertMethod(kit, lvl, countOfLvl = 0):
    satiety = lvl + 10
    if kit < satiety:
        return countOfLvl

    money = 0
    while kit > satiety:
        satiety = lvl + 10
        kit -= satiety
        money += satiety * 90

        lvl+=1
        countOfLvl+=1

    kit += money / 300

    return ConvertMethod(kit, lvl, countOfLvl)

app.run()
