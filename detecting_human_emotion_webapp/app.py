from flask import render_template
from detecting_human_emotion_webapp import app
import os



@app.route("/",methods=["GET"])
def home():

    header = 'Detecting Human Emotion'
    data = getLineFromTextFile('detecting_human_emotion_webapp/questions.txt')
    print(data)
    template_name = "index.html"
    return render_template(template_name_or_list=template_name,data =data, title = header)


def getLineFromTextFile(fileName):
    data = ''

    with open(fileName, 'r') as file:

        for line in file:
            data += line

    return data


if __name__ == '__main__':
    app.run()
