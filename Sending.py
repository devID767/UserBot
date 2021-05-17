import asyncio

class Work:
    def __init__(self):
        self.is_started = False
        self._task = None

    async def Start(self, message, text):
        if not self.is_started:
            self.is_started = True
            self._task = asyncio.ensure_future(self._Working(message, text))

    async def Stop(self):
        if self.is_started:
            self.is_started = False
            self._task.cancel()

    async def _Working(self, message, text):
        while True:
            await message.reply_text("Выйти из подземелья", quote=False)
            await message.reply_text("Реанимировать жабу", quote=False)
            await message.reply_text(text, quote=False)
            await asyncio.sleep(5)  # 7200

            await message.reply_text("Завершить работу", quote=False)
            await asyncio.sleep(3)  # 21600

class Eat:
    def __init__(self):
        self.is_started = False
        self._task = None

    async def Start(self, message, text):
        if not self.is_started:
            self.is_started = True
            self._task = asyncio.ensure_future(self._Eating(message, text))
        else:
            await message.reply_text("Жаба уже кушает!", quote=False)


    async def Stop(self):
        if self.is_started:
            self.is_started = False
            self._task.cancel()

    async def _Eating(self, message, text):
        while True:
            await message.reply_text(text, quote=False)
            if text.lower() == "откормить жабу":
                await asyncio.sleep(5) #14400
            elif text.lower() == "покормить жабу":
                await asyncio.sleep(10) #43200


class Customise:
    def __init__(self, text, time, chat):
        self.text = text
        self.time = time
        self.chat = chat

        self.is_started = False
        self._task = None

    async def Start(self, message):
        if not self.is_started:
            self.is_started = True
            self._task = asyncio.ensure_future(self._Sending(message))

    async def Stop(self):
        if self.is_started:
            self.is_started = False
            self._task.cancel()

    async def _Sending(self, message):
        while True:
            await message.reply_text(self.text, quote=False)
            await asyncio.sleep(self.time)

class Periodic:
    def __init__(self, func, time):
        self.func = func
        self.time = time
        self.is_started = False
        self._task = None

    async def start(self):
        if not self.is_started:
            self.is_started = True
            # Start task to call func periodically:
            self._task = asyncio.ensure_future(self._run())

    async def stop(self):
        if self.is_started:
            self.is_started = False
            # Stop task and await it stopped:
            self._task.cancel()

    async def _run(self):
        while True:
            await asyncio.sleep(self.time)
            self.func()