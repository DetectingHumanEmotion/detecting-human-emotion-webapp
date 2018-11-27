
from threading import Thread
from multiprocessing import Process
import os


# from audio.paura2 import recordAudioSegments
# from deception_detection.visual.detect_multi_threaded import record

try:
    from deception_detection.audio.paura2 import recordAudioSegments
    from deception_detection.visual.detect_multi_threaded import record
except ModuleNotFoundError:
    from .deception_detection.audio.paura2 import recordAudioSegments
    from .deception_detection.visual.detect_multi_threaded import record

"""
created by tybruno

This file is used to run both the visual and audio deception detection in realtime 
"""


def run_audio_detection():
    """
    created by tybruno

    Will perform audio deception and emotion classification in real time for
    :return: Raw results of both the classifiations
    """
    # model and algorithm for deception detection
    DECEPTION_MODEL = "audio/deceptionSvm_edited"
    ALGORITHM = "svm"

    # Model and algorithm for emotion detection
    EMOTION_MODEL = "audio/emotionExtraTrees"
    EMOTION_ALGORITHM = "extratrees"
    BLOCKSIZE = .10
    FS = 16000
    SHOWSPECTOGRAM = True
    SHOWCHROMOGRAM = True
    RECORDACTIVITY = True

    return recordAudioSegments(BLOCKSIZE=BLOCKSIZE, model=DECEPTION_MODEL, algorithm=ALGORITHM, emotion_model=EMOTION_MODEL,
                               emotion_algorithm=EMOTION_ALGORITHM, Fs=FS, showSpectrogram=SHOWSPECTOGRAM,
                               showChromagram=SHOWCHROMOGRAM, recordActivity=RECORDACTIVITY)

def deception_detection_multiprocessing():
    """
    developed by tybruno

    does audio and video deception detection in real time using multiprocessing
    :return: void
    """
    ## Multiprocessing way
    try:
        process1 = Process(target=record)

        process2 = Process(target=run_audio_detection)

        process1.start()
        print("Proecss 1 started")
        process2.start()
        print("Process 2 started")

        process1.join()
        process2.join()

    except:
        print("process failed")

def deception_detection_threading():
    """
    developed by tybruno

    does audio and video deception detection in real time using threading
    :return: void
    """
    try:
        thread1 = Thread(target=record)

        thread2 = Thread(target=run_audio_detection)


        thread1.start()
        print("Thread 1 started")
        thread2.start()
        print("Thread 2 started")

        thread1.join()
        thread2.join()

    except:
        print("Thread failed")

def run_deception_detection(process="threading"):
    """
    Created by tybruno

    This function runs both the visual and audio deception classification in real time using either multiprocessing or threading.
    :return:
    """
    if process is "threading":
        deception_detection_threading()
    else:
        deception_detection_multiprocessing()


if __name__ == '__main__':
    run_deception_detection()