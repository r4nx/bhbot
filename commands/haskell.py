import logging
import sys
sys.path.append('..')

from bhbot.models import Command
from bhbot.lang import get_phrase

import requests

logger = logging.getLogger('bhbot')
INTERPRETER_URL = 'https://tryhaskell.org/eval'


class HaskellCommand(Command):
    @property
    def triggers(self):
        return ['haskell', 'hs']

    def __call__(self, context: dict) -> str:
        if len(context['args']) < 1:
            return get_phrase('NOT_ENOUGH_ARGUMENTS')

        exp = ' '.join(context['args'])
        try:
            resp = requests.post(INTERPRETER_URL, data={'exp': exp}).json()
        except requests.RequestException:
            logger.exception('Error occured while sending request to Haskell interpreter.')
            return 'Произошла ошибка при отправке запроса.'
        except ValueError:
            return 'Произошла ошибка при декодировании ответа сервера.'
        else:
            success = resp.get('success')
            if success is not None:
                stdout = success.get('stdout')
                output = '\n'.join(line.strip() for line in stdout) if type(stdout) == list else '// No output provided'

                value = success.get('value', '// No value provided')

                return 'Output:\n{}\n\nValue:\n{}'.format(output, value)
            elif 'error' in resp:
                return 'Error:\n{}'.format(resp['error'])
            else:
                return 'Сервер вернул некорректный ответ.'


def get_command():
    return HaskellCommand
