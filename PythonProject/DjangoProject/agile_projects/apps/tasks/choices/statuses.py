from enum import Enum


class Statuses(Enum):
    NEW = 'NEW'
    IN_PROGRESS = 'IN_PROGRESS'
    PENDING = 'PENDING'
    BLOCKED = 'BLOCKED'
    TESTING = 'TESTING'
    CLOSED = 'CLOSED'

    @classmethod
    # метод относится ко всему классу, а не к конкретному объекту.
    # def choices(cls) — создаётся метод choices, где cls — это сам Enum-класс (Statuses например).
    # return [(attr.name, attr.value) for attr in cls] — здесь цикл перебирает все элементы
    # перечисления Enum и формирует список кортежей
    def choices(cls):
        return [(attr.name, attr.value) for attr in cls]



