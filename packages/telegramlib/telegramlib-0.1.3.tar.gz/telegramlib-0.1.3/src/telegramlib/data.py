"""
Data Management Module

This module provides functions for managing user-specific parameters and retrieving chat history
within a Telegram bot environment. It allows you to set and get custom parameters for users
as well as access and format their chat history according to various criteria.
"""

from .config import config, _bot_started_check
import warnings
from .telegram_warnings import NonExistentParameterWarning

__all__ = ['set_param', 'get_param', 'get_chat']

@_bot_started_check
def set_param(key, value):
    """
    Set the value of a user custom parameter.

    Parameters
    ----------
    key : any
        The key name of the parameter to be set. It must be one of the keys in the default parameter dictionary.
    value : any
        The value to be associated with the key.
    """
    if key not in config._data[config._user_id] or key in config._system_params:
        warnings.warn(NonExistentParameterWarning(key))
        return
    config._data[config._user_id][key] = value

@_bot_started_check
def get_param(key):
    """
    Get the value of a user custom parameter.

    Parameters
    ----------
    key : any
        The key name of the parameter whose value you want to get. It must be one of the keys in the default parameter dictionary.

    Returns
    -------
    any
        The value associated with the key name parameter.
    """
    if key not in config._data[config._user_id] or key in config._system_params:
        warnings.warn(NonExistentParameterWarning(key))
        return
    return config._data[config._user_id][key]

@_bot_started_check
def get_chat(user = None, last = None, last_message = None, max_char = None, to_string = False, to_list = False, only_name_keys = False, without_keys = False):
    """
    Get the chat history of a user.

    Parameters
    ----------
    user : int or str or None, optional
        user_id of the user whose chat to get or `None` (default) to use `config._user_id`.
    last : int or str or None, optional
        Number of last messages or last `"day"`, `"month"`, or `"year"` time frame (default is `None`).
    last_message : str, optional
        Last message of which you want to get the next ones (default is `None`).
    max_char : int, optional
        Maximum number of characters to be obtained (default is `None`).
    to_string : bool, optional
        `True` to return the chat in string format (default is `False`).
    to_list : bool, optional
        `True` to return the chat in list format (default is `False`).
    only_name_keys : bool, optional
        `True` to return chat with keys containing only names (default is `False`).
    without_keys : bool, optional
        `True` to return the chat with only message contents (default is `False`).

    Returns
    -------
    dict or str or list
        The user's chat in the specified format.
    """
    if user is None:
        user = config._user_id
    if user not in config._data:
        return
    
    def add_start_dict(d, d0):
        d0.update(d)
        return d0

    def flatten_dict(d, parent_key='', sep='_'):
        items = []
        for k, v in d.items():
            new_key = f"{parent_key}{sep}{k}" if parent_key else k
            if isinstance(v, dict):
                items.extend(flatten_dict(v, new_key, sep=sep).items())
            else:
                items.append((new_key, v))
        return dict(items)

    def unflatten_dict(flat_dict, sep='_'):
        nested_dict = {}
        for flat_key, value in flat_dict.items():
            keys = flat_key.split(sep)
            d = nested_dict
            for key in keys[:-1]:
                if int(key) not in d:
                    d[int(key)] = {}
                d = d[int(key)]
            d[keys[-1]] = value
        return nested_dict

    chat = config._data[user]['chat'].copy()

    if last == 'day':
        chat = list( list( list( chat.values() )[-1].values() )[-1].values() )[-1]
    elif last == 'month':
        chat = list( list( chat.values() )[-1].values() )[-1]
    elif last == 'year':
        chat = list( chat.values() )[-1]

    l, s, d, items = [], '', {}, []
    n_line = n_char = 0
    for key, value in reversed(flatten_dict(chat).items()):
        n_line += 1
        n_char += len( key.split('_[')[-1] + value ) + 1
        if value == last_message or (isinstance(last, int) and n_line > last) or (max_char is not None and n_char > max_char):
            break
            
        if only_name_keys:
            key = key.split(')')[-1]
        elif without_keys:
            key = ''

        if not to_list and not to_string:
            if only_name_keys or without_keys:
                items.insert(0, (key, value))
            else:
                d = add_start_dict(d, {key: value})

        if not without_keys:
            key += ': '

        if to_list:
            l.insert(0, key + value)
        elif to_string:
            s = '\n' + key + value + s

    if to_list:
        return l
    if to_string:
        return s[1:]
    if only_name_keys or without_keys:
        return items
    return unflatten_dict(d)