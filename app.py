from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import session
from pymongo import MongoClient

# -- Initialization section --
app = Flask(__name__)

if __name__ == '__main__':
    app.run()