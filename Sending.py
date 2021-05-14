import threading


class Work:

    def __init__(self):
        self.workSleep = threading.Event()

        self.IsWorking = False

    def Working(self, message, text):
        workSleep = self.workSleep

        if not self.IsWorking:
            self.IsWorking = True
            while not workSleep.is_set():
                message.reply_text("Выйти из подземелья", quote=False)
                message.reply_text("Реанимировать жабу", quote=False)
                message.reply_text(text, quote=False)
                workSleep.wait(7210) # 7200
                message.reply_text("Завершить работу", quote=False)
                workSleep.wait(21610) # 21600
            message.reply_text("Работа завершена", quote=False)
            self.IsWorking = False
        else:
            message.reply_text("Is Working")


class Eat:

    def __init__(self):
        self.eatSleep = threading.Event()

        self.IsEating = False

    def Eating(self, message, text):
        eatSleep = self.eatSleep

        if not self.IsEating:
            self.IsEating = True
            while not eatSleep.is_set():
                message.reply_text(text, quote=False)
                if text.lower() == "откормить жабу":
                    eatSleep.wait(14410) #14400
                elif text.lower() == "покормить жабу":
                    eatSleep.wait(43210) #43200
            message.reply_text("Кормка завершена", quote=False)
            self.IsEating = False
        else:
            message.reply_text("Is Eating")
