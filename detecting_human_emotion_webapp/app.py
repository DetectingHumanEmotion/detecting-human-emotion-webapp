from flask import render_template, redirect,url_for
from detecting_human_emotion_webapp import app
from detecting_human_emotion_webapp.forms import UserInfoForm
# from deception_detection.audio.paura2 import recordAudioSegments



import os
import platform

users = []

if platform.system() is "Windows":
    from .user import User
    QUESTIONS = 'detecting_human_emotion_webapp/questions.txt'
else:
    from user import User

    QUESTIONS = 'questions.txt'

class questions:

    def __init__(self,questions):
        self.questions = questions
        self.currentQuestion = 0

    def getSize(self):
        return len(self.questions)

    def getCurrentQuestion(self):
        question = self.questions[self.currentQuestion]
        self.currentQuestion += 1

        return question


#This is the python script that should be ran n the html code
def recordAudioSegments():
    MODEL = "deceptionSvm_edited"
    BLOCKSIZE = .10
    FS = 16000
    SHOWSPECTOGRAM = True
    SHOWCHROMOGRAM = True
    RECORDACTIVITY = True
    ALGORITHM = "svm"
    #
    recordAudioSegments(BLOCKSIZE=BLOCKSIZE, model=MODEL, algorithm=ALGORITHM, Fs=FS, showSpectrogram=SHOWSPECTOGRAM,
                        showChromagram=SHOWCHROMOGRAM, recordActivity=RECORDACTIVITY)

#
@app.route("/", methods=["GET"])
def userInfo():
    header = 'Get User Info'
    userInfo = UserInfoForm()
    template_name = "get_user_info.html"
    return render_template(template_name_or_list=template_name, userInfoForm=userInfo, title=header)


@app.route("/", methods=["POST"])
def userInfoPost():
    userInfo = UserInfoForm()

    users.append(User(firstname=userInfo.first_name.data, lastname=userInfo.last_name.data, race=userInfo.race.data,
                      gender=userInfo.gender.data, age=userInfo.age.data))
    # this is an example how you print data from a form
    return redirect("/detecting")


@app.route("/detecting", methods=["GET"])
def recording_start_get():
    header = "Start Detecting Human Emotion"
    template = "startprompt.html"

    prompt = "After clicking on the start button you will be asked a series of question. Once you have read the question please answer to the best of your ability and alaborate on your response."

    return render_template(template_name_or_list=template, header = header, prompt=prompt)

@app.route("/detecting",methods=["POST"])
def recording_start_post():
    # questions = getListFromTextFile(QUESTIONS)
    # print(questions)
    return redirect(url_for('question', questionNumber = 0))

@app.route("/detecting/<int:questionNumber>", methods=["GET"])
def question(questionNumber):

    questions = getListFromTextFile(QUESTIONS)
    header = f'Question {questionNumber}'
    template_name = "questions.html"

    q= questions[questionNumber]


    return render_template(template_name_or_list=template_name,title=header,question = q, numberOfQuestions = str(len(questions)),currentQuestionNumber = str(questionNumber ))

#

@app.route("/detecting/<int:questionNumber>", methods=["POST"])
def question_post(questionNumber):

    questions = getListFromTextFile(QUESTIONS)
    questionNumber += 1
    if questionNumber < len(questions):
        return redirect(url_for('question', questionNumber = questionNumber))
    else:
        return redirect("/results")

@app.route("/results",methods=["GET"])
def resultsPage():
    header = 'Results Page'
    # userInfo = UserInfoForm()
    template_name = "results_page.html"
    #passing in as an array
    data = getLineFromTextFile(QUESTIONS).split("\n")
    return render_template(template_name_or_list=template_name, data = data, title = header)

# @app.route("/detecting", methods=["GET"])
# def home():
#
#     header = 'Detecting Human Emotion'
#
#     data = getListFromTextFile(QUESTIONS)
#     users[-1].questions = data
#     user = users[-1]
#
#
#
#     print(users[-1].print_data())
#
#     template_name = "index.html"
#     return render_template(template_name_or_list=template_name,user = user, data=data, title=header)
#
# @app.route("/detecting", methods=["POST"])
# def homePost():
#     print("testing that it posted")




def getLineFromTextFile(fileName):
    data = ''
    with open(fileName, 'r') as file:
        for line in file:
            data += line

    return data
def getListFromTextFile(fileName):
    l = []
    with open(fileName, 'r') as file:
        for line in file:
            formatted_line = line.strip('\n')
            l.append(formatted_line)

    return l



if __name__ == '__main__':
    app.run()
