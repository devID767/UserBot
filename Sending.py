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
                workSleep.wait(5) # 7200
                message.reply_text("Завершить работу", quote=False)
                workSleep.wait(10) # 21600
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
                if text.lower() == "Откормить жабу":
                    eatSleep.wait(5) #14400
                else:
                    eatSleep.wait(5) #43200
            message.reply_text("Кормка завершена", quote=False)
            self.IsEating = False
        else:
            message.reply_text("Is Eating")
