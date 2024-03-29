from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import session
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from flask_pymongo import PyMongo
import scrape


app = Flask(__name__)
username = "laurafelix2026"
password = "Papo662607004"
url = f"mongodb+srv://{username}:{password}@userinfo.nqpknhe.mongodb.net/database"
app.config["MONGO_URI"] = url
client = PyMongo(app)

db = client.db 

user = db.user

jobs_ = db.jobs

clubs = scrape.open()

#redirect(url_for('signup', var=var))
# -- Initialization section --
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template("login_required.html")
    else:
        if request.form['button-choice'] == "login":
            return redirect(url_for('login', user_in = False))
        else:
            return redirect(url_for('signup'))


@app.route('/signup', methods=['GET', 'POST'] )
def signup():
    #this is signup 
    if request.method == 'POST':
        
        all_users = list(user.find({}))
        
        dict_user = {"name": request.form['firstname'], "lastname": request.form['lastname'], "birthday": request.form['birthday'], 
                    "email": request.form['email'], "major": request.form['primajor'], "club":request.form['clubby'], "password": request.form['password'], "username": request.form["firstname"]+request.form["lastname"]+request.form["birthday"][0:2]}
        
        bool_check = False
        for i in all_users:
            if dict_user["email"].lower() == i["email"].lower():
                bool_check = True

        if bool_check:
            # return redirect(url_for('login', clubs=scrape.open_site(), user_in = True, validNU=True))
            return render_template("login.html", clubs=clubs, user_in = True, validNU=True)

        if "u.northwestern.edu" not in dict_user["email"].lower():
            return render_template("login.html", clubs=clubs, user_in = False, validNU=False)
        
        user.insert_one(dict_user)

        return redirect(url_for('homepage', name=dict_user["username"]))
    else:
        return render_template("login.html", clubs=clubs, user_in = False, validNU=True)

@app.route('/login', methods=['GET', 'POST'] )
def login():
    if request.method == 'POST':  
        all_users = list(user.find({}))
        for i in all_users:
            if request.form["email"].lower() == i["email"].lower():
                if request.form["password"].lower() == i["password"].lower():
                    return redirect(url_for('homepage',name=i["username"]))
                else:
                    return render_template("signup.html", email_bool = True, password_bool=False)

        return render_template("signup.html",  email_bool = False, password_bool=True) 
    else:
        return render_template("signup.html", email_bool=True, password_bool=True)

@app.route('/homepage/<name>', methods=['GET', 'POST'])
def homepage(name):
    if request.method == 'POST':
        return render_template("homepage.html", url=url_for("homepage", name=name), url_jobs=url_for("jobs", name=name))
    else:
        username = user.find_one({"username": name})
        if username:
            return render_template("homepage.html", user=username, url=url_for("homepage", name=name), url_jobs=url_for("jobs", name=name))
        
        return "USER NOT FOUND! DUMBASS."

@app.route('/jobs/<name>', methods=['GET', 'POST'])
def jobs(name):
    all_jobs = list(jobs_.find({}))
    if request.method == 'GET':
        return render_template("jobs.html", jobs=all_jobs, name=name, url=url_for("homepage", name=name), url_jobs=url_for("jobs", name=name))
    else:
        return redirect(url_for('insert_jobs', name=name))

@app.route("/insert_jobs/<name>", methods=['GET', 'POST'])
def insert_jobs(name):
    username = user.find_one({"username": name})
    if username:
        if request.method == 'POST':
            job_dictionary = {
                    "Position": request.form["position"], 
                    "Company": request.form["company"], 
                    "Timeline": request.form["timeline"],
                    "Description": request.form["description"], 
                    "Link": request.form["link"],
                    "Added by": username['name']+" "+username['lastname'], 
                    "Genre": request.form["genre"],
                    "Year": request.form["year"],
                    "Img": scrape.logo_search(request.form["company"])
                }

            jobs_.insert_one(job_dictionary)
                
            return redirect(url_for("jobs", name=name))
        else:
            return render_template("insert_jobs.html", user=username, url=url_for("homepage", name=name), url_jobs=url_for("jobs", name=name), url_insert=url_for("insert_jobs", name=name))
    return "USER NOT FOUND!"        





if __name__ == '__main__':
    app.run()