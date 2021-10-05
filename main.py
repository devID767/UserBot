import asyncio

from pyrogram import Client, filters

import Sending
import Data

app = Client("my_account")
#app = Client("anya")
#app = Client("pasha")

@app.on_message(filters.me & filters.command("help", prefixes="."))
async def Help(client, message):
    await message.delete()
    await message.reply_text(".status\n"
                       ".delete [message]\n"
                       ".eat [name of command/stop]\n"
                       ".work [name of command/stop]\n"
                       ".timer [num/stop/show] [sec/ minutes/ hours/ days]\n"
                             "(ответом на сообщение. \nЕсли набрать вначале сообщения '.test', то оно автоматически удалится)\n"
                       ".trigger [name of trigger/delete/show/all/restore]\n"
                             "(ответом на сообщение. \nЕсли набрать вначале сообщения '.test', то оно автоматически удалится)\n"
                       ".duel [start/stop] [count/none]\n"
                       ".craft\n"
                       ".echo [count] [message]\n"
                       ".convert [kits] [lvl]\n"
                       "\nAlso can duel, eat and work")

@app.on_message(filters.me & filters.command("status", prefixes="."))
async def Status(client, message):
    await message.delete()

    try:
        IsWorking = Data.Works.get(message.chat.id).is_started
    except:
        IsWorking = False

    try:
        IsEating = Data.Eats.get(message.chat.id).is_started
    except:
        IsEating = False

    try:
        Count = Data.DuelCount[message.chat.id]
    except:
        Count = 0

    await message.reply_text(f"IsEating = {IsEating}\n"
                       f"IsWorking = {IsWorking}\n"
                       f"CanDuel = {Data.CanDuel} : {Count}")

@app.on_message(filters.command("trigger", prefixes=".") & filters.me)
async def TriggerCommand(client, message):
    command = message.text.split(".trigger ", maxsplit=1)[1]

    if command == "delete":
        RepeatMessage = await app.get_messages(message.chat.id, reply_to_message_ids=message.message_id)
        if Data.Triggers[RepeatMessage.text.lower()]['chat'] == message.chat.id:
            await message.reply_text(f'Триггер "{RepeatMessage.text}" : "{Data.Triggers[RepeatMessage.text.lower()]["text"]}" удален!')
            del Data.Triggers[RepeatMessage.text.lower()]
        Data.saveTriggers()
    elif command == "restore":
        Data.Triggers.clear()
        Data.saveTriggers()
        await message.reply_text(
            f'Триггеры удалены')
    elif command == "show":
        printed = ""
        for triggers in Data.Triggers:
            if Data.Triggers[triggers].get("chat") == message.chat.id:
                printed += f"{triggers} : {Data.Triggers[triggers].get('text')}\n"
        if printed == "":
            await message.reply_text("Триггеров нет")
        else:
            await message.reply_text(printed)
    elif command == "all":
        printed = ""
        for triggers in Data.Triggers:
            printed += f"{triggers} : {Data.Triggers[triggers].get('text')} \n{Data.Triggers[triggers].get('chat')}\n"
        if printed == "":
            await message.reply_text("Триггеров нет")
        else:
            await message.reply_text(printed)
    else:
        RepeatMessage = await app.get_messages(message.chat.id, reply_to_message_ids=message.message_id)

        if '.test' in RepeatMessage.text:
            RepeatMessage.text = RepeatMessage.text.split(maxsplit=1)[1]

        Data.newTrigger(command.lower(), RepeatMessage.text, RepeatMessage.chat.id)
        await message.reply_text(f'Триггер "{command}" : "{RepeatMessage.text}" добавлен!')

    await message.delete()

@app.on_message(filters.command("timer", prefixes=".") & filters.me)
async def TimerCommand(client, message):
    command = message.text.split(maxsplit=2)[1]
    RepeatMessage = await app.get_messages(message.chat.id, reply_to_message_ids=message.message_id)

    if command == "stop":
        for timer in Data.Timers:
            if timer.text == RepeatMessage.text and timer.chat == message.chat.id:
                await timer.Stop()
                Data.Timers.remove(timer)
                await message.reply_text(f"{timer.text} stopped")
    elif command == "show":
        printed = ""
        for timer in Data.Timers:
            if timer.chat == message.chat.id:
                if timer.typeOfTime == 'sec':
                    time = timer.time
                elif timer.typeOfTime == 'minutes':
                    time = timer.time / 60
                elif timer.typeOfTime == 'hours':
                    time = timer.time / 3600
                elif timer.typeOfTime == 'days':
                    time = timer.time / 86400
                printed += f"{timer.text} : {int(time)} {timer.typeOfTime}\n"
        if printed != "":
            await message.reply_text(printed)
        else:
            await message.reply_text("Таймеров нет")
    else:
        try:
            typeOfTime = message.text.split(maxsplit=2)[2]
        except:
            typeOfTime = ''

        if typeOfTime == 'sec':
            time = int(command)
        elif typeOfTime == 'minutes':
            time = int(command) * 60
        elif typeOfTime == 'hours':
            time = int(command) * 3600
        elif typeOfTime == 'days':
            time = int(command) * 86400
        else:
            await message.reply_text('Неверно задан тип времени')

        if '.test' in RepeatMessage.text:
            RepeatMessage.text = RepeatMessage.text.split(maxsplit=1)[1]

        timer = Sending.Customise(RepeatMessage.text, time, typeOfTime, message.chat.id)
        Data.Timers.append(timer)
        Data.saveArray("Timers", Data.Timers)
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

    try:
        eat = Data.Eats[message.chat.id]
    except:
        eat = Sending.Eat()
        Data.Eats[message.chat.id] = eat

    if command.lower() == "покормить жабу" or command.lower() == "откормить жабу":
        await eat.Start(message, command)
    elif command == "stop":
        await eat.Stop()
        del Data.Eats[message.chat.id]
        await message.reply_text("Eat stopped")
    else:
        await message.reply_text("Unknown command")

@app.on_message(filters.command("work", prefixes=".") & filters.me)
async def WorkCommand(client, message):
    command = message.text.split(".work ", maxsplit=1)[1]
    await message.delete()

    try:
        work = Data.Works[message.chat.id]
    except:
        work = Sending.Work()
        Data.Works[message.chat.id] = work

    if command.lower() == "поход в столовую" or command.lower() == "работа крупье" or command.lower() == "работа грабитель":
        await work.Start(message, command)
    elif command == "stop":
        await work.Stop()
        del Data.Works[message.chat.id]
        await message.reply_text("Work stopped")
    else:
        await message.reply_text("Unknown command")


@app.on_message(filters.command("duel", prefixes=".") & filters.me)
async def DuelCommand(client, message):
    command = message.text.split(maxsplit=2)[1]

    try:
        Count = int(message.text.split(maxsplit=2)[2])
        if Count <= 0:
            await message.reply_text("Норм так математика")
            return
    except:
        Count = 5000

    await message.delete()
    if command == "start":
        Data.DuelCount[message.chat.id] = Count
        Data.CanDuel = True
        await message.reply_text(f"Дуэль включена на {Count} боев")
    elif command == "stop":
        Data.CanDuel = False
        Data.DuelCount[message.chat.id] = 0
    else:
        await message.reply_text("Unknown command")


@app.on_message(filters.text & filters.reply)
async def Duel(client, message):
    if message.text.lower() == "дуэль принять":
        Data.DuelCount[message.chat.id] -= 1

        Oldmessage = await app.get_messages(message.chat.id, reply_to_message_ids=message.message_id)
        if Oldmessage.from_user.is_self and Data.CanDuel:
            await asyncio.sleep(10)
            if Data.DuelCount[message.chat.id] <= 0:
                msg = await message.reply_text("Count истёк")
                await Trigger(client, msg)
            else:
                await message.reply_text("Реанимировать жабу", quote=False)
                await message.reply_text("дуэль", quote=True)

@app.on_message(filters.command("craft", prefixes=".") & filters.me)
async def echo(_, message):
    await message.delete()
    await message.reply_text('Скрафтить клюв цапли')
    await message.reply_text('Скрафтить букашкомет')
    await message.reply_text('Скрафтить наголовник из клюва цапли')
    await message.reply_text('Скрафтить нагрудник из клюва цапли')
    await message.reply_text('Скрафтить налапники из клюва цапли')

@app.on_message(filters.command("echo", prefixes=".") & filters.me)
async def echo(_, msg):
    count = int(0)
    orig_text = msg.text.split(maxsplit=2)[2]
    max = int(msg.text.split(maxsplit=2)[1])

    await msg.delete()
    while (int(max) != int(count)) and (int(max) <= 100) and (int(max) > 0):
        await app.send_message(msg.chat.id, orig_text)
        count += 1


@app.on_message(filters.me & filters.command("convert", prefixes="."))
async def Convert(client, message):
    kit = int(message.text.split(maxsplit=2)[1])
    lvl = int(message.text.split(maxsplit=2)[2])

    await message.delete()
    await message.reply_text(f"с {lvl} уровня {kit} аптечек дадут тебе {str(await ConvertMethod(kit, lvl))} уровней")

@app.on_message(filters.media | filters.text)
async def Trigger(client, message):
    if message.media:
        try:
            text = message.caption.lower()
        except:
            return
    else:
        text = message.text.lower()

    if text in Data.Triggers:
        if Data.Triggers[text].get('chat') == message.chat.id:
            msg = await message.reply_text(Data.Triggers[text].get('text'), quote=True)
            await Trigger(client, msg)


async def ConvertMethod(kit, lvl, countOfLvl = 0):
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

    return await ConvertMethod(kit, lvl, countOfLvl)

app.run()
