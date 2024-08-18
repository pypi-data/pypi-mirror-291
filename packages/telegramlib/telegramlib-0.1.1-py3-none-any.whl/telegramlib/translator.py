"""
Translation and Language Detection Module

This module provides functionalities for translating text between different languages
and detecting the language of a given text using the `googletrans` library.

Usage Example
-------------
1. Command-Line Usage:
    ```console
    python translator.py --english --italian Hello, World!
    ```
    The above command converts "Hello, World!" from english to Italian.
    ```console
    python translator.py --english --italian Hello, World!
    ```
    The above command converts "Hello, World!" in Italian detecting the quote is in english.
    ```console
    python translator.py --detect Hello, World!
    ```
    The above command detect "Hello, World!" language.
"""

from googletrans import Translator, LANGUAGES
import sys

def main():
    """Main function that handles command-line arguments for translation and language detection."""
    if len(sys.argv) > 2 and (sys.argv[1] == '-d' or sys.argv[1] == '--detect'):
        print( language_of( ' '.join(sys.argv[2:]) ) )
    elif len(sys.argv) > 3 and sys.argv[1][:2] == '--' and sys.argv[2][:2] == '--':
        if not (is_a_language(sys.argv[1][2:]) and is_a_language(sys.argv[2][2:])):
            print('Error: invalid language')
        else:
            print( translate( ' '.join(sys.argv[3:]), sys.argv[1][2:], sys.argv[2][2:] ) )
    elif len(sys.argv) > 2 and sys.argv[1][:2] == '--':
        if not is_a_language(sys.argv[1][2:]):
            print('Error: invalid language')
        else:
            print( translate( ' '.join(sys.argv[2:]), dest = sys.argv[1][2:] ) )
    elif len(sys.argv) > 1:
        print( translate( ' '.join(sys.argv[1:]) ) )
    else:
        print('translator.py --<src language> --<dest language> <text to translate>\n'+
            'translator.py --<dest language> <text to translate>\n'+
            '(without src or/and dest languages will interpret as possible)\n'+
            'translator.py -d (or --detect) <text whose language is to be detected>')


def translate(text, src = None, dest = None):
    """
    Translates the given text from the source language to the destination language.

    Parameters
    ----------
    text : str
        The text to be translated
    src : str, optional
        The source language code (default is `None`, which means automatic detection).
    dest : str, optional
        The destination language code (default is `None`, which means automatic detection).

    Returns
    -------
    str
        The translated text or the detected language code.
    """
    if src and dest:
        return Translator().translate('_ ' + text, src = src, dest = dest).text[1:].strip()
    elif dest:
        return Translator().translate('_ ' + text, dest = dest).text[1:].strip()
    elif src:
        return Translator().translate('_ ' + text, src = src).text[1:].strip()
    return Translator().translate('_ ' + text).text[1:].strip()

def language_of(text):
    """
    Detects the language of the given text.

    Parameters
    ----------
    text : str
        The text whose language is to be detected.

    Returns
    -------
    str
        The language code of the detected language.
    """
    return Translator().detect('_ ' + text).lang

def is_a_language(lan):
    """
    Checks if the given language code or name is a valid language supported by Google Translate.

    Parameters
    ----------
    lan : str
        The language code or name to check.

    Returns
    -------
    bool
        `True` if the language is valid, `False` otherwise.
    """
    return lan in LANGUAGES.keys() or lan in LANGUAGES.values()

if __name__ == '__main__':
    main()
