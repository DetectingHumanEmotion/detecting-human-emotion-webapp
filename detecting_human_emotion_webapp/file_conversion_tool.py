from pydub import AudioSegment
import os
"""
Created by Tyler Bruno
The purpose of this file is to store all the file conversion functions

"""

def mp3_to_wav(file):
    """
    developed by tybruno

    Converts mp3 files to .wav files

    :param file: mp3 file that is being converted
    :return: .wav file
    """
    print(os.path.isfile(file))
    print(file)
    # sound = AudioSegment.from_mp3(file)
    sound = AudioSegment.from_file(file,"mp3")
    print(sound.export(os.path.dirname(file)+"test.wav", format ="wav"))

def mp4_to_wav(file):
    """
    developer: tybruno
    converts .mp4 files to .wav files.
    :param file: .mp4 file that will be converted to .wav
    :return: .wav file
    """
    print(os.path.isfile(file))
    sound = AudioSegment.from_file(file, "mp3")
    sound.export(os.path.dirname(file) +"test.mp3",format="mp3")

