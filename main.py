from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.errors import FloodWait

from time import sleep

import Sending
import threading

app = Client("my_account")

Works = {}
Eats = {}
CanDuel = False

Triggers = {}
Timers = []

@app.on_message(filters.me & filters.command("help", prefixes="."))
def Help(client, message):
    message.delete()
    message.reply_text(".status\n"
                       ".delete [message]\n"
                       ".eat [name of command/stop]\n"
                       ".work [name of command/stop]\n"
                       ".timer [sec] (reply on message)\n"
                       ".trigger [name of trigger] (reply on message)\n"
                       ".duel [start/stop]\n"
                       ".echo [count] [message]\n"
                       ".convert [kits] [lvl]\n"
                       "\nAlso can duel, eat and work")

@app.on_message(filters.me & filters.command("status", prefixes="."))
def Status(client, message):
    message.delete()

    try:
        IsWorking = Works.get(message.chat.id).is_started
    except:
        IsWorking = False

    try:
        IsEating = Eats.get(message.chat.id).is_started
    except:
        IsEating = False

    message.reply_text(f"IsEating = {IsEating}\n"
                       f"IsWorking = {IsWorking}\n"
                       f"CanDuel = {CanDuel}")

@app.on_message(filters.command("trigger", prefixes=".") & filters.me)
def TriggerCommand(client, message):
    command = message.text.split(".trigger ", maxsplit=1)[1]

    if command == "delete":
        RepeatMessage = app.get_messages(message.chat.id, reply_to_message_ids=message.message_id)
        if Triggers[RepeatMessage.text.lower()].chat.id == message.chat.id:
            #Triggers.pop(RepeatMessage.text)
            message.reply_text(f'Триггер "{RepeatMessage.text}" : "{Triggers[RepeatMessage.text.lower()].text}" удален!')
            del Triggers[RepeatMessage.text.lower()]
    elif command == "show":
        printed = ""
        for triggers in Triggers:
            if Triggers[triggers].chat.id == message.chat.id:
                printed += f"{triggers} : {Triggers[triggers].text}\n"
        if printed == "":
            message.reply_text("Триггеров нет")
        else:
            message.reply_text(printed)
    else:
        RepeatMessage = app.get_messages(message.chat.id, reply_to_message_ids=message.message_id)
        Triggers[command.lower()] = RepeatMessage
        message.reply_text(f'Триггер "{command}" : "{RepeatMessage.text}" добавлен!')

    message.delete()

@app.on_message(filters.command("timer", prefixes=".") & filters.me)
async def TimerCommand(client, message):
    command = message.text.split(".timer ", maxsplit=1)[1]
    RepeatMessage = await app.get_messages(message.chat.id, reply_to_message_ids=message.message_id)

    global Timers

    if command == "stop":
        for timer in Timers:
            if timer.text == RepeatMessage.text and timer.chat == message.chat.id:
                await timer.Stop()
                Timers.remove(timer)
                await message.reply_text(f"{timer.text} stopped")
    elif command == "show":
        printed = ""
        for timer in Timers:
            if timer.chat == message.chat.id:
                printed += f"{timer.text} : {timer.time}\n"
        if printed != "":
            await message.reply_text(printed)
        else:
            await message.reply_text("Таймеров нет")
    else:
        timer = Sending.Customise(RepeatMessage.text, int(command), message.chat.id)
        Timers.append(timer)
        await timer.Start(message)

    await message.delete()


@app.on_message(filters.command("delete", prefixes=".") & filters.me)
def DeleteMessages(client, message):
    enteredText = message.text.split(".delete ", maxsplit=1)[1]
    message.delete()
    for msg in app.iter_history(message.chat.id, limit=100):
        if msg.text == enteredText:
            app.delete_messages(message.chat.id, msg.message_id, True)

@app.on_message(filters.command("eat", prefixes=".") & filters.me)
async def EatCommand(client, message):
    command = message.text.split(".eat ", maxsplit=1)[1]
    await message.delete()

    global Eats

    try:
        eat = Eats[message.chat.id]
    except:
        eat = Sending.Eat()
        Eats[message.chat.id] = eat

    if command.lower() == "покормить жабу" or command.lower() == "откормить жабу":
        await eat.Start(message, command)
    elif command == "stop":
        await eat.Stop()
        del Eats[message.chat.id]
        await message.reply_text("Eat stopped")
    else:
        await message.reply_text("Unknown command")

@app.on_message(filters.command("work", prefixes=".") & filters.me)
async def WorkCommand(client, message):
    command = message.text.split(".work ", maxsplit=1)[1]
    await message.delete()

    global Works

    try:
        work = Works[message.chat.id]
    except:
        work = Sending.Work()
        Works[message.chat.id] = work

    if command.lower() == "поход в столовую" or command.lower() == "работа крупье" or command.lower() == "работа грабитель":
        await work.Start(message, command)
    elif command == "stop":
        await work.Stop()
        del Works[message.chat.id]
        await message.reply_text("Work stopped")
    else:
        await message.reply_text("Unknown command")


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
    elif message.text.lower() in Triggers.keys():
        Oldmessage = app.get_messages(message.chat.id, reply_to_message_ids=message.message_id)
        if Oldmessage.from_user.is_self:
            message.reply_text(Triggers[message.text.lower()].text, quote=True)

@app.on_message(filters.command("echo", prefixes=".") & filters.me)
def echo(_, msg):
    count = 0
    orig_text = msg.text.split(maxsplit=2)[2]
    max = int(msg.text.split(maxsplit=2)[1])

    msg.delete()
    while (max != count & max <= 100):
        msg.reply_text(orig_text)
        count += 1


@app.on_message(filters.me & filters.command("convert", prefixes="."))
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
