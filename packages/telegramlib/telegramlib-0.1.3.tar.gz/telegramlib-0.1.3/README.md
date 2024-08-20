# telegramlib

Easiest Python package to create Telegram bots.

Developed by [ilLancio](https://illancio.github.io).

[![pypi](https://img.shields.io/badge/pypi-v0.1.3-blue)](https://pypi.org/project/telegramlib/)
[![python](https://img.shields.io/badge/python-3.11%2B-blue)](https://www.python.org)
[![release date](https://img.shields.io/badge/release_date-august_2024-red)](https://github.com/ilLancio/telegramlib/blob/master/CHANGELOG.md)

## Table of Contents

* [Installation](#installation)
* [Usage Examples](#usage-examples)
* [Complete List of Functions](#complete-list-of-functions)
* [Documentation](#documentation)
* [Changelog](#changelog)
* [License](#license)
* [Author](#author)

## Installation

You can install the package from [PyPI](https://pypi.org/project/telegramlib/) using pip:

```console
pip install telegramlib
```

## Usage examples

### Setting up your bot

1. **Obtain a Telegram bot token** from [BotFather](https://t.me/BotFather).
2. **Obtain your Telegram user ID** from [RawDataBot](https://t.me/raw_info_bot).
3. **Replace placeholders** with your actual bot token and user ID in the examples below.

### Example 1: Starting the Bot

Define a start function that performs what you want to happen when a user types the `/start` command. Then remember to add the command in the `start_bot` function along with your token and user id.

```python
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
```

```Telegram
User: /start
Bot:  Bot started!
```

#### Disable user privacy

If you want to save user information, you must explicitly specify it as a parameter in the `start_bot` function by setting `privacy=False`, like so: `start_bot(token=TOKEN, ..., privacy=False)`. User information will be saved in the `database.json` file.

#### Legal Disclaimer: User Privacy and Data Handling

Please note that you are solely responsible for complying with all applicable data protection and privacy laws. This includes, but is not limited to, obtaining user consent where required, securely storing the data, and providing users with necessary disclosures regarding how their data will be used. The author of this library assumes no liability for any legal consequences arising from the use or misuse of this functionality.

#### Disable user updates

Disabling user privacy and being an admin yourself, you will receive informative messages from the bot about the activities of your bot's users. To disable or enable it, send it the `/usersupdates` command.

### Example 2: Other Commands and Message Handler

Define another command function that makes the bot respond by giving you the command arguments and a message handler that gives the user the name of the bot after being asked for it. Always remember to add the functions in `start_bot`.

```python
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
```

```Telegram
User: /yourcommand Hello Bot!
Bot:  You sent me your command with these arguments: ['Hello', 'Bot!']
User: What's your name
Bot:  My name is <bot-name>
```

### Example 3: Scheduling Future Messages

Define the start function so that it schedules a daily task at 6 p.m., so, typing the start command, every day at 6 p.m. will be executed the contents of the `scheduled_task` function defined under, also to be added to the `start_bot` function. Additionally define a command that removes all user tasks.

```python
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
async def scheduled_task():
    await bot_reply_text('This is a scheduled task!')

# Bot configuration and start
start_bot(
    token=TOKEN,
    admin=ADMIN,
    commands=[start, removetasks],
    scheduled=scheduled_task
)
```

```Telegram
User: /start
Bot:  Scheduled task every day at 6 p.m.

(at 6:00 PM)
Bot:  This is a scheduled task!

User: /removetasks
Bot:  Tasks all deleted
```

### Example 4: Users Parameters, Admin and Controllers

Specify in the `start_bot` function a dictionary representative of the users' default parameters. That done, you can access and modify those parameters with `get_param` and `set_param`. In the example we use within the start command and commands with access restricted to the admin and controllers, which are also specified in the `start_bot` function.

```python
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
```

```Telegram
User: /start
Bot:  Your parameter 2 is been set to False
User: /admincommand
Bot:  I am answering you because you are the admin and your parameter 1 is 42
User: /controllercommand
Bot:  I am responding to you because you are an admin and an admin is always controller. Your parameter 1 is 42
```

## Complete List of Functions

* `start_bot(token, admin, commands, messages=None, scheduled=None error=None, controllers = None, params=None, privacy=True)`

  *Start the Telegram bot.*

* `command_args()`

  *Get the command arguments.*

* `bot_reply_text(message, text_to_audio=False, translate_to=None, talking_about_latex=False)`

  *Respond with a text from the bot.*

* `send(message, chat_id=None, save=True, token=None, parse_mode=ParseMode.HTML)`

  *Send a message.*

* `delete(chat_id, message_id, token=None)`

  *Delete a message.*

* `context()`

  *Get the python-telegram-bot context.*

* `update()`

  *Get the python-telegram-bot update.*

* `bot_name()`

  *Get the name of the bot.*

* `set_param(key, value)`

  *Set a parameter of the user.*

* `get_param(key)`

  *Get a parameter of the user.*

* `get_chat(user=None, last=None, last_message=None, max_char=None, to_string=False, to_list=False, only_name_keys=False, without_keys=False)`

  *Get a chat.*

* `admin_command(func)`

  *Decorator for admin Telegram commands.*

* `controllers_command(func)`

  *Decorator for controllers Telegram commands.*

#### Ready-to-use commands (to be added to start_bot for use)

* `terminal()`

  *Admin Telegram command to type a command on the bot's machine terminal.*

* `follow()`

  *Admin Telegram command to follow user messages.*

* `unfollow()`

  *Admin Telegram command to stop following user messages.*

* `write()`

  *Admin Telegram command to write a message to another user.*

* `ban()`

  *Admin Telegram command to ban a user.*

* `sban()`

  *Admin Telegram command to remove ban from a user.*

* `creator()`

  *Telegram command to contact the creator of the bot.*

* `close_creator()`

  *Telegram command to close the dialog with the bot creator.*

#### For scheduling tasks

* `new_daily_job_from_args(function, reset=False)`

  *Create a new daily job by taking time from command arguments.*

* `get_command_args_daily_job_time_format(n_arg=0)`

  *Get time from command arguments.*

* `is_daily_job_scheduled(function, hour, minute)`

  *Check whether a daily job is scheduled.*

* `daily_jobs_scheduled_times_to_string(mex='', if_empty_mex='')`

  *Convert scheduled daily job times to a string.*

* `remove_all_daily_jobs()`

  *Remove all daily jobs.*

* `new_daily_job(function, hour, minute, reset=False)`

  *Create a new daily job.*

## Documentation

You can find documentation [here](https://illancio.github.io/telegramlib/).

## Changelog

For a detailed history of changes, see the [Changelog](https://github.com/ilLancio/telegramlib/blob/master/CHANGELOG.md).

## License

This project is licensed under the MIT License - see the [LICENSE](https://github.com/ilLancio/telegramlib/blob/master/LICENSE) file for details.

The licenses of the dependencies used in this project are listed in the file [THIRD_PARTY_LICENSES.txt](https://github.com/ilLancio/telegramlib/blob/master/THIRD_PARTY_LICENSES.txt).

## Author

* Daniele Lanciotti

  Email: <daniele9001@gmail.com>

  Website: [illancio.github.io](https://illancio.github.io/)
