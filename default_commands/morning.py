import sys
sys.path.append('..')

from models import Command


class MorningCommand(Command):
    def __call__(self, context: dict) -> str:
        return 'Всем доброго утра и хорошего дня!'
