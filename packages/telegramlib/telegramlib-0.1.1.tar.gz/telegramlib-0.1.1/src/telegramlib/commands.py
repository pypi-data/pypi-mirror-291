"""
Telegram Bot Command Module
===========================

This module provides functionality for defining and handling default commands within a Telegram bot.
It includes decorators to restrict access to certain commands based on user roles and functions to
perform specific actions such as executing terminal commands, managing user follow lists, sending
messages, and banning users.

Usage
-----
To make these commands usables, it is necessary to add them to the command list during bot start in start_bot function.
"""

import functools
from .core import _bot_started_check, send, bot_reply_text
from .config import config, context, update, bot_name
import subprocess
from .data import get_chat

__all__ = ['admin_command', 'controllers_command', 'terminal', 'follow', 'unfollow', 'write', 'ban', 'sban', 'creator', 'closecreator']

# decorator
def admin_command(func):
    """
    Decorator to restrict command execution to the bot's admin.

    This decorator checks if the current user is the admin before executing
    the decorated function. It ensures that only the admin can perform certain
    sensitive actions, such as managing users or executing system commands.

    Parameters
    ----------
    func : function
        The function to be wrapped and executed only by the admin.

    Returns
    -------
    wrapper : function
        The wrapped function with admin check applied.
    """
    @functools.wraps(func)
    @_bot_started_check
    async def wrapper(*args):
        if config._user_id == config._admin:
            await func()
    return wrapper

# decorator
def controllers_command(func):
    """
    Decorator to restrict command execution to users listed as controllers.

    This decorator allows only users identified as controllers in the bot's
    configuration to execute the decorated function. Controllers have a higher
    level of access compared to regular users but less than the admin.

    Parameters
    ----------
    func : function
        The function to be wrapped and executed only by controllers.

    Returns
    -------
    wrapper : function
        The wrapped function with controller check applied.
    """
    @functools.wraps(func)
    @_bot_started_check
    async def wrapper(*args):
        if config._user_id in config._controllers:
            await func()
    return wrapper

@admin_command
async def terminal():
    """
    Executes terminal commands as the admin.

    This function allows the admin to execute system-level commands directly
    from the chat. It filters out the initial bot command and 'sudo' keyword
    for security reasons. The output of the command is sent back to the chat.

    Example
    -------
    /command ls -la
    """
    command = update().message.text.split(' ')
    command = list(filter(('').__ne__, command)) # elimina dalla lista tutti gli elementi stringa vuota: ''
    if len(command) > 1 and 'sudo' not in command:
        command = command[1:]
        cmd = ' '.join(command)
        send(f'<b>Execute</b>: {cmd}')
        try:
            output = subprocess.check_output(command, universal_newlines = True)
        except Exception as e:
            send(f'<b>Error</b>: {e}')
        else:
            send(output)

@admin_command
async def follow():
    """
    Adds users to the admin's list of followed users.

    This function allows the admin to follow specific users, meaning he
    will receive messages sent from these users to the bot. It adds the
    specified users to the `config._users_to_send_to_admin` list and
    provides recent chat history.

    Example
    -------
    /follow <user_id_1> <user_id_2>
    """
    config._users_to_send_to_admin += context().args
    send(f'following: {config._users_to_send_to_admin}')

    for user in context().args:
        if user in config._data:
            send( '<b>' + user + '</b>\n' +  get_chat(user, last = 10, to_string = True, only_name_keys = True) )

@admin_command
async def unfollow():
    """
    Removes users from the admin's list of followed users.

    This function removes the specified users from the list of followed users.
    If no users are specified, it clears the entire list.

    Example
    -------
    /unfollow <user_id_1> <user_id_2>
    """
    if len(context().args) == 0:
        config._users_to_send_to_admin = []
    else:
        for id in context().args:
            if id in config._users_to_send_to_admin:
                config._users_to_send_to_admin.remove(id)

    send(f'following: {config._users_to_send_to_admin}')

@admin_command
async def write():
    """
    Sends a message to a specified user from the admin.

    This function allows the admin to send a custom message to any user.
    It takes the user ID (or 'all') and the message text as arguments.

    Example
    -------
    /write <user_id> Hello! How are you?
    """
    s = 'No messages sent'
    if len(context().args) >= 2:
        id = context().args[0]
        message = ' '.join(context().args[1:])
        s = send(message, id)
    send(str(s))

@admin_command
async def ban():
    """
    Bans specified users from the bot.

    This function sets a 'ban' flag for each specified user, preventing them
    from interacting with the bot.

    Example
    -------
    /ban <user_id_1> <user_id_2>
    """
    for id in context().args:
        config._data[id]['ban'] = True
    banned = [ id for id in config._data if config._data[id]['ban'] ]
    send(f'banned: {banned}')

@admin_command
async def sban():
    """
    Unbans all or specified users from the bot.

    This function removes the 'ban' flag from all users if no arguments are provided,
    or from the specified users if arguments are given.

    Example
    -------
    /sban <user_id_1> <user_id_2>
    """
    if len(context().args) == 0:
        for id in config._data:
            config._data[id]['ban'] = False
    else:
        for id in context().args:
            config._data[id]['ban'] = False

    banned = [ id for id in config._data if config._data[id]['ban'] ]
    send(f'banned: {banned}')

@_bot_started_check
async def creator():
    """
    Initiates a direct conversation with the bot's creator.

    This function notifies the admin that a user wants to initiate a conversation.
    It adds the user to the list of users to send messages to the admin and provides
    a prompt indicating that they are now talking to the bot's creator.
    """
    config._users_to_send_to_admin.append(config._user_id)
    config._creator_users.append(config._user_id)
    send(f'<b>{config._who} ({config._user_id}) VUOLE PARLARE CON TE</b>')
    await bot_reply_text('You are now talking to the creator of the bot, you can ask what you need and wait for his answer')

@_bot_started_check
async def closecreator():
    """
    Ends the conversation with the bot's creator.

    This function removes the user from the list of users having a direct
    conversation with the bot's creator and provides a message indicating
    that the conversation is closed.
    """
    if config._user_id in config._creator_users:
        config._creator_users.remove(config._user_id)
    await bot_reply_text('Conversation closed, now what you write will only be read by ' + bot_name())