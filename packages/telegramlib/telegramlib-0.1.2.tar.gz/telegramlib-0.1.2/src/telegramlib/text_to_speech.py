"""
Text-to-Speech Conversion Module

This module provides functionality to convert text into spoken words using the Google Text-to-Speech (gTTS) library.
It supports playing the generated speech audio, saving it in various formats, and removing the file after playback.

Usage Example
-------------
1. Command-Line Usage:
    ```console
    python text_to_speech.py "Hello, World!" en
    ```
    The above command converts "Hello, World!" to speech in English.
2. Function Usage:
    The `text_to_speech` function can be used within other Python scripts to convert text to speech with custom options.

    Example of converting text to speech and playing it:
    ```python
    text_to_speech(“Hello, how are you?”, play = True, remove = True)
    ```
"""

from gtts import gTTS
from playsound import playsound
from pydub import AudioSegment
import os, sys

def main():
    """Main function that handles command-line arguments and invokes the text_to_speech function."""
    #argv
    if len(sys.argv) > 2:
        # The text that you want to convert to audio
        mytext = sys.argv[1]
        # Language in which you want to convert
        language = sys.argv[2]
    elif len(sys.argv) == 2:
        mytext = sys.argv[1]
        language = 'en'
    else:
        mytext = 'Hello there!'
        language = 'en'

    text_to_speech(mytext, lang = language, play = True)


def text_to_speech(text, file = 'speech.mp3', lang = 'en', play = False, remove = False, slow = False, convert = True):
    """
    Converts text to speech and handles audio file operations.

    Parameters
    ----------
    text : str
        The text to convert to speech.
    file : str, optional
        The filename to save the audio file as (default is 'speech.mp3').
    lang : str, optional
        The language code for the speech conversion (default is 'en').
    play : bool, optional
        If `True`, plays the generated audio file (default is `False`).
    remove : bool, optional
        If `True`, removes the audio file after playback (default is `False`).
    slow : bool, optional
        If `True`, speaks the text slowly (default is `False`).
    convert : bool, optional
        If `True`, converts the file to a format specified by the file extension, if different from 'mp3' (default is `True`).
    """
    myobj = gTTS(text = text, lang = lang, slow = slow)

    # Saving the converted audio in a mp3 file named
    with open(file, 'wb') as f:
        myobj.write_to_fp(f)

    #playing the audio file
    if play:
        playsound(file)

    if remove:
        os.remove(file)
    elif convert and '.' in file and file.split('.')[-1] != 'mp3':
        sound = AudioSegment.from_mp3(file)
        sound.export(file, format = file.split('.')[-1])


if __name__ == '__main__':
    main()
