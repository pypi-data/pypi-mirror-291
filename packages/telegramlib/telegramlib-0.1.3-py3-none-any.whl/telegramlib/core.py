"""
Telegram Bot Main Functionality Module

This module provides core functionality for managing a Telegram bot, including bot startup, message handling,
error handling, and user data management. It incorporates Telegram bot handlers, decorators, and utility functions
to facilitate the smooth operation of the bot.
"""

from typing import Callable
from .config import config, context, update, bot_name, _bot_started_check
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
from .telegram_exceptions import MissingStartCommandError
from datetime import time, datetime, timedelta
import pytz
from .jobs import _scheduled
from .utils import *
from unicodeit import replace
from .translator import translate, language_of
from .utils import emoji_in
from .text_to_speech import text_to_speech
import os
import warnings
from .telegram_warnings import TextToSpeechWarning
from telegram.constants import ParseMode  # <s>strikethrough</s>  <u>underlined</u>  <i>italics</i>  <b>bold</b>
import requests
import traceback
from colorama import Fore
import functools

__all__ = ['start_bot', 'command_args', 'bot_reply_text', 'send', 'delete']

def start_bot(
        token, admin,
        commands,
        messages = None,
        scheduled = None,
        error = None,
        controllers = None,
        params = None,
        privacy = True
    ):
    """
    Most important function needed to start the bot.

    Parameters
    ----------
    token : str
        Telegram bot token.
    admin : int or str
        Admin user_id.
    commands : Callable or list of Callable
        start function or list of command handler functions.
    messages : Callable or list of Callable or None, optional
        Message handler function or list of [function, telegram filter] (default is `None`).
    scheduled : Callable or list of Callable or None, optional
        Scheduled function/functions (default is `None`).
    error : Callable or None, optional
        Error handler function or `None` (default) to use default _error handler function.
    controllers : str or list of str or None, optional
        Controller user_id/user_ids (default is `None`).
    params : dict or None, optional
        Users' default parameters (default is `None`).
    privacy : bool, optional
        `False` to enable user tracking (default is `True`).
    Raises
    ------
    MissingStartCommandError
        If the function is executed before the bot starts.
    """

    config._token, config._admin, config._scheduled_functions, config._controllers, config._default_params, config._privacy = token, admin, scheduled, controllers, params, privacy

    application = ApplicationBuilder().token(config._token).build()

    if commands is not None:
        if callable(commands):
            commands = [commands]
        missing_start = True
        for command in commands:
            if command.__name__ == 'start':
                missing_start = False
            command_handler = CommandHandler(command.__name__, _telegram(command))
            application.add_handler(command_handler)
        if missing_start:
            raise MissingStartCommandError()
    else:
        raise MissingStartCommandError()
    
    async def usersupdates():
        if config._user_id in config._controllers:
            config._data[config._user_id]['usersupdates'] = not config._data[config._user_id]['usersupdates']
            if config._data[config._user_id]['usersupdates']:
                send('<b>You will receive updates on users.</b>', config._user_id)
            else:
                send('<b>You will no longer receive updates on users.</b>', config._user_id)
 
    command_handler = CommandHandler(usersupdates.__name__, _telegram(usersupdates))
    application.add_handler(command_handler)

    class NotCommandFilter(filters.BaseFilter):
        def not_command_filter(update):
            message_text = update.message.text
            is_not_command = True
            for command in commands:
                is_not_command = is_not_command and not message_text.startswith('/' + command.__name__)
            return is_not_command

    not_command_filter = NotCommandFilter()

    async def void_func():
        pass

    if messages is not None:
        if callable(messages):
            message_handler = MessageHandler(filters.TEXT & not_command_filter, _telegram(messages))
            application.add_handler(message_handler)
        else:
            for message in messages:
                message_handler = MessageHandler(message[1], _telegram(message[0]))
                application.add_handler(message_handler)
    else:
        message_handler = MessageHandler(not_command_filter, _telegram(void_func))
        application.add_handler(message_handler)
    

    if error is not None:
        application.add_error_handler(error)
    else:
        application.add_error_handler(_error)

    # Recreating work queues from database
    for chat_id, user in config._data.items():
        for job in user['jobs']:
            for func in config._scheduled_functions:
                if func.__name__ == job['function']:
                    target_time = time(hour = job['hour'], minute = job['minute']).replace(tzinfo = pytz.timezone('Europe/Berlin'))
                    application.job_queue.run_daily(_scheduled(func), time = target_time, chat_id = chat_id, name = str(chat_id))

    _firma()

    config._memorize()

    config._started_correctly = True

    send('<b>STARTED</b>', config._controllers)

    application.run_polling()

@_bot_started_check
def command_args():
    """
    Get command's arguments.

    Returns
    -------
    list of str or None
        Command's arguments.
    """
    if context() is not None and len(context().args) > 0:
        return context().args
    return None

@_bot_started_check
async def bot_reply_text(message, text_to_audio = False, translate_to = None, talking_about_latex = False):
    """
    Makes the bot respond to a message from the user. Must be executed with `await` in front.

    Parameters
    ----------
    message : str
        Bot response message.
    text_to_audio : bool, optional
        `True` to send the text as audio (default is `False`).
    translate_to : str or None, optional
        The language in which you want the message to arrive translated (default is `None`).
    talking_about_latex : bool, optional
        `True` if the message mentions latex formulas that do not need to be converted (default is `False`).
    """
    message = message.strip()

    message_latex = replace(message)    # convert Latex expressions to unicode

    if translate_to is not None:
        message = translate(message, dest = translate_to)
        message_latex = translate(message_latex, dest = translate_to)

    message_latex = message_latex.replace('−', '-')

    if text_to_audio and message == message_latex and 'http' not in message and not emoji_in(message):
        audio_file = config._path + 'audio'
        try:
            text_to_speech(message, file = audio_file, lang = language_of(message))
        except:
            text_to_speech(message, file = audio_file)
        message_id = await update().message.reply_audio(open(audio_file, 'rb'), title = 'audio')
        message_id = message_id.message_id
        _save_text_message_in_data(message, message_id, is_text_to_audio = True)
        os.remove(audio_file)
    else:

        if text_to_audio:
            warnings.warn(TextToSpeechWarning(message))
        if message == message_latex or talking_about_latex:
            if update() is not None:
                message_id = await update().message.reply_text(message)
            else:
                message_id = await context().bot.send_message(config._user_id, text = message)
            message_id = message_id.message_id
            _save_text_message_in_data(message, message_id)
        if message != message_latex:
            message_latex = message_latex.replace('$', '')
            if update() is not None:
                message_id = await update().message.reply_text(message_latex)
            else:
                message_id = await context().bot.send_message(config._user_id, text = message_latex)
            message_id = message_id.message_id
            _save_text_message_in_data(message_latex, message_id)

def send(message, chat_id = None, save = True, token = None, parse_mode = ParseMode.HTML):
    """
    Sends a text message to a specified user.

    Parameters
    ----------
    message : str
        Text message to send.
    chat_id : int or str or None, optional
        user_id of the recipient, `'all'` to send to all users in the database or `None` (default) to send to the admin.
    save : bool, optional
        `False` if you don't want to save the message in the database (default is `True`).
    token : str or None, optional
        Telegram bot token
    parse_mode : ParseMode, optional
        Text message parse mode (default is `ParseMode.HTML`).

    Returns
    -------
    dict or list of dict
        Response/responses of api requests.
    """
    def save_in_database(message, id, response):
        if save and response['ok']:
            message_id = response['result']['message_id']
            _save_text_message_in_data(message, message_id, id)
            config._memorize()

    if token is None:
        token = config._token
    if chat_id is None:
        chat_id = config._admin
    if chat_id == 'all':
        chat_id = list(config._data.keys())
        response = []
        for id in chat_id:
            url = f'https://api.telegram.org/bot{token}/sendMessage?chat_id={id}&parse_mode={parse_mode}&text={message}'
            response.append(requests.get(url).json())
            save_in_database(message, id, response[-1])
        return response
    elif isinstance(chat_id, list):
        response = []
        for id in chat_id:
            url = f'https://api.telegram.org/bot{token}/sendMessage?chat_id={id}&parse_mode={parse_mode}&text={message}'
            response.append(requests.get(url).json())
            if id in config._data:
                save_in_database(message, id, response[-1])
        return response
    else:
        url = f'https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&parse_mode={parse_mode}&text={message}'
        response = requests.get(url).json()
        if chat_id in config._data:
            save_in_database(message, chat_id, response)
        return response

def delete(chat_id, message_id, token = None):
    """
    Deletes a text message of a user.

    Parameters
    ----------
    chat_id : int or str
        user_id of the recipient.
    message_id : int or str
        message_id of the message to be deleted.
    token : str or None, optional
        Telegram bot token or `None` (default) to use token set during bot startup.

    Returns
    -------
    dict
        Response of api requests.
    """
    if token is None:
        token = config._token
    url = f'https://api.telegram.org/bot{token}/deleteMessage?chat_id={chat_id}&message_id={message_id}'
    return requests.get(url).json()

async def _error(update, context):
    """
    Default error handler.

    This function is private and should not be used directly by users of the package.

    Parameters
    ----------
    update : telegram.Update
        python-telgram-bot update object.
    context : telegram.Context
        python-telgram-bot context object.
    """
    tb = traceback.format_exception(None, context.error, context.error.__traceback__)
    print(Fore.RED + ''.join(tb) + Fore.RESET)
    send( f'<b>ERROR</b>: {config._who}\n{context.error}\n\n{tb[-2]}', [ c for c in config._controllers if c in config._data and config._data[c]['usersupdates'] ] )
    config._last_time = None

# decorator
def _telegram(func):
    """
    Main decorator applied to telegram message handler functions to configure and manage data.

    This decorator is private and should not be used directly by users of the package.

    Parameters
    ----------
    func : Callable
        Function to decorate.

    Returns
    -------
    Callable
        A modified function that includes configuration and management of data.
    """
    @functools.wraps(func)
    async def wrapper(*args):
        await _init(*args)
        if not config._data[config._user_id]['ban'] and (config._user_id not in config._creator_users or func.__name__ == 'closecreator'):
            await func()
        config._memorize()
        config._update = config._context = None
    return wrapper

async def _init(update, context):
    """
    Data management initialization and configuration function executed for each user message in _telegram decorator.

    This function is private and should not be used directly by users of the package.

    Parameters
    ----------
    update : telegram.Update
        python-telgram-bot update object.
    context : telegram.Context
        python-telgram-bot context object.
    """
    config._update, config._context = update, context

    for message in config._message_to_delete_in_init:
        delete(message[0], message[1])
        config._message_to_delete_in_init = []

    user = update.message.from_user
    _save_user_in_data(user)

    if config._privacy:
        return

    await _save_profile_photo()

    now = datetime.now()
    delta = timedelta(minutes = 10)
    if user.username is not None:
        if config._who != str(user.username) or config._last_time is None or now - config._last_time > delta:
            config._who = str(user.username)
            print(f'\n{config._who:-^20}\n')
            send( f'<b>{config._who}</b> is writing', [ c for c in config._controllers if c in config._data and config._data[c]['usersupdates'] ] )
    elif user.first_name is not None:
        if config._who != str(user.first_name) or config._last_time is None or now - config._last_time > delta:
            config._who = str(user.first_name)
            print(f'\n{config._who:-^20}\n')
            send( f'<b>{config._who}</b> is writing', [ c for c in config._controllers if c in config._data and config._data[c]['usersupdates'] ] )
    elif config._who != 'NO USERNAME' or config._last_time is None or now - config._last_time > delta:
        config._who = 'NO USERNAME'
        print(f'\n{config._who:-^20}\n')
        send( f'<b>{config._who}</b> is writing', [ c for c in config._controllers if c in config._data and config._data[c]['usersupdates'] ] )
    if config._last_time is None or now - config._last_time > delta:
        config._last_time = now

    _save_text_message_in_data()

def _save_user_in_data(user):
    """
    Handles and saves user's infos into config._data dict.

    This function is private and should not be used directly by users of the package.

    Parameters
    ----------
    user : telegram.User
        python-telgram-bot user object.
    """
    time = str([int(t) for t in datetime.timetuple(datetime.now())][:6])

    user_dict = user.to_dict()
    del user_dict['id']

    stringUser = ''
    for key, val in user_dict.items():
        stringUser += f'{key}: {val}\n'
    stringUser = stringUser[:-1]

    if config._user_id not in config._data:
        params = config._system_params
        if config._user_id in config._controllers:
            params = dict( list( params.items() ) + list( config._controllers_params.items() ) )
        if config._default_params is not None:
            params = dict( list( params.items() ) + list( config._default_params.items() ) )
        config._data[config._user_id] = params
        if config._privacy:
            return
        config._data[config._user_id]['info'][time] = user_dict
        print(f"\n{'NEW USER':-^20}\n{stringUser}")
        send( f'<b>NEW USER</b>\n{stringUser}', [ c for c in config._controllers if c in config._data and config._data[c]['usersupdates'] ] )
    elif not config._privacy and (not config._data[config._user_id]['info'] or user_dict != list(config._data[config._user_id]['info'].values())[-1]):
        config._data[config._user_id]['info'][time] = user_dict
        config._last_time = None
        print(f"\n{'CHANGED USER INFO':-^20}\n{stringUser}")
        send( f'<b>CHANGED USER INFO</b>\n{stringUser}', [ c for c in config._controllers if c in config._data and config._data[c]['usersupdates'] ] )

async def _save_profile_photo():
    """
    Saves profile photo of the user to ./photos/user_id/ (only if privacy is turned off).

    This function is private and should not be used directly by users of the package.

    Parameters
    ----------
    user : telegram.User
        python-telgram-bot user object.
    """
    if config._privacy:
        return

    photos = await config._context.bot.get_user_profile_photos(config._user_id)
    if photos.total_count > 0:
        photoFile = await photos.photos[0][2].get_file()
        photoName = await photoFile.download_to_drive()
        photoName = str(photoName)
        path = config._path + 'profile_photos/' + config._user_id
        if not os.path.exists(path):
            os.makedirs(path)
        os.rename(photoName, path + '/' + photoName)
        return path + '/' + photoName

def _save_text_message_in_data(message = None, message_id = None, user_id = None, is_text_to_audio = False):
    """
    Saves text message to config._data dict (only if privacy is turned off).

    This function is private and should not be used directly by users of the package.

    Parameters
    ----------
    message : str or None, optional
        The message to be saved sent by the bot or `None` (dafault) if message is sent by the user.
    message_id : int or str or None, optional
        message_id of the message to be saved sent by the bot or `None` (default) if message is sent by the user.
    user_id : int or str or None, optional
        user_id of the user you are sending the message to be saved to or `None` (default) to use `config._user_id`.
    is_text_to_audio : bool, optional
        `True` if the message to be saved that the bot is sending is text converted to audio (default is `False`).
    """
    if config._privacy:
        return

    year, month, day, hour, min, sec, *_ = [str(t) for t in datetime.timetuple(datetime.now())]

    message_type = 'text'

    if message is None:
        mex = update().message.text
        if mex is None:
            mex = ''
        message_id = update().message.message_id
        who = config._who
    else:
        mex = message
        who = bot_name()
        if is_text_to_audio:
            message_type = 'audio'

    if user_id is None:
        user_id = config._user_id

    key = f'[{hour}, {min}, {sec}]({message_type})({message_id}){who}'

    print(key + ':\t' + mex)

    chat = config._data[user_id]['chat']

    try:
        while key in chat[year][month][day]:
            key += ' '
    except:
        None

    empty = {
        year: {
            month: {
                day: {
                    key: mex
                }
            }
        }
    }

    if year not in chat:
        chat.update(empty)
    elif month not in chat[year]:
        chat[year].update(empty[year])
    elif day not in chat[year][month]:
        chat[year][month].update(empty[year][month])
    else:
        chat[year][month][day].update(empty[year][month][day])

    if message is None and user_id in config._users_to_send_to_admin:
        send(f'<b>' + key + '</b>: ' + mex)