import sys
sys.path.append('..')

from models import Command


class RulesCommand(Command):
    def __call__(self, context: dict) -> str:
        return 'Не срать, не оскорблять, не троллить. Всё.'
