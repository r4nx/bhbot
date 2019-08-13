from time import time
import random
import sys
sys.path.append('..')

from bhbot.models import Command
from bhbot.lang import get_phrase


class OrCommand(Command):
    @property
    def triggers(self):
        return ['or', 'или']

    def __call__(self, context: dict) -> str:
        if len(context['args']) < 1:
            return get_phrase('NOT_ENOUGH_ARGUMENTS')

        text = ' '.join(context['args'])
        variants = [variant.strip() for variant in text.split('или')]
        variants = list(filter(lambda variant: len(variant) > 0, variants))

        if len(variants) < 2:
            return 'Недостаточно вариантов.'

        random.seed(time())
        return random.choice(variants)


def get_command():
    return OrCommand
