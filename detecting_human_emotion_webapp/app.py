from flask import render_template, redirect
from detecting_human_emotion_webapp import app
from detecting_human_emotion_webapp.forms import UserInfoForm
from .user import User
import os

users = []


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
def home():

    header = 'Detecting Human Emotion'
    data = getListFromTextFile('detecting_human_emotion_webapp\questions.txt')
    users[-1].questions = data
    user = users[-1]



    print(users[-1].print_data())

    template_name = "index.html"
    return render_template(template_name_or_list=template_name,user = user, data=data, title=header)

@app.route("/detecting", methods=["POST"])
def homePost():
    print("testing that it posted")

@app.route("/dashboard", methods=["GET"])
def dashBoard():
    template_name = "dashboard.html"
    return render_template(template_name_or_list=template_name)


@app.route("/results", methods=["GET"])
def resultsPage():
    header = 'Results Page'
    # userInfo = UserInfoForm()
    template_name = "results_page.html"
    data = getLineFromTextFile('detecting_human_emotion_webapp\questions.txt')

    return render_template(template_name_or_list=template_name, data=data, title=header)


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
