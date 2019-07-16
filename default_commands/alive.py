import sys
sys.path.append('..')

from models import Command


class AliveCommand(Command):
    def __call__(self, context: dict) -> str:
        return 'Yes, I am alive.'
