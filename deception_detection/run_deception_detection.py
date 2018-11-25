
from threading import Thread
from multiprocessing import Process
import os

try:
    from deception_detection.audio.paura2 import recordAudioSegments
    from deception_detection.visual.detect_multi_threaded import record
except ModuleNotFoundError:
    from .deception_detection.audio.paura2 import recordAudioSegments
    from .deception_detection.visual.detect_multi_threaded import record


# try:
#     print("here")
#     from deception_detection.visual.detect_multi_threaded import record
# except ModuleNotFoundError:
#     from .deception_detection.audio.paura2 import recordAudioSegments
#     from .deception_detection.visual.detect_multi_threaded import record


def run_audio_detection():
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

def run_deception_detection():



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

    ## This is the Threading way
    # try:
    #     thread1 = threading.Thread(target=record)
    #
    #     thread2 = threading.Thread(target=run)
    #
    #
    #     thread1.start()
    #      print("Thread 1 started")
    #     thread2.start()
    #     print("Thread 2 started")
    #
    #     thread1.join()
    #     thread2.join()
    #
    # except:
    #     print("Thread failed")
if __name__ == '__main__':
    run_deception_detection()