"""
Daily Jobs Management Module

This module provides functionalities for scheduling, managing, and retrieving daily jobs for users
within a Telegram bot environment. It allows you to schedule new daily jobs, check if specific jobs
are scheduled, and manage existing jobs by removing or listing them. It also handles the formatting
of daily job schedules into user-friendly strings.
"""

from .config import config, context, _bot_started_check
import functools
import warnings
from .telegram_warnings import FunctionNotScheduledWarning
import re
from datetime import time
import pytz


__all__ = [
    'new_daily_job_from_args',
    'get_command_args_daily_job_time_format',
    'is_daily_job_scheduled',
    'daily_jobs_scheduled_times_to_string',
    'remove_all_daily_jobs',
    'new_daily_job'
]

# decorator
def _scheduled(func):
    """
    Decorator applied to scheduled functions to check if the function is been passed as scheduled during startup of the bot and to configure and manage data.

    This decorator is private and should not be used directly by users of the package.

    Parameters
    ----------
    func : Callable
        Scheduled function to decorate.

    Returns
    -------
    Callable
        A modified function that includes check, configuration and management of data.
    """
    if not ( func == config._scheduled_functions or (isinstance(config._scheduled_functions, list) and func in config._scheduled_functions) ):
        warnings.warn(FunctionNotScheduledWarning(func))
    @functools.wraps(func)
    async def wrapper(*args):
        config._context = args[0]
        if not config._data[config._user_id]['ban']:
            await func()
            config._memorize()
        config._context = None
    return wrapper

def new_daily_job_from_args(function, reset = False):
    """
    Schedules a new user's daily job from Telegram command argument with hh:mm format.

    Parameters
    ----------
    function : Callable
        Scheduled function of daily job.
    reset : bool, optional
        `True` to remove all previously scheduled daily jobs of the user (defalut is `False`).

    Returns
    -------
    str
        Successful or unsuccessful message: `'job created'`, `'wrong args'` or `'empty args'`.
    """
    if len(context().args) > 0:
        hour, minute = get_command_args_daily_job_time_format()
        if hour is not None and minute is not None:
            new_daily_job(function, hour, minute, reset)
            return 'job created'
        return 'wrong args'
    return 'empty args'

def get_command_args_daily_job_time_format(n_arg = 0):
    """
    Get (hour, minute) from Telegram command argument with hh:mm format.

    Parameters
    ----------
    n_arg : int, optional
        Numerical argument index (default is `0`).

    Returns
    -------
    tuple
        A tuple containing hour (int) and minute (int).
    """
    hour = minute = None
    time_format = re.compile('^(?:[01]?\d|2[0-3])(?::[0-5]\d){1,2}$')
    args = context().args
    if len(args) > n_arg:
        if time_format.match(args[n_arg]):
            hour = int(args[n_arg].split(':')[0])
            minute = int(args[n_arg].split(':')[1])
    return (hour, minute)

@_bot_started_check
def is_daily_job_scheduled(function, hour, minute):
    """
    Tells whether a given user's daily job is scheduled or not.

    Parameters
    ----------
    function : Callable
        Scheduled function of daily job.
    hour : int
        Scheduled hour of daily job.
    minute : int
        Scheduled minute of daily job.

    Returns
    -------
    bool
        `True` if the function is scheduled at the given hour and minute, `False` otherwise.
    """
    current_jobs = context().job_queue.get_jobs_by_name(config._user_id)
    for job in current_jobs:
        if job.callback.__name__ == function.__name__ and str(job.trigger) == f"cron[day_of_week='sun,mon,tue,wed,thu,fri,sat', hour='{hour}', minute='{minute}', second='0']":
            return True
    return False

@_bot_started_check
def daily_jobs_scheduled_times_to_string(mex = '', if_empty_mex = ''):
    """
    Get the user's daily jobs formatted into a string.

    Parameters
    ----------
    mex : str, optional
        Text that comes before the list of daily jobs (default is `''`).
    if_empty_mex : str, optional
        Text returned in case of no daily jobs (default is `''`).

    Returns
    -------
    str
        Text with daily jobs list.
    """
    current_jobs = context().job_queue.get_jobs_by_name(config._user_id)
    if len(current_jobs) == 0:
        mex = if_empty_mex
    elif mex:
        if len(current_jobs) == 1:
            mex += ' '
        else:
            mex += ':\n'
    for job in current_jobs:
        hour_index = job.trigger.FIELD_NAMES.index('hour')
        hour = int(str( job.trigger.fields[hour_index] ))
        minute_index = job.trigger.FIELD_NAMES.index('minute')
        minute = int(str( job.trigger.fields[minute_index] ))
        mex += '%d:%02d' % (hour, minute) + '\n'
    return mex if mex[-1] != '\n' else mex[:-1]

@_bot_started_check
def remove_all_daily_jobs():
    """
    Removes all saved user's daily jobs from both the job queue and the user's data.
    """
    current_jobs = context().job_queue.get_jobs_by_name(config._user_id)
    for job in current_jobs:
        job.schedule_removal()
    config._data[config._user_id]['jobs'] = []

@_bot_started_check
def new_daily_job(function, hour, minute, reset = False):
    """
    Schedules and saves a new user's daily job.

    Parameters
    ----------
    function : Callable
        Scheduled function of daily job.
    hour : int
        Scheduled hour of daily job.
    minute : int
        Scheduled minute of daily job.
    reset : bool, optional
        `True` to remove all previous saved user's daily jobs (default is `False`).
    """
    function = _scheduled(function)
    if reset:
        remove_all_daily_jobs()
    target_time = time(hour = hour, minute = minute).replace(tzinfo = pytz.timezone('Europe/Berlin'))
    context().job_queue.run_daily(function, time = target_time, chat_id = config._user_id, name = config._user_id)
    _save_daily_job_in_data(function, hour, minute)

def _save_daily_job_in_data(function, hour, minute):
    """
    Saves function name, hour and minute of a new user's daily job in config._data.

    This function is private and should not be used directly by users of the package.

    Parameters
    ----------
    function : Callable
        Scheduled function of daily job.
    hour : int
        Scheduled hour of daily job.
    minute : int
        Scheduled minute of daily job.
    """
    function = function.__name__
    config._data[config._user_id]['jobs'].append( {'function': function, 'hour': hour, 'minute': minute} )