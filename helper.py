from dataclasses import dataclass
import datetime

items = []


@dataclass
class Item:
    text: str
    date: datetime
    isCompleted: bool = False

# Speichern der Daten
# b zu bbb
def add(text, date):
    text = text.replace('b', 'bbb').replace('B', 'Bbb')
    items.append(Item(text, datetime.date.fromisoformat(date)))


def get_all():
    return items


def get(index):
    return items[index] 


def update(index):
    items[index].isCompleted = not items[index].isCompleted
