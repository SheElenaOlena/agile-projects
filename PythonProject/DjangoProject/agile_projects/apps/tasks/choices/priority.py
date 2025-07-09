from enum import Enum


class Priority(Enum):
    VERY_LOW =( 1,'VERY_LOW')
    LOW = (2,'LOW')
    MEDIUM = (3, 'MEDIUM')
    HIGH = (4, 'HIGH')
    CRITICAL = (5, 'CRITICAL')


    @classmethod
    def choices(cls):
        return [(key.value[0], key.value[1]) for key in cls]

    def __getitem__(self, item):
        # позволяет обращаться к элементу Enum как к списку или словарю
        return self.value[item]




