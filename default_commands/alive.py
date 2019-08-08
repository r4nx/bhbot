import sys
sys.path.append('..')

from models import Command


class AliveCommand(Command):
    @property
    def triggers(self):
        return ['alive']
    def __call__(self, context: dict) -> str:
        return 'Yes, I am alive.'


def get_command():
    return AliveCommand
