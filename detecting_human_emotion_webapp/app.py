from flask import render_template, redirect,url_for, g
from detecting_human_emotion_webapp import app
from detecting_human_emotion_webapp.forms import UserInfoForm
from okta import UsersClient
from flask_oidc import OpenIDConnect
import platform
okta_client = UsersClient("https://dev-240328.oktapreview.com", "00Axbx-B_Dl0XMqSoQmZlURJv9djfBRjHQ9F2xQ4GT")

oidc = OpenIDConnect(app)
if platform.system() is "Windows":

    QUESTIONS = 'detecting_human_emotion_webapp/questions.txt'
else:

    QUESTIONS = 'questions.txt'

@app.before_request
def before_request():
    if oidc.user_loggedin:
        g.user = okta_client.get_user(oidc.user_getfield("sub"))
    else:
        g.user = None


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


@app.route("/")
def index():

    if oidc.user_loggedin is False:
        return redirect("/login")
    else:
        return redirect("/detecting")


@app.route("/login")
@oidc.require_login
def login():
    # return redirect(url_for(".dashboard"))
    return redirect("/detecting")


@app.route("/logout", methods=["GET","POSt"])
@oidc.require_login
def logout():
    oidc.logout()

    # return redirect(url_for(".login"))
    return redirect("/login")

@app.route("/getUserInfo", methods=["GET"])
def userInfo():
    header = 'Get User Info'
    userInfo = UserInfoForm()
    template_name = "get_user_info.html"
    return render_template(template_name_or_list=template_name, userInfoForm=userInfo, title=header)


@app.route("/getUserInfo", methods=["POST"])
def userInfoPost():
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

    return render_template(template_name_or_list=template, header = header, prompt=prompt)

@app.route("/detecting",methods=["POST"])
def recording_start_post():


    g.user.profile.questions = getListFromTextFile(QUESTIONS)
    print(g.user.profile.questions)
    return redirect(url_for('question', questionNumber = 0))

@app.route(f"/detecting/<int:questionNumber>", methods=["GET"])
def question(questionNumber):
    g.user.profile.questions = getListFromTextFile(QUESTIONS)
    # questions = getListFromTextFile(QUESTIONS)
    header = f'Question {questionNumber + 1}'
    template_name = "questions.html"
    #
    q= g.user.profile.questions[questionNumber]

    return render_template(template_name_or_list=template_name,title=header,question=q, numberOfQuestions = str(len(g.user.profile.questions)),currentQuestionNumber = str(questionNumber + 1))


@app.route("/detecting/<int:questionNumber>", methods=["POST"])
def question_post(questionNumber):
    g.user.profile.questions = getListFromTextFile(QUESTIONS)
    # questions = getListFromTextFile(QUESTIONS)
    questionNumber += 1
    print(questionNumber)
    if questionNumber < len(g.user.profile.questions):
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


@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

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
    app.run(host="localhost",port= 5000)
