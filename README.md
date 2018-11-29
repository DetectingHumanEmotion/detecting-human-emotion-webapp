# Detecting Human Emotion
This repository will contain the project work done by the members of Detecting Human Emotion throughout the course of the Fall 2018 semester in SE 195B.

# Project Structure 
This section contains highlights of the most important part's of the project.
* **deception_detection**: This section contains both audio and visual detection code.
    * audio: contains all the code needed to train detection models as well as testing
        * **detection-testing**: Directory contains all the testing conducted on deception and emotion testing with audio.
        * **audio_detection.py**: This is the script that was used to train models for both emotion and deception detection as well as provide testing for those models. It also can classify .wav files.
        * **paura2**: This script can run deception or emotion detection in real time.
    * **visual**: contains the code to run the facial deception detection.
        * **detect_multi_threading.py**: Run's the facial deception detection.
    * **run_deception_detection.py**: Run's both the audio emotion/deception detection and visual detection in real time.
* **detecting_human_emotion_webapp**: Contains the files for the website portion of our project.
    * **app.py**: This is the script that run's the website.
* **training-data**: Training data used for developing the audio emotion/deception detection models
    * **deception-audio**
        * **lie_audio**: raw data set that contains the lie audio (.wav files) used for deception detection model training.
        * **lie_audio_edited**: edited data which filtered out every other sounds besides the person being questioned. This data set was used to trained the edited deception detection models.
        * **testing_data**: contains all the testing files used for testing deception.
        * **truth_audio**: truth data set used to train the audio deception detection.
    * **Pipfile**: File used for the pipenv (virtual environment). The Pipfile contains all the dependencies for the project. If the user does not want to use pipenv they can view the pipfile to find which requirements are needed for the project.
* **Realtim-visual-and-audio-deception-detection-demo.mp4**: Demo for the real time visual and audio deception detection.
* **website-demo.mp4**: demo of the website.
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
1. Run deception_detection/run_deception_detection.py <br/>
        `python3 deception_detection/run_deception_detection.py`


# Webapp
The webapp is the location where user's can upload mp4, mp3, and wav files which will then display the deception and emotion results. This website has Single Sign On (Okta) implementation. To correctly enable login/logout and signup the URL with LocalHost not 127.0.0.1 should be used

1. Run the following python file as a flask app
2. Once flask app is running enter **LocalHost:5000** in the browser. NOTE **127.0.0.1:5000 will not work correctly with our Single Sign On (SSO) implementation.**
3. Sign in or sign up 
4. Navigate to the Upload page. (localhost:5000/upload)
5. Upload a file from your computer that you would like to test or use the audio test files included in this project. Test files are located in this directory training-data/deception-audio/test_audio_files.
6. Once you submit the file you will be directed to the results page which will show your results



# Developers
* Tyler Bruno [(tybruno)](https://github.com/tybruno)
* Cindy Yee (CindyYee)
* Avani Bhatnagar (avanibhatnagar)
* Luis Arevalo (luisarevalo21)

# Contributions
[PyAudioAnalysis](https://github.com/tyiannak/pyAudioAnalysis) and [Paura2](https://github.com/tyiannak/paura) were developed by the director of machine learning at Behavioral Signals, Dr. Theodoros Giannakopoulos [(tyiannak)](https://github.com/tyiannak).


Giannakopoulos, T. (2015, December 11). PyAudioAnalysis: An Open-Source Python Library for Audio Signal Analysis. Retrieved from https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0144610


Deception Detection Data sets
Veronica Perez-Rosas, Mohamed Abouelenien, Rada Mihalcea, Mihai Burzo, Deception Detection using Real-life Trial Data, in Proceedings of the ACM International Conference on Multimodal Interaction (ICMI 2015), Seattle, November 2015. [[pdf](http://web.eecs.umich.edu/~mihalcea/papers/chao.cvpr15.pdf)]


Eye blink detection with OpenCV, Python, and dlib
by Adrian Rosebrock on April 24, 2017
https://www.pyimagesearch.com/2017/04/24/eye-blink-detection-opencv-python-dlib/


Victor Dibia, Real-time Hand-Detection using Neural Networks (SSD) on Tensorflow, (2017), GitHub repository, https://github.com/victordibia/handtracking
