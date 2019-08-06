from time import time
import random
import sys
sys.path.append('..')

from models import Command

members_nominative = (
    'кеша',
    'ранкс',
    'книга',
    'фип',
    'имринг',
    'молимашка',
    'рандаззо',
    'мемир'
)

members_dative = (
    'кеше',
    'ранксу',
    'книге',
    'фипу',
    'имрингу',
    'молимашке'
    'рандаззо',
    'мемиру'
)

members_genetive = (
    'кешу',
    'ранкса',
    'книгу',
    'фипа',
    'имринга',
    'молимашку',
    'рандаззо',
    'мемира'
)


class PseudoWhoCommand(Command):
    def __call__(self, context: dict) -> str:
        if len(context['args']) < 1:
            return 'Недостаточно аргументов.'

        members = {
            'кому': members_dative,
            'кого': members_genetive
        }.get(context['trigger'].lower(), members_nominative)

        random.seed(time())
        return random.choice(members) + ' ' + ' '.join(context['args'])
