import sys
sys.path.append('..')

from time import time
import random

from bhbot.models import Command
from bhbot.members import members
from bhbot.lang import get_phrase


class PseudoListCommand(Command):
    @property
    def triggers(self):
        return ['list', 'список']
    def __call__(self, context: dict) -> str:
        if len(context['args']) < 1:
            return get_phrase('NOT_ENOUGH_ARGUMENTS')
        random.seed(time())
        attempts = 0
        selected = []
        while len(selected) < random.randint(1, min(5, len(members))) and attempts < 5:
            member = random.choice(members)
            if member not in selected:
                selected.append(member)
            else:
                attempts += 1
            
        return 'Список {}:\n{}'.format(' '.join(context['args']), '\n'.join(selected))


def get_command():
    return PseudoListCommand
