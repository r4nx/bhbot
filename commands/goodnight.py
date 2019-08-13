import sys
sys.path.append('..')

from bhbot.models import Command


class GoodNightCommand(Command):
    @property
    def triggers(self):
        return ['spok', 'спок']

    def __call__(self, context: dict) -> str:
        return 'Всем спокойной ночи и сладких снов!'


def get_command():
    return GoodNightCommand
