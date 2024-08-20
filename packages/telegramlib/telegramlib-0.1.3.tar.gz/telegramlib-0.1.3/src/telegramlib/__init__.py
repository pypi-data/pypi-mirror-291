"""
telegramlib
===========

Easiest Python package to create Telegram bots.

Version:
    0.1.3

Authors:
    Daniele Lanciotti (daniele9001@gmail.com) (https://illancio.github.io)

Changelog:

    https://github.com/ilLancio/telegramlib/blob/master/CHANGELOG.md

License:
    MIT License
    
    https://github.com/ilLancio/telegramlib/blob/master/LICENSE

Third party licenses:

    https://github.com/ilLancio/telegramlib/blob/master/THIRD_PARTY_LICENSES.txt


Modules
-------
.. autosummary::
   :toctree: _autosummary

   config
   core
   data
   commands
   jobs

   telegram_exceptions
   telegram_warnings
   utils
   text_to_speech
   translator

Exported Functions
------------------
.. autosummary::
   :toctree: _autosummary

   start_bot
   command_args
   bot_reply_text
   send
   delete

   context
   update
   bot_name

   set_param
   get_param
   get_chat

   admin_command
   controllers_command
   terminal
   follow
   unfollow
   write
   ban
   sban
   creator
   closecreator

   new_daily_job_from_args
   get_command_args_daily_job_time_format
   is_daily_job_scheduled
   daily_jobs_scheduled_times_to_string
   remove_all_daily_jobs
   new_daily_job


Installation
------------
You can install the package from PyPI using pip:

.. code-block:: bash

    pip install telegramlib


Usage Examples
--------------
Setting up your bot:

1. **Obtain a Telegram bot token** from https://t.me/BotFather.

2. **Obtain your Telegram user ID** from https://t.me/raw_info_bot.

3. **Replace placeholders** with your actual bot token and user ID in the examples below.


Usage Example 1: Starting the Bot
---------------------------------
Define a start function that performs what you want to happen when a user types the `/start` command.
Then remember to add the command in the `start_bot` function along with your token and user id.

.. code-block:: python

    from telegramlib import *

    TOKEN = 'your Telegram bot token'
    ADMIN = 'your user ID'

    # Define a start command function
    async def start():
        await bot_reply_text('Bot started!')

    # Bot configuration and start
    start_bot(
        token=TOKEN,
        admin=ADMIN,
        commands=start
    )

.. code-block:: text

    User: /start
    Bot:  Bot started!

Disable user privacy:

If you want to save user information, you must explicitly specify it as a parameter
in the `start_bot` function by setting `privacy=False`, like so: `start_bot(token=TOKEN, ..., privacy=False)`.
User information will be saved in the `database.json` file.

Legal Disclaimer: User Privacy and Data Handling:

Please note that you are solely responsible for complying with all applicable data protection and privacy laws.
This includes, but is not limited to, obtaining user consent where required, securely storing the data,
and providing users with necessary disclosures regarding how their data will be used.
The author of this library assumes no liability for any legal consequences arising from the use or misuse of this functionality.

Disable user updates:

Disabling user privacy and being an admin yourself, you will receive informative messages from the bot
about the activities of your bot's users.
To disable or enable it, send it the `/usersupdates` command.


Usage Example 2: Other Commands and Message Handler
---------------------------------------------------
Define another command function that makes the bot respond by giving you the command arguments
and a message handler that gives the user the name of the bot after being asked for it.
Always remember to add the functions in `start_bot`.

.. code-block:: python

    from telegramlib import *

    TOKEN = 'your Telegram bot token'
    ADMIN = 'your user ID'

    # Define a start command function
    async def start():
        await bot_reply_text('Bot started!')

    # Define another command function
    async def yourcommand():
        args = str( command_args() )
        response = 'You sent me your command with these arguments: ' + args
        await bot_reply_text(response)

    # Define a message handler function
    async def message():
        if user_message() == "What's your name?":
            await bot_reply_text('My name is ' + bot_name())

    # Bot configuration and start
    start_bot(
        token=TOKEN,
        admin=ADMIN,
        commands=[start, yourcommand],
        messages=message
    )

.. code-block:: text

    User: /yourcommand Hello Bot!
    Bot:  You sent me your command with these arguments: ['Hello', 'Bot!']
    User: What's your name
    Bot:  My name is <bot-name>


Usage Example 3: Scheduling Future Messages
-------------------------------------------
Define the start function so that it schedules a daily task at 6 p.m.,
so, typing the start command, every day at 6 p.m. will be executed the contents of the
`scheduled_task` function defined under, also to be added to the `start_bot` function.
Additionally define a command that removes all user tasks.

.. code-block:: python

    from telegramlib import *

    TOKEN = 'your Telegram bot token'
    ADMIN = 'your user ID'

    # Define a start command function
    async def start():
        # Task scheduling. reset=True to remove old scheduled tasks
        new_daily_job(scheduled_task, 18, 0, reset=True)
        await bot_reply_text('Scheduled task every day at 6 p.m.')

    # Define another command
    async def removetasks():
        remove_all_daily_jobs()
        await bot_reply_text('Tasks all deleted')

    # Define a scheduled function
    async def scheduled_task():
        await bot_reply_text('This is a scheduled task!')

    # Bot configuration and start
    start_bot(
        token=TOKEN,
        admin=ADMIN,
        commands=[start, removetasks],
        scheduled=scheduled_task
    )

.. code-block:: text

    User: /start
    Bot:  Scheduled task every day at 6 p.m.

    (at 6:00 PM)
    Bot:  This is a scheduled task!

    User: /removetasks
    Bot:  Tasks all deleted


Usage Example 4: Users Parameters, Admin and Controllers
--------------------------------------------------------
Specify in the `start_bot` function a dictionary representative of the users' default parameters.
That done, you can access and modify those parameters with `get_param` and `set_param`.
In the example we use within the start command and commands with access restricted
to the admin and controllers, which are also specified in the `start_bot` function.

.. code-block:: python

    from telegramlib import *

    TOKEN = 'your Telegram bot token'
    ADMIN = 'your user ID'

    # Define a start command function
    async def start():
        set_param('parameter 2', False)
        await bot_reply_text('Your parameter 2 is been set to False')

    # Admin restricted access command
    @admin_command
    async def admincommand():
        p = get_param('parameter 1')
        await bot_reply_text(f'I am answering you because you are the admin and your parameter 1 is {p}')

    # Controllers restricted access command
    @controllers_command
    async def controllercommand():
        p = get_param('parameter 1')
        await bot_reply_text(f'I am responding to you because you are an admin and an admin is always a controller. Your parameter 1 is {p}')

    # Bot configuration and start
    start_bot(
        token=TOKEN,
        admin=ADMIN,
        commands=[start, admincommand, controllercommand],
        controllers=[<user_id_1>, <user_id_2>],
        params={'parameter 1': 42, 'parameter 2': True}
    )

.. code-block:: text

    User: /start
    Bot:  Your parameter 2 is been set to False
    User: /admincommand
    Bot:  I am answering you because you are the admin and your parameter 1 is 42
    User: /controllercommand
    Bot:  I am responding to you because you are an admin and an admin is always controller. Your parameter 1 is 42

-----------------------------------------------------------------------------------------------------------------
"""

from .config import *
from .core import *
from .data import *
from .commands import *
from .jobs import *

__version__ = "0.1.0"

__all__ = [
    'start_bot',
    'command_args',
    'bot_reply_text',
    'send',
    'delete',
    # config
    'context',
    'update',
    'user_message',
    'bot_name',
    # data
    'set_param',
    'get_param',
    'get_chat',
    # commands
    'admin_command',
    'controllers_command',
    'terminal',
    'follow',
    'unfollow',
    'write',
    'ban',
    'sban',
    'creator',
    'closecreator',
    # jobs
    'new_daily_job_from_args',
    'get_command_args_daily_job_time_format',
    'is_daily_job_scheduled',
    'daily_jobs_scheduled_times_to_string',
    'remove_all_daily_jobs',
    'new_daily_job'
]