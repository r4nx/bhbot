from time import time
import random
import sys
sys.path.append('..')

from bhbot.models import Command


class HowMuchCommand(Command):
    @property
    def triggers(self):
        return ['howmuch', 'сколько']
    def __call__(self, context: dict) -> str:
        if len(context['args']) < 1:
            return 'Недостаточно аргументов.'

        random.seed(time())
        return str(random.randint(0, 10000)) + ' ' + ' '.join(context['args'])


def get_command():
    return HowMuchCommand
