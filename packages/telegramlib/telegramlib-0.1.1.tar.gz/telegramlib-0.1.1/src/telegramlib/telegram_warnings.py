"""
Warnings Module for Telegram Bot Library

This module defines a set of custom warning classes for the Telegram bot library.
These warnings are used to notify developers and users of non-critical issues
that may occur during the operation of the bot, such as invalid configurations
or usage patterns that may lead to unexpected behavior.

Details
-------
All warnings in this module are derived from `TelegramLibWarning`, which in turn
derives from Python's built-in `Warning` class. Each warning class provides additional
context-specific information relevant to the Telegram bot library.
"""

from colorama import Fore

class TelegramLibWarning(Warning):
    """
    Base class for warnings in this module.

    This is the base class for all custom warnings defined in the Telegram bot library.
    It ensures that all exceptions use yellow colored output for better visibility in console applications.

    Parameters
    ----------
    message : str
        The message describing the warning.
    """
    def __init__(self, message):
        super().__init__(Fore.YELLOW + message + Fore.RESET)

class TextToSpeechWarning(Warning):
    """
    Warning raised for attempts to convert text unsuitable for conversion to speech.

    Parameters
    ----------
    text : str
        The text that was attempted to be converted.
    message : str, optional
        Custom message for the warning (default is "You cannot convert text to speech").
    """
    def __init__(self, text, message="You cannot convert text to speech"):
        self.text = text
        self.message = f"{message}: {text}"
        super().__init__(self.message)

class FunctionNotScheduledWarning(TelegramLibWarning):
    """
    Warning raised for attempts to define scheduled function without passing it during bot startup.

    Parameters
    ----------
    function : function
        The function object that was not scheduled correctly.
    message : str, optional
        Custom message for the warning (default is "Function not passed as a scheduled function during startup").
    """
    def __init__(self, function, message=f"Function not passed as a scheduled function during startup"):
        self.function = function.__name__
        self.message = f"{message}: {self.function}"
        super().__init__(self.message)

class InvalidBotParameterWarning(TelegramLibWarning):
    """
    Warning raised for attempts to define restricted bot parameters.

    Parameters
    ----------
    parameter : str
        The name of the parameter that is restricted.
    message : str, optional
        Custom message for the warning (default is "You cannot define bot parameters named 'chat', 'info', 'jobs', 'ban' or 'usersupdates'").
    """
    def __init__(self, parameter, message="You cannot define bot parameters named 'chat', 'info', 'jobs', 'ban' or 'usersupdates"):
        self.parameter = parameter
        self.message = f"{message}: {parameter}"
        super().__init__(self.message)

class NonExistentParameterWarning(TelegramLibWarning):
    """
    Warning raised for attempts to access or modify non-existent parameter

    Parameters
    ----------
    parameter : str
        The name of the non-existent parameter.
    message : str, optional
        Custom message for the warning (default is "Parameter non-existent").
    """
    def __init__(self, parameter, message=f"Parameter non-existent"):
        self.parameter = parameter
        self.message = f"{message}: {parameter}"
        super().__init__(self.message)
