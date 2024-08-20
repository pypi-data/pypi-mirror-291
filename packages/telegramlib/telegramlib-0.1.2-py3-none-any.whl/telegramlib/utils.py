"""
Utility Module

This module provides utility functions.
"""
import emoji
from .config import config
from .firma import morpheus_typing, sleep_lock, set_cursor_visibility_to
import random
from time import sleep
import getpass
from telegram.constants import ParseMode  # <s>strikethrough</s>  <u>underlined</u>  <i>italics</i>  <b>bold</b>
import requests

__all__ = ['emoji_in', '_firma']

def emoji_in(text):
    """
    Tells whether a given text contains emojis or not.

    Parameters
    ----------
    text : str
        Text message to check

    Returns
    -------
    bool
        `True` if text contains emojis, `False` otherwise
    """
    for character in text:
        if character in emoji.UNICODE_EMOJI['en']:
            return True
    return False

def _firma(p = 80, t1 = 4, t2 = 4):
    neo = getpass.getuser().title()
    if config._admin in config._data and config._data[config._admin]['info']:
        info = list(config._data[config._admin]['info'].values())[-1]
        if 'first_name' in info:
            neo = info['first_name']
        elif 'username' in info:
            neo = info['username']

    def _morpheus_typing(monito):
        morpheus_typing(monito, reactivate_cursor = False)

    def _send(message):
        url = f'https://api.telegram.org/bot{config._token}/sendMessage?chat_id={config._admin}&parse_mode={ParseMode.HTML}&text={message}'
        return requests.get(url).json()

    m = []
    for contactme in [_morpheus_typing, _send]:
        if random.randrange(p) == 0:
            sleep_lock(t1)
            m.append(contactme('Wake up ' + neo + '...'))
            sleep_lock(t2)
            t1 = 0
        if random.randrange(p) == 0:
            sleep_lock(t1)
            m.append(contactme('The Matrix has you...'))
            sleep_lock(t2)
            t1 = 0
        if random.randrange(p) == 0:
            sleep_lock(t1)
            m.append(contactme('Follow the white rabbit.'))
            sleep_lock(t2)
            t1 = 0
        if random.randrange(p) == 0:
            sleep_lock(t1)
            m.append(contactme('Knock, knock, ' + neo + '.'))
            sleep_lock(t2)
        set_cursor_visibility_to(True)
    config._message_to_delete_in_init = [ [ i['result']['chat']['id'], i['result']['message_id'] ] for i in m if i ]