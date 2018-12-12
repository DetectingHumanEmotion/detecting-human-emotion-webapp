from flask import render_template, redirect, url_for, request, g, flash, send_from_directory, jsonify, Response
from werkzeug.utils import secure_filename
import os
from okta import UsersClient
from flask_oidc import OpenIDConnect
import platform
from shutil import copy2
from pydub import AudioSegment

#local project directories
try:
    from detecting_human_emotion_webapp import app
    from detecting_human_emotion_webapp.forms import UserInfoForm
    from deception_detection.audio.audio_detection import classify_file, classify_file_process
    from detecting_human_emotion_webapp.camera import VideoCamera
    from detecting_human_emotion_webapp.parsing_tool import parse_deception_audio_result, parse_emotion_audio_result
    from detecting_human_emotion_webapp.file_conversion_tool import mp3_to_wav
except ModuleNotFoundError:
    print(ModuleNotFoundError)
    from .detecting_human_emotion_webapp import app
    from .detecting_human_emotion_webapp.forms import UserInfoForm
    from .deception_detection.audio.audio_detection import classify_file, classify_file_process
    from .detecting_human_emotion_webapp.camera import VideoCamera
    from .detecting_human_emotion_webapp.parsing_tool import parse_deception_audio_result, parse_emotion_audio_result




okta_client = UsersClient("https://dev-240328.oktapreview.com", "00Axbx-B_Dl0XMqSoQmZlURJv9djfBRjHQ9F2xQ4GT")


ALLOWED_EXTENSIONS = ['wav', 'mp3', 'mp4']

AUDIO_DECEPTION_DOMINATE_RESULT = {0: "Truth", 1: "Lie"}
AUDIO_EMOTION_DOMINATE_RESULT = {0: "Neatural", 1: "Calm", 2: "Happy", 3: "Sad", 4: "Angry", 5: "Fear", 6: "Disgust",
                                 8: "Surprise"}

video_camera = None
global_frame = None

oidc = OpenIDConnect(app)

if platform.system() is "Windows":
    QUESTIONS = 'detecting_human_emotion_webapp/questions.txt'
else:

    QUESTIONS = 'questions.txt'


@app.before_request
def before_request():
    """
    created by tybruno

    This function is for SSO (okta). Checks if user is logged in.
    :return: void
    """
    if oidc.user_loggedin:
        g.user = okta_client.get_user(oidc.user_getfield("sub"))
    else:
        g.user = None


class questions:

    def __init__(self, questions):
        self.questions = questions
        self.currentQuestion = 0

    def getSize(self):
        return len(self.questions)

    def getCurrentQuestion(self):
        question = self.questions[self.currentQuestion]
        self.currentQuestion += 1

        return question


@app.route('/record_status', methods=['POST'])
def record_status():
    global video_camera
    if video_camera is None:
        video_camera = VideoCamera()

    json = request.get_json()

    status = json['status']

    if status == "true":
        video_camera.start_record()
        print("recording started")
        return jsonify(result="started")
    else:
        video_camera.stop_record()
        return jsonify(result="stopped")


def video_stream():
    global video_camera
    global global_frame

    if video_camera is None:
        video_camera = VideoCamera()

    while True:
        frame = video_camera.get_frame()

        if frame is not None:
            global_frame = frame
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
        # else:
        #     print(global_frame)
        #     # yield (b'--frame\r\n'
        #     #        b'Content-Type: image/jpeg\r\n\r\n' + global_frame + b'\r\n\r\n')


@app.route('/video_viewer')
def video_viewer():
    return Response(video_stream(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route("/")
def index():
    if oidc.user_loggedin is False:
        return redirect("/login")
    else:
        return redirect("/home")


@app.route("/login")
@oidc.require_login
def login():

    # return redirect(url_for(".dashboard"))
    return redirect("/")


@app.route("/logout", methods=["GET", "POSt"])
@oidc.require_login
def logout():
    """
    created by tybruno

    logs out user from SSO (okta)
    :return: redirects the user to login page
    """
    oidc.logout()

    # return redirect(url_for(".login"))
    return redirect("/login")


@app.route("/getUserInfo", methods=["GET"])
def userInfo():
    """
    Gets user info
    :return:
    """
    header = 'Get User Info'
    userInfo = UserInfoForm()
    template_name = "get_user_info.html"
    return render_template(template_name_or_list=template_name, userInfoForm=userInfo, title=header)


@app.route("/getUserInfo", methods=["POST"])
def userInfoPost():
    """
    created by tybruno
    Gets info about the current user
    :return:
    """
    userInfo = UserInfoForm()
    g.user.profile.race = userInfo.race.data
    g.user.profile.gender = userInfo.gender.data
    g.user.profile.age = userInfo.age

    return redirect("/detecting")


@app.route("/detecting", methods=["GET"])
def recording_start_get():
    header = "Start Detecting Human Emotion"
    template = "startprompt.html"

    prompt = "After clicking on the start button you will be asked a series of question. Once you have read the question please answer to the best of your ability and alaborate on your response."

    return render_template(template_name_or_list=template, header=header, prompt=prompt)


@app.route("/detecting", methods=["POST"])
def recording_start_post():
    g.user.profile.questions = getListFromTextFile(QUESTIONS)
    print(g.user.profile.questions)
    return redirect(url_for('question', questionNumber=0))


@app.route(f"/detecting/<int:questionNumber>", methods=["GET"])
def question(questionNumber):
    g.user.profile.questions = getListFromTextFile(QUESTIONS)
    # questions = getListFromTextFile(QUESTIONS)
    header = f'Question {questionNumber + 1}'
    template_name = "questions.html"
    #
    q = g.user.profile.questions[questionNumber]

    return render_template(template_name_or_list=template_name, title=header, question=q,
                           numberOfQuestions=str(len(g.user.profile.questions)),
                           currentQuestionNumber=str(questionNumber + 1))


# send video recording file
@app.route("/detecting/<int:questionNumber>", methods=["POST"])
def question_post(questionNumber):
    g.user.profile.questions = getListFromTextFile(QUESTIONS)
    # questions = getListFromTextFile(QUESTIONS)
    questionNumber += 1
    print(questionNumber)
    if questionNumber < len(g.user.profile.questions):
        return redirect(url_for('question', questionNumber=questionNumber))
    else:
        return redirect("/results")


@app.route("/results", methods=["GET"])
def resultsPage():
    """

    :return:
    """
    header = 'Results Page'
    # userInfo = UserInfoForm()
    template_name = "results_page.html"

    # passing in as an array
    data = getLineFromTextFile(QUESTIONS).split("\n")
    return render_template(template_name_or_list=template_name, data=data, title=header)


@app.route("/home")
def home():
    """

    :return: dashboard html file
    """
    return render_template("home.html")


@app.route("/dashboard")
def dashboard():
    """
    Created by tybruno
    :return: dashboard html file
    """
    return render_template("dashboard.html")


def getLineFromTextFile(fileName):
    """
    created by luis


    :param fileName:
    :return:
    """
    data = ''
    with open(fileName, 'r') as file:
        for line in file:
            data += line

    return data


def getListFromTextFile(fileName):
    """
    Gets a list from at in a file
    :param fileName: the file that we are pulling the data from
    :return: list of the data in the file
    """

    l = []
    with open(fileName, 'r') as file:
        for line in file:
            formatted_line = line.strip('\n')
            l.append(formatted_line)

    return l


def allowed_file(filename):
    """
    Used to check if the uploaded file is a valid file type from the allowed extensions

    allowed extensions: .mp4, .mp3, and .wav
    :param filename: the file that is being checked for correct file type
    :return:
    """
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# this the uploading method
@app.route("/upload", methods=["GET"])
@oidc.require_login
def upload():
    """
    Developed by tybruno

    this allows the user to upload files to detect deception and emotion.

    File types supported: .mp4, .mp3, and .wav

    :return:
    """
    header = "Uploading a file"
    template = "uploading_page.html"

    prompt = "Here you can upload a file to detect lying and emotion"
    return render_template(template_name_or_list=template, header=header, prompt=prompt)


@app.route('/uploads/<filename>')
@oidc.require_login
def uploaded_file(filename):
    """
    Developed by tybruno

    :param filename: filename that will be uploaded
    :return: sends the uploaded file
    """
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)


def classify_audio(file, deception_model_path="../deception_detection/audio/deceptionGradientBoosting",
                   deception_algorithm="gradientboosting",
                   emotion_model_path="../deception_detection/audio/emotionExtraTrees", emotion_algorithm="extratrees"):
    """
    developed by tybruno

    Classifies audio file with the level of deception and emotion of the person recorded from the audio file.
    This function only supports .wav files
    :param file: audio file to be classified
    :param deception_model_path: The  model path to the deception model
    :param deception_algorithm: The algorithm used to train the deceptionn model
    :param emotion_model_path: The model path to the emotion model
    :param emotion_algorithm: The algorithm used to train the emotion model
    :return: results of deception and emotion classification
    """
    audio_deception_results = classify_file(file=file, trained_model_name=deception_model_path,
                                            trained_machine_algorithm=deception_algorithm)

    audio_emotion_results = classify_file(file=file, trained_model_name=emotion_model_path,
                                          trained_machine_algorithm=emotion_algorithm)

    return audio_deception_results, audio_emotion_results


def classify_audio_file(file):
    """
    developed by tybruno

    Classifies audio file. The classification will include deception and emotion classifications and returns the results for each.

    :param file: File that will be classifieded for deception and emotion
    :return: deception results and emotion results as a tuple.
    """

    audio_deception_results, audio_emotion_results = classify_audio(file)

    return audio_deception_results, audio_emotion_results


@app.route("/upload", methods=["POST"])
@oidc.require_login
def uploading():
    """
    tybruno

    Upload section where the user can upload video/audio files. These files will be classified with audio to check deception and emotion from the user in video/audio file.
    Upload only supports .mp4, .mp3, .wav files
    :return: file_upload_results template
    """

    saved_file_location = ""

    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)

    file = request.files['file']

    # if user does not select file, browser also
    # submit a empty part without filename
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)

    if file and allowed_file(file.filename):
        saved_file_location = os.path.join(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(file.filename)))
        print(os.getcwd())
        print(os.path.exists(saved_file_location))
        file.save(saved_file_location)

    print(saved_file_location)

    filename, extension = os.path.splitext(saved_file_location)

    if extension is ".mp4":
        mp3_conversion_file = os.path.join(filename, ".mp3")
        copy2(saved_file_location, mp3_conversion_file)
        mp3_to_wav(mp3_conversion_file)
        # audio_deception_results = classify_file(file=mp3_conversion_file, trained_machine_name=deception_model_path,trained_machine_algorithm=deception_algorithm)
        audio_deception_results, audio_emotion_results = classify_audio(file=mp3_conversion_file)
    elif extension is ".mp3":
        mp3_conversion_file = os.path.join(filename, ".mp3")
        mp3_to_wav(mp3_conversion_file)
        # audio_deception_results = classify_file(file=mp3_conversion_file, trained_machine_name=deception_model_path,trained_machine_algorithm=deception_algorithm)
        audio_deception_results, audio_emotion_results = classify_audio(file=mp3_conversion_file)

    else:
        audio_deception_results, audio_emotion_results = classify_audio(file=saved_file_location)

        # audio_deception_results = classify_file(file=saved_file_location, trained_machine_name=deception_model_path)

    audio_deception_results = parse_deception_audio_result(audio_deception_results)
    audio_emotion_results = parse_emotion_audio_result(audio_emotion_results)

    # SAVE FILE HERE WHICH WAS INPUTED
    results = {"audio_deception_detection": audio_deception_results, "audio_emotion_detection": audio_emotion_results}
    print(results)

    return render_template(template_name_or_list="file_upload_results.html", results=results)

if __name__ == '__main__':
    app.run(host="localhost", port=5000)
