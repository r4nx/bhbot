import sys
sys.path.append('..')

from time import time
import random

from models import Command

members = (
    'kewa',
    'ranx',
    'книга',
    'FYP',
    'imring',
    'molimawka',
    'randazzo',
    'memir'
)


class PseudoListCommand(Command):
    def __call__(self, context: dict) -> str:
        if len(context['args']) < 1:
            return 'Недостаточно аргументов.'
        random.seed(time())
        return 'Список {}:\n{}'.format(' '.join(context['args']), '\n'.join(random.choices(members, k=random.randint(1,  5 if len(members) > 5 else len(members)))))
