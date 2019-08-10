import random
import sys
sys.path.append('..')
from time import time
from datetime import datetime, timedelta

from bhbot.models import Command
from bhbot.lang import get_phrase


class WhenCommand(Command):
    @property
    def triggers(self):
        return ['when', 'когда']

    def __call__(self, context: dict) -> str:
        if len(context['args']) < 1:
            return get_phrase('NOT_ENOUGH_ARGUMENTS')

        random.seed(time())
        now = datetime.now()
        return (now + timedelta(days=random.randint(0, 500))).strftime('%d.%m.%Y') + \
            ' ' + ' '.join(context['args'])


def get_command():
    return WhenCommand
