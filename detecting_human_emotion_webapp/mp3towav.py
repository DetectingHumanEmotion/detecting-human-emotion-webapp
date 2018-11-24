from pydub import AudioSegment
import os
from shutil import copy2

def mp3_to_wav(file):
    print(os.path.isfile(file))
    print(file)
    # sound = AudioSegment.from_mp3(file)
    sound = AudioSegment.from_file(file,"mp3")
    print(sound.export(os.path.dirname(file)+"test_audio_files.wav", format ="wav"))

def mp4_to_wav(file):
    print(os.path.isfile(file))
    sound = AudioSegment.from_file(file, "mp3")
    sound.export(os.path.dirname(file) +"test_audio_files.mp3",format="mp3")


# file = "uploads/trial_lie_002_16.wav"
# # # print(os.path.dirname(file))
# # print(os.path.isfile(file))
# # print(os.path.dirname(os.path.realpath(__file__)))
# # mp3_to_wav(file)
print(os.path.dirname(os.path.realpath(__file__)))
file = "uploads/trial_lie_001.mp4"
file = "uploads/trial_lie_002.wav"
file = "uploads/test_audio_files.mp3"

# mp4_to_wav(file)
# copy2(file,"uploads/testnesssss.mp3")

mp3_to_wav(file)