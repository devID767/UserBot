import json

def saveArray(filename, dict):
    with open(filename, 'w') as f:
        json.dump(dict, f)

def loadArray(filename, Isdict = True):
    try:
        with open(filename, 'r') as f:
            return json.load(f)
    except:
        if Isdict:
            return {}
        else:
            return []

def saveArrayEncoder(filename, dict, encoder):
    with open(filename, 'w') as f:
        json.dump(dict, f, cls=encoder)

def loadArrayEncoder(filename):
        with open(filename, 'r') as f:
            return json.load(f)

Works = {}

Eats = {}

CanDuel = False
DuelCount = {}

class Trigger:
    def __init__(self, text, chat, **kwargs):
        self.key = text
        self.text = text
        self.chat = chat
        self.attribute = kwargs or None
    def get(self, key):
        if key == 'text':
            return self.text
        elif key == 'chat':
            return self.chat

class TriggersEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Trigger):
            return obj.__dict__
        return json.JSONEncoder.default(self, obj)

Triggers = loadArray("Triggers")
saveArrayEncoder("Triggers", Triggers, TriggersEncoder)

def newTrigger(key, valueText, valueChat):
    Triggers[key] = Trigger(valueText, valueChat)
    saveArrayEncoder("Triggers", Triggers, TriggersEncoder)

def saveTriggers():
    saveArrayEncoder("Triggers", Triggers, TriggersEncoder)

Timers = []
saveArray("Timers", Timers)
Timers = loadArray("Timers")