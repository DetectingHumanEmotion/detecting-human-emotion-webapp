from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def home():
    data = getLineFromTextFile('Questions.rtf')

    return render_template('index.html', data = data)


def getLineFromTextFile(FileName):
    data = ''

    with open(FileName, 'r') as file:

        for line in file:
            data += line

    return data


if __name__ == '__main__':
    app.run()
