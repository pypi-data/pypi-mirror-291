"""
Telegram Bot Library Exceptions Module

This module defines custom exception classes for the Telegram bot library.
These exceptions are used to handle specific error conditions that may arise
during the operation of the bot, providing more granular and meaningful error
messages.

Details
-------
All exceptions in this module derive from `TelegramLibError`, which in turn
inherits from Python's built-in `Exception` class. Each custom exception provides
context-specific error handling, enabling the bot to communicate precise issues
to developers and users.
"""

from colorama import Fore

class TelegramLibError(Exception):
    """
    Base class for exceptions in this module.

    This is the base class for all custom exceptions defined in the Telegram bot library.
    It ensures that all exceptions use red colored output for better visibility in console applications.

    Parameters
    ----------
    message : str
        The message describing the error.
    """
    def __init__(self, message):
        super().__init__(Fore.RED + message + Fore.RESET)

class InternalError(TelegramLibError):
    """
    Exception raised for internal errors.

    Parameters
    ----------
    message : str
        The message describing the internal error.
    """
    def __init__(self, message):
        super().__init__(Fore.RED + 'Internal Error: ' +  message + Fore.RESET)

class MissingStartCommandError(TelegramLibError):
    """
    Exception raised when starting bot without a start command.
    
    Parameters
    ----------
    message : str, optional
        Custom message for the exception (default is "You can't start a bot without a start command").
    """
    def __init__(self, message="You can't start a bot without a start command"):
        self.message = message
        super().__init__(self.message)

class InvalidDataStructureError(TelegramLibError):
    """
    Exception raised when database is corrupted or improperly modified
    
    Parameters
    ----------
    message : str, optional
        Custom message for the exception (default is "Invalid data structure: database is corrupted or improperly modified").
    """
    def __init__(self, message="Invalid data structure: database is corrupted or improperly modified"):
        self.message = message
        super().__init__(self.message)

class AdminNotDefinedError(InternalError):
    """
    Exception raised when attempting to set controllers without an admin.
    
    Parameters
    ----------
    message : str, optional
        Custom message for the exception (default is "You cannot define controllers without first specifying the admin").
    """
    def __init__(self, message="You cannot define controllers without first specifying the admin"):
        self.message = message
        super().__init__(self.message)

class InvalidTypeError(TelegramLibError):
    """
    Exception raised when a variable is of an unexpected type.
    
    Parameters
    ----------
    expected_type : type
        The expected type of the variable.
    actual_type : type
        The actual type of the variable.
    message : str, optional
        Custom message for the exception (default is "Invalid type").
    """
    def __init__(self, expected_type, actual_type, message="Invalid type"):
        self.message = f"{message}: expected {expected_type}, got {actual_type}"
        super().__init__(self.message)

class BotNotStartedCorrectlyError(TelegramLibError):
    """
    Exception raised when attempting to perform actions without starting the bot properly.

    Parameters
    ----------
    message : str, optional
        Custom message for the exception (default is "You must first start the bot with the start_bot function").
    """
    def __init__(self, message="You must first start the bot with the start_bot function"):
        self.message = message
        super().__init__(self.message)