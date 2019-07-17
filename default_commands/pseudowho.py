import sys
sys.path.append('..')

from time import time
import random

from models import Command


class PseudoWhoCommand(Command):
    def __call__(self, context: dict) -> str:
        if len(context['args']) < 1:
            return 'Недостаточно аргументов.'
        random.seed(time())
        return random.choice([
            'kewa',
            'ranx',
            'книга',
            'FYP',
            'imring',
            'molimawka',
            'randazzo',
            'memir'
        ]) + ' ' + ' '.join(context['args'])
