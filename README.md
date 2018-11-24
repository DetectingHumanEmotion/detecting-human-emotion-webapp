# Detecting Human Emotion
This repository will contain the project work done by the members of Detecting Human Emotion throughout the course of the Fall 2018 semester in SE 195B.

## Environment Installation 
### Linux OS
1. sudo apt-get install portaudio19-dev
2. brew install libmagic

### Mac OS
1. brew install portaudio

### Windows OS
should work without any of the above installs

## Python Library Installation
This project was designed to take advantage of virtual environments. We use Pipenv for our Python Virtual Environment. 

### How to install Python dependencies 
1. Clone project: https://github.com/DetectingHumanEmotion/detecting-human-emotion-webapp.git
2. Set up virtual environment with the project. [How to use Pipenv](https://github.com/DetectingHumanEmotion/detecting-human-emotion-webapp/wiki)
3. Once the virtual environment has been created, it should download all the required Python libraries from the pipfile. The pipfile contains all the Python libraries needed to run the project.
4. If you have a problem installing hmmlearn run the following command in cli:
python3 -m pip install hmmlearn


# Run realtime visual and audio deception detection
The following file path contains the python script that runs both the video and audio classification scripts using multiprocessing. Once the script has started, the video stream will begin (takes several seconds to start) then the audio stream will begin. This script was designed as a proof of concept for our deception detection in real time. The user can respond to questions that another person asks, the console will display the likely hood of the person being untruthful and their emotion.
1. Run handtracking-master/detect_multi_threaded.py <br/>
        `python3 handtracking-master/detect_multi_threaded.py`

# Webapp
The webapp is the location where user's can upload mp4, mp3, and wav files which will then display the deception and emotion results. This website has Single Sign On (Okta) implementation. To correctly enable login/logout and signup the URL with LocalHost not 127.0.0.1 should be used

1. Run the following python file as a flask app
2. Once flask app is running enter **LocalHost:5000** in the browser. NOTE **127.0.0.1:5000 will not work correctly with our Single Sign On (SSO) implementation.**
3. Sign in or sign up 
4. Navigate to the Upload page. (localhost:5000/upload)
5. Upload a file from your computer that you would like to test or use the audio test files included in this project. Test files are located in this directory training-data/deception-audio/test_audio_files.
6. Once you submit the file you will be directed to the results page which will show your results

# General Project Structure 
