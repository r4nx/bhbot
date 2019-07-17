import sys
sys.path.append('..')

from time import time
import random

from models import Command


class EvgenSimulatorCommand(Command):
    def __call__(self, context: dict) -> str:
        if len(context['args']) < 1:
            return 'Недостаточно аргументов.'
        evgen_templates = [
            'эмм\n{}',
            '{} как бы'
        ]
        random.seed(time())
        return random.choice(evgen_templates).format(' '.join(context['args']))
