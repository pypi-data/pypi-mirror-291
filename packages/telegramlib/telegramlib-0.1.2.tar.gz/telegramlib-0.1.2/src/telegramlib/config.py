"""
Telegram Bot Configuration Module
=================================

This module manages the configuration and state of a Telegram bot. It includes functionalities for 
setting and retrieving bot parameters, user management, and data persistence. This module ensures 
proper initialization and management of bot settings, admin and controller user IDs, and other 
configuration parameters.

Usage
-----
This module should be used internally.
"""

import pathlib
import inspect
import copy
import json
from .telegram_exceptions import InvalidDataStructureError, AdminNotDefinedError, InvalidTypeError, BotNotStartedCorrectlyError
import warnings
from .telegram_warnings import InvalidBotParameterWarning
import functools

__all__ = ['context', 'update', 'user_message', 'bot_name']

class Config:
    """
    Class for bot configuration management.
    """
    def __init__(self):
        self._path = str( pathlib.Path(inspect.stack()[-1].filename).parent.absolute() ) + '/'
        self._database = self._path + 'database.json'

        self._bot_name = pathlib.Path(inspect.stack()[-1].filename).stem
        if self._bot_name == 'main':
            self._bot_name = str(pathlib.Path(inspect.stack()[-1].filename)).split('/')[-2]

        self.__token = self.__admin = self.__controllers = self.__default_params = self.__scheduled_functions = None

        self._privacy = True

        self.__system_params = {'info': {}, 'chat': {}, 'jobs': [], 'ban': False}
        self.__controllers_params = {'usersupdates': True}

        self.__update = self.__context = self.__user_id = self._who = self._last_time = None

        self._users_to_send_to_admin, self._creator_users, self._message_to_delete_in_init = [], [], []

        self._started_correctly = False

        self._data = self._remind()

    @property
    def _token(self):
        """
        Get bot token.

        This property is private and should not be used directly by users of the package.

        Returns
        -------
        str
            Bot token.
        """
        return self.__token

    @_token.setter
    def _token(self, value):
        """
        Set bot token.

        This property is private and should not be used directly by users of the package.

        Parameters
        ----------
        value : str
            Bot token.
        """
        self.__token = str(value)

    @property
    def _admin(self):
        """
        Get admin user_id.

        This property is private and should not be used directly by users of the package.

        Returns
        -------
        str
            Admin user_id.
        """
        return self.__admin

    @_admin.setter
    def _admin(self, value):
        """
        Set admin user_id.

        This property is private and should not be used directly by users of the package.

        Parameters
        ----------
        value : str
            Admin user_id.
        """
        self.__admin = str(value)

    @property
    def _controllers(self):
        """
        Get controller user_ids.

        This property is private and should not be used directly by users of the package.

        Returns
        -------
        list
            Controller user_ids.
        """
        return self.__controllers

    @_controllers.setter
    def _controllers(self, value):
        """
        Set controller user_ids.

        This property is private and should not be used directly by users of the package.

        Parameters
        ----------
        value : str or list of str
            Controller user_id/user_ids.

        Raises
        ------
        AdminNotDefinedError
            If admin user_id is None.
        """
        if self.__admin is None:
            raise AdminNotDefinedError()
        if value is None:
            self.__controllers = [self.__admin]
        elif isinstance(value, list) and self.__admin not in value:
            self.__controllers = value + [self.__admin]
        elif not isinstance(value, list) and value != self.__admin:
            self.__controllers = [self.__admin, value]
        else:
            self.__controllers = value

        for controller in self._controllers:
            if controller in self._data and list(self._controllers_params.keys())[0] not in self._data[controller]:
                self._data[controller] = dict( list( self._data[controller].items() ) + list( self._controllers_params.items() ) )

        for user in self._data:
            if user not in self._controllers:
                self._data[user] = {k: v for k, v in self._data[user].items() if k not in self._controllers_params}

    @property
    def _system_params(self):
        """
        Get a deepcopy of default system parameters of the users: {'info': {}, 'chat': {}, 'jobs': [], 'ban': False}.

        This property is private and should not be used directly by users of the package.

        Returns
        -------
        dict
            Copy of users' system parameters.
        """
        return copy.deepcopy(self.__system_params)
    
    @property
    def _controllers_params(self):
        """
        Get a deepcopy of default parameters reserved for the admin: {'usersinfos': True}.

        This property is private and should not be used directly by users of the package.

        Returns
        -------
        dict
            Copy of users' system parameters.
        """
        return copy.deepcopy(self.__controllers_params)

    @property
    def _default_params(self):
        """
        Get a deepcopy of default parameters of the users.

        This property is private and should not be used directly by users of the package.

        Returns
        -------
        dict
            Copy of users' default parameters.
        """
        return copy.deepcopy(self.__default_params)

    @_default_params.setter
    def _default_params(self, value):
        """
        Set default parameters of the users.

        This property is private and should not be used directly by users of the package.

        Parameters
        ----------
        value : dict
            Default parameters of the users.

        Raises
        ------
        InvalidTypeError
            If value isn't dict type.
        """
        if value is None:
            return
        if not isinstance(value, dict):
            raise InvalidTypeError(dict, type(value))
        for key in list(self._system_params.keys()) + list(self._controllers_params.keys()):
            if key in value:
                del value[key]
                warnings.warn(InvalidBotParameterWarning(key))

        for id, user in self._data.items():
            user_copy = user.copy()
            for key in user_copy:
                if key not in list(value.keys()) + list(self._system_params.keys()) + list(self._controllers_params.keys()):
                    del self._data[id][key]
            for key, val in value.items():
                if key not in self._data[id]:
                    self._data[id].update({key: val})

        self.__default_params = value

    @property
    def _scheduled_functions(self):
        """
        Get scheduled functions.

        This property is private and should not be used directly by users of the package.

        Returns
        -------
        list
            Scheduled functions.
        """
        return self.__scheduled_functions

    @_scheduled_functions.setter
    def _scheduled_functions(self, value):
        """
        Set scheduled functions.

        This property is private and should not be used directly by users of the package.

        Parameters
        ----------
        value : Callable or list of Callable
            Scheduled function/functions.
        """
        if callable(value):
            self.__scheduled_functions = [value]
        elif isinstance(value, list):
            self.__scheduled_functions = list(dict.fromkeys(value)) # remove duplicates

    @property
    def _update(self):
        """
        Get python-telgram-bot update object.

        This property is private and should not be used directly by users of the package.

        Returns
        -------
        telegram.Update
            python-telgram-bot update object.
        """
        return self.__update

    @_update.setter
    def _update(self, value):
        """
        Set python-telgram-bot update object.

        This property is private and should not be used directly by users of the package.

        Parameters
        ----------
        value : telegram.Update
            python-telgram-bot update object.
        """
        self.__update = value
        if self.__update is None:
            self.__user_id = None
        else:
            self.__user_id = str(self.__update.message.from_user.id)

    @property
    def _context(self):
        """
        Get python-telgram-bot context object.

        This property is private and should not be used directly by users of the package.

        Returns
        -------
        telegram.Context
            python-telgram-bot context object.
        """
        return self.__context

    @_context.setter
    def _context(self, value):
        """
        Set python-telgram-bot context object.

        This property is private and should not be used directly by users of the package.

        Parameters
        ----------
        value : telegram.Context
            python-telgram-bot context object.
        """
        self.__context = value
        if self.__context is None:
            self.__user_id = None
        elif self.__update is None:
            self.__user_id = str(self.__context.job.chat_id)

    @property
    def _user_id(self):
        """
        Get user_id of the user.

        This property is private and should not be used directly by users of the package.

        Returns
        -------
        str
            user_id of the user.
        """
        return self.__user_id

    def _memorize(self):
        """
        Save dict data content into json database file.

        This method is private and should not be used directly by users of the package.
        """
        self._validate_data_structure(self._data)
        with open(self._database, 'w') as file:
            json.dump(self._data, file, indent = 4, ensure_ascii = False)

    def _remind(self):
        """
        Get content of json database file.

        This method is private and should not be used directly by users of the package.

        Returns
        -------
        dict
            Content of json database file.
        """
        memory = {}
        try:
            with open(self._database, 'r') as file:
                memory = json.load(file)
        except:
            print('Memory not found, creating a new one in ' + self._path)
            return {}
        self._validate_data_structure(memory)
        return memory

    def _validate_data_structure(self, data):
        """
        Gives an exception if data content has an invalid structure.

        This method is private and should not be used directly by users of the package.

        Parameters
        ----------
        data : dict
            Content of json database file.

        Raises
        ------
        InvalidDataStructureError
            If data content has an invalid structure.
        """
        if not isinstance(data, dict):
            raise InvalidDataStructureError()
        
        for id, user in data.items():
            if not isinstance(id, str):
                raise InvalidDataStructureError()
            
            if not isinstance(user, dict):
                raise InvalidDataStructureError()
            for key, val in self._system_params.items():
                if key not in user or not isinstance(user[key], type(val)):
                    raise InvalidDataStructureError()

config = Config()

# decorator
def _bot_started_check(func):
    """
    Gives an error if the function is executed before the bot starts.

    This decorator is private and should not be used directly by users of the package.

    Parameters
    ----------
    func : Callable
        Function to decorate.

    Returns
    -------
    Callable
        A modified function that includes checking that the bot has been started.

    Raises
    ------
    BotNotStartedCorrectly
        If the function is executed before the bot starts.

    Examples
    --------
    @_bot_started_check\ndef my_function():
        # Function code
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if not config._started_correctly:
            raise BotNotStartedCorrectlyError()
        return func(*args, **kwargs)
    return wrapper

def update():
    """
     Get python-telegram-bot update object.

     Returns
     -------
     telegram.Update
         python-telegram-bot update object.
     """
    return config._update

def context():
    """
     Get python-telegram-bot context object.

     Returns
     -------
     telegram.Context
         python-telegram-bot context object.
     """
    return config._context

def user_message():
    """
     Get message sent by the user.

     Returns
     -------
     str
         The message sent by the user.
     """
    return update().message.text

def bot_name():
    """
     Get name of the bot.

     Returns
     -------
     str
         Name of the bot.
     """
    return config._bot_name