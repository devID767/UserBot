import json

def saveArray(filename, dict):
    with open(filename, 'w') as f:
        json.dump(dict, f)

def loadArray(filename):
    with open(filename, 'r') as f:
        return json.load(f)

def saveArrayEncoder(filename, dict):
    with open(filename, 'w') as f:
        json.dump(dict, f, cls=Encoder)

Works = {}

Eats = {}

CanDuel = False
DuelCount = {}

class Trigger:
    def __init__(self, text, chat, boss, **kwargs):
        self.key = text
        self.text = text
        self.chat = chat
        self.boss = boss
        self.attribute = kwargs or None

    def get(self, key):
        if key == 'text':
            return self.text
        elif key == 'chat':
            return self.chat

class Encoder(json.JSONEncoder):
    def default(self, obj):
        return obj.__dict__

Triggers = loadArray("Triggers")
saveArrayEncoder("Triggers", Triggers)

def newTrigger(key, valueText, valueChat, boss = 0):
    global Triggers
    Triggers[key] = Trigger(valueText, valueChat, boss)
    saveTriggers()

def saveTriggers():
    global Triggers
    saveArrayEncoder("Triggers", Triggers)
    Triggers = loadArray("Triggers")

class TimerState:
    def __init__(self, text, time, typeOfTime, chat, **kwargs):
        self.text = text
        self.time = time
        self.typeOfTime = typeOfTime
        self.chat = chat

        self.is_started = False

        self.title = f"{text} : {time} : {typeOfTime}\n"

        self.attribute = kwargs or None

    def get(self, key):
        if key == 'text':
            return self.text
        elif key == 'time':
            return self.time
        elif key == 'typeOfTime':
            return self.typeOfTime
        elif key == 'is_started':
            return self.is_started
        elif key == 'title':
            return self.title
        elif key == 'chat':
            return self.chat

Timers = []
TimersState = loadArray("Timers")
saveArrayEncoder("Timers", TimersState)

def newTimerState(timer):
    global TimersState
    TimersState.append(timer)
    saveTimersState()

def saveTimersState():
    global TimersState
    saveArrayEncoder("Timers", TimersState)
    TimersState = loadArray("Timers")
