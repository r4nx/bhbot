from abc import ABC, abstractmethod
from typing import Iterable, Optional

from lang import get_phrase


class Command(ABC):
    def __init__(self, triggers: Iterable[str]):
        self.triggers = triggers

    @abstractmethod
    def __call__(self, context: dict) -> str:
        pass


class CommandDispatcher():
    def __init__(self):
        self.commands = {}

    def register_command(self, cmd: Command) -> None:
        self.commands.update({trigger: cmd for trigger in cmd.triggers})
        print('commands triggers: {}'.format(' '.join(self.commands.keys())))

    def dispatch(self, text: str, context: dict) -> Optional[str]:
        print('dispatching text {}'.format(text))
        args = text.split(' ')
        if len(args) < 1:
            return get_phrase('EMPTY_CMD')
        print('arg 0 {}'.format(args[0]))
        try:
            cmd = self.commands[args[0]]
        except KeyError:
            return get_phrase('CMD_NOT_FOUND')
        else:
            context['args'] = args[1:]  # Trimming command name
            return cmd(context)
