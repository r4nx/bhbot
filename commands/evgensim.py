import sys
sys.path.append('..')

from time import time
import random

from bhbot.models import Command


class EvgenSimulatorCommand(Command):
    @property
    def triggers(self):
        return ['evgensim', 'evgen1137', 'евген']
    def __call__(self, context: dict) -> str:
        if len(context['args']) < 1:
            return 'Недостаточно аргументов.'
        evgen_templates = [
            'эмм\n{}',
            '{} как бы'
        ]
        random.seed(time())
        return random.choice(evgen_templates).format(' '.join(context['args']))


def get_command():
    return EvgenSimulatorCommand
