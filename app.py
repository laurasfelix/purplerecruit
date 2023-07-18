from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import session
from pymongo import MongoClient

# -- Initialization section --
app = Flask(__name__)
@app.route('/')
@app.route('/login_required')
def index():
    return render_template("login_required.html")

if __name__ == '__main__':
    app.run()