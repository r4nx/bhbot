import sys
sys.path.append('..')

from bhbot.models import Command


class MorningCommand(Command):
    @property
    def triggers(self):
        return ['morning', 'utro', 'ytro', 'утро']

    def __call__(self, context: dict) -> str:
        return 'Всем доброго утра и хорошего дня!'


def get_command():
    return MorningCommand
