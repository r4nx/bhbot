from time import time
import random
import sys
sys.path.append('..')

from bhbot.models import Command


class PercentCommand(Command):
    @property
    def triggers(self):
        return ['percent', 'процент', 'проц']
    def __call__(self, context: dict) -> str:
        if len(context['args']) < 1:
            return 'Недостаточно аргументов.'

        random.seed(time())
        return '{:d}% {}'.format(random.randint(0, 100), ' '.join(context['args']))


def get_command():
    return PercentCommand
