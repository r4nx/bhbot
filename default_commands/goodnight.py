import sys
sys.path.append('..')

from models import Command


class GoodNightCommand(Command):
    def __call__(self, context: dict) -> str:
        return 'Всем спокойной ночи и сладких снов!'
