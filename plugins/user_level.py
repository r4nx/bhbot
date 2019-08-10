import json
import logging
import os
import math
from collections import defaultdict
from functools import partial
from time import time

import telebot

logger = logging.getLogger('bhbot')
here = os.path.abspath(os.path.dirname(__file__))
get_path = partial(os.path.join, here)

AVERAGE_LENGTH = 20.0
CONTENT_EXPERIENCE = {
    'text': 4.0,
    'sticker': 2.0,
    'voice': 2.0
}
MIN_MESSAGES_INTERVAL = 4
SAVING_INTERVAL = 60 * 5  # 5 minutes
MAX_CACHE_AGE = 60 * 30  # 30 minutes
DATA_FILE = get_path('experience.json')

experience = defaultdict(dict)
name_cache = {}
last_messages = defaultdict(dict)
last_save = time()
bot = None


def level_handler(msg):
    # Flood protection
    last_message = last_messages[msg.chat.id].get(msg.from_user.id)
    if last_message is not None and time() - last_message < MIN_MESSAGES_INTERVAL:
        logger.info('Too fast, not counted')
        return
    last_messages[msg.chat.id][msg.from_user.id] = time()

    logger.info('Content type: ' + msg.content_type)
    logger.info('Score for such content type: ' + str(CONTENT_EXPERIENCE[msg.content_type]))
    logger.info('Length modifier: ' + str(min(len(msg.text) / AVERAGE_LENGTH, 2) if msg.content_type == 'text' else 1))
    score = CONTENT_EXPERIENCE[msg.content_type] * \
        (min(len(msg.text) / AVERAGE_LENGTH, 1.5) if msg.content_type == 'text' else 1)

    chat_id, user_id = str(msg.chat.id), str(msg.from_user.id)

    experience[chat_id][user_id] = experience[chat_id].get(user_id, 0) + score
    logger.info('Added {} score to {}'.format(score, msg.from_user.first_name))

    # Saving the data periodically
    global last_save
    if time() - last_save >= SAVING_INTERVAL:
        with open(DATA_FILE, 'w') as f:
            json.dump(dict(experience), f)
        last_save = time()
        logger.info('Saved experience')
    logger.info('')


def command_handler(msg):
    chat_id = str(msg.chat.id)
    users_exp = experience[chat_id]
    exp_list = []
    for user_id, exp in sorted(users_exp.items(), key=lambda x: x[1], reverse=True):
        level = int(math.floor(25 + math.sqrt(625 + 100 * exp)) / 50)
        next_level_exp = 25 * level * (1 + level)
        try:
            exp_list.append('{:16.16} - {:d} [{:.0f} / {:.0f}]'.format(
                get_name(user_id), level, exp, next_level_exp)
            )
        except telebot.apihelper.ApiException:
            logging.warning('User not found: {}'.format(user_id))
    bot.send_message(msg.chat.id, 'Level:\n    ' + '\n    '.join(exp_list))


def get_name(user_id):
    if user_id not in name_cache or time() - name_cache[user_id][1] > MAX_CACHE_AGE:
        name_cache[user_id] = bot.get_chat(user_id).first_name, time()
        logger.info('{} was not found in cache, maked request to Telegram API'.format(name_cache[user_id]))
    else:
        logger.info('{} was already in cache'.format(name_cache[user_id]))
    return name_cache[user_id][0]


def setup(tb):
    try:
        with open(DATA_FILE, 'r') as f:
            global experience
            experience = defaultdict(dict, json.load(f))
            logger.info('Loaded experience:\b' + str(experience))
    except FileNotFoundError:
        logging.info('Experience file not found')
    except JSONDecodeError:
        logging.exception('Failed to decode experience file')

    global bot
    bot = tb

    tb.message_handler(
        content_types=['text'],
        func=lambda msg: msg.text == '>toplvl' and \
            msg.chat.type in ('group', 'supergroup') and \
            msg.forward_date is None
    )(command_handler)

    tb.message_handler(
        content_types=CONTENT_EXPERIENCE.keys(),
        func=lambda msg: msg.chat.type in ('group', 'supergroup')
    )(level_handler)
