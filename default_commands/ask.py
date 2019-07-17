import sys
sys.path.append('..')

from time import time
import random

from models import Command

from Levenshtein import distance


class AskCommand(Command):
    def __call__(self, context: dict) -> str:
        if len(context['args']) < 1:
            return 'Недостаточно аргументов.'
        
        question = ' '.join(context['args'])

        if distance('что делать', question.lower()) < 6:
            return 'муравью хуй приделать'

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
