from abc import ABC, abstractmethod
from typing import Iterable, Optional

from lang import get_phrase


class Command(ABC):
    @property
    @abstractmethod
    def triggers(self):
        pass

    @abstractmethod
    def __call__(self, context: dict) -> str:
        pass

    def setup(self, dispatcher):
        dispatcher.register_command(self.__class__())


class CommandDispatcher():
    def __init__(self):
        self.commands = {}

    def register_command(self, cmd: Command) -> None:
        self.commands.update({trigger: cmd for trigger in cmd.triggers})

    def dispatch(self, text: str, context: dict) -> Optional[str]:
        args = text.split(' ')
        if len(args) < 1:
            return get_phrase('EMPTY_CMD')
        try:
            cmd = self.commands[args[0]]
        except KeyError:
            return get_phrase('CMD_NOT_FOUND')
        else:
            context['trigger'] = args[0]
            context['args'] = args[1:]  # Trimming command name
            return cmd(context)
