from flask import Flask, request
import git


app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Developing3...'


@app.route('/update_server', methods=['POST'])
def webhook():
    if request.method == 'POST':
        repo = git.Repo('telegram-king')
        origin = repo.remotes.origin
        origin.pull()

        return 'Updated PythonAnywhere successfully', 200
    else:
        return 'Wrong event type', 400
