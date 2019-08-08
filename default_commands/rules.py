import sys
sys.path.append('..')

from models import Command


class RulesCommand(Command):
    @property
    def triggers(self):
        return ['rules', 'правила']
    def __call__(self, context: dict) -> str:
        return 'Не срать, не оскорблять, не троллить. Всё.'


def get_command():
    return RulesCommand
