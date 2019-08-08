from time import time
import random
import sys
sys.path.append('..')

from models import Command


class OrCommand(Command):
    @property
    def triggers(self):
        return ['or', 'или']
    def __call__(self, context: dict) -> str:
        if len(context['args']) < 1:
            return 'Недостаточно аргументов.'

        text = ' '.join(context['args'])
        variants = text.split('или')
        if len(variants) < 2:
            return 'Недостаточно вариантов.'

        random.seed(time())
        return random.choice(variants).strip()


def get_command():
    return OrCommand
