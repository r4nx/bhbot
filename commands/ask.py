import sys
sys.path.append('..')

from time import time
import random

from bhbot.models import Command
from bhbot.lang import get_phrase


class AskCommand(Command):
    @property
    def triggers(self):
        return ['ask', 'спрос']
    def __call__(self, context: dict) -> str:
        if len(context['args']) < 1:
            return get_phrase('NOT_ENOUGH_ARGUMENTS')
        
        question = ' '.join(context['args'])

        random.seed(time())

        if ' фп ' in (' ' + question):
            return random.choice((
                'приличные люди такое не спрашивают',
                'ты че говнарь такое спрашивать',
                'не туда воюешь дебил',
                'слыш ты ахуел',
                'мда',
                'еблан?'
            ))

        return random.choice(('Да', 'Нет'))


def get_command():
    return AskCommand
