from pyrogram import Client, filters
from pyrogram.errors import FloodWait

from time import sleep

import sqlite3

app = Client("my_account")

CanEat = False
CanWork = False
CanDuel = False

conn = sqlite3.connect("groups.db")
cursor = conn.cursor()

# Создание таблицы
cursor.execute("""CREATE TABLE IF NOT EXISTS groups (
                   id INTEGER, 
                   IsEating TEXT, 
                   IsWorking TEXT);
               """)

cursor.execute("DELETE FROM groups")
conn.commit()

conn.close()


def InsertToBase(chat_id, IsEating, IsWorking):
    conn = sqlite3.connect('groups.db')
    cursor = conn.cursor()

    Delete(chat_id)

    cursor.execute("INSERT INTO groups VALUES(?, ?, ?);", (str(chat_id), str(IsEating), str(IsWorking)))
    conn.commit()

    conn.close()

def Delete(_chat_id):
    conn = sqlite3.connect('groups.db')
    cursor = conn.cursor()

    cursor.execute("DELETE FROM groups WHERE id = ?", (_chat_id,))
    conn.commit()

    conn.close()

def GetFromBase(_chat_id):
    try:
        conn = sqlite3.connect('groups.db')
        cursor = conn.cursor()

        sql_select_query = """select * from groups where id = ?"""
        cursor.execute(sql_select_query, (_chat_id,))
        records = cursor.fetchone()

        cursor.close()
    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)
    finally:
        if conn:
            conn.close()
        return records

def isEating(message):
    if GetFromBase(message.chat.id) is None:
        return False
    else:
        if GetFromBase(message.chat.id)[1] == "True":
            return True
        else:
            return False

def isWorking(message):
    if GetFromBase(message.chat.id) is None:
        return False
    else:
        if GetFromBase(message.chat.id)[2] == "True":
            return True
        else:
            return False


@app.on_message(filters.text & filters.me & filters.command("help", prefixes="."))
def Help(client, message):
    message.delete()
    message.reply_text(".status\n"
                       ".settings\n"
                       ".delete [message]\n"
                       ".eat [on/name of command/stop/off]\n"
                       ".work [on/name of command/stop/off]\n"
                       ".duel [start/delete]\n"
                       ".echo [num] [message]\n"
                       ".convert [kits] [lvl]\n"
                       "\nAlso can duel, eat and work")

@app.on_message(filters.text & filters.me & filters.command("status", prefixes="."))
def Status(client, message):
    message.delete()
    message.reply_text(f"IsEating = {isEating(message)}\n"
                       f"IsWorking = {isWorking(message)}")


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

    if command == "on":
        CanEat = True
        message.reply_text("Eat on")
    elif command.lower() == "покормить жабу" or command.lower() == "откормить жабу":
        Eating(message, command)
    elif command == "stop":
        IsEating = False
        InsertToBase(message.chat.id, IsEating, isWorking(message))
        message.reply_text("Eat stopped")
    elif command == "off":
        CanEat = False
        message.reply_text("Eat off")
    else:
        message.reply_text("Unknown command")

def Eating(message, eat):
    IsEating = isEating(message)

    if not IsEating:
        IsEating = True
        InsertToBase(message.chat.id, IsEating, isWorking(message))
        while CanEat and isEating(message):
            message.reply_text(eat, quote=False)
            if eat.lower() == "откормить жабу":
                sleep(14410)  #14400
            else:
                sleep(43210) #43200
        message.reply_text("Кормка завершена", quote=False)
        IsEating = False
        InsertToBase(message.chat.id, IsEating, isWorking(message))
    else:
        message.reply_text("Is Eating")


@app.on_message(filters.command("work", prefixes=".") & filters.me)
def WorkCommand(client, message):
    command = message.text.split(".work ", maxsplit=1)[1]
    message.delete()

    global CanWork

    if command == "on":
        CanWork = True
        message.reply_text("Work on")
    elif command.lower() == "поход в столовую" or command.lower() == "работа крупье" or command.lower() == "работа грабитель":
        Working(message, command)
    elif command == "stop":
        IsWorking = False
        InsertToBase(message.chat.id, isEating(message), IsWorking)
        message.reply_text("Work stopped")
    elif command == "off":
        CanWork = False
        message.reply_text("Work off")
    else:
        message.reply_text("Unknown command")


def Working(message, work):
    IsWorking = isWorking(message)

    if not IsWorking:
        IsWorking = True
        InsertToBase(message.chat.id, isEating(message), IsWorking)
        while CanWork and isWorking(message):
            message.reply_text("Выйти из подземелья", quote=False)
            message.reply_text("Реанимировать жабу", quote=False)
            message.reply_text(work, quote=False)
            sleep(7210)  # 7200
            if not isWorking(message):
                break
            message.reply_text("Завершить работу", quote=False)
            sleep(21610)  # 21600
        message.reply_text("Работа завершена", quote=False)
        IsWorking = False
        InsertToBase(message.chat.id, isEating(message), IsWorking)
    else:
        message.reply_text("Is Working")


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
        kit -= satiety
        money += satiety * 90

        lvl+=1
        countOfLvl+=1

    kit += money / 300

    return ConvertMethod(kit, lvl, countOfLvl)

app.run()
