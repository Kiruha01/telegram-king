from flask import Flask, request
import git
from logic import database


app = Flask(__name__)


@app.route('/')
def hello():
    return database.getall()

@app.route('/add/<name>/')
def hello_world(name):
    creator = request.args.get("creator")
    if creator:
        database.add(name, creator)
        return 'ok'
    else:
        return 'error'


@app.route('/update_server', methods=['POST'])
def webhook():
    if request.method == 'POST':
        repo = git.Repo('telegram-king')
        origin = repo.remotes.origin
        origin.pull()

        return 'Updated PythonAnywhere successfully', 200
    else:
        return 'Wrong event type', 400
