from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import session
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import scrape
app = Flask(__name__)
username = "laurafelix2026"
password = "Papo662607004"
url = f"mongodb+srv://{username}:{password}@database.nqpknhe.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(url, server_api=ServerApi('1'))

db = client.database 

user = db.user

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

clubs = scrape.open()

#redirect(url_for('signup', var=var))
# -- Initialization section --
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template("login_required.html")
    else:
        if request.form['button-choice'] == "login":
            return redirect(url_for('signup', user_in = False))
            #return render_template("signup.html", user_in = False)
        else:
            return redirect(url_for('login', clubs=clubs, user_in = False, validNU=True))

@app.route('/login', methods=['GET', 'POST'] )
def login():
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
        # return render_template("homepage.html")
    else:
        return render_template("login.html", clubs=clubs, user_in = False, validNU=True)

@app.route('/signup', methods=['GET', 'POST'] )
def signup():
    if request.method == 'POST':
        all_users = list(user.find({}))
        if all_users:
            for i in all_users:
                if request.form["email"].lower() == i["email"].lower():
                    if request.form["password"].lower() == i["password"].lower():
                        return redirect(url_for('homepage',name=i["username"]))
                    else:
                        return render_template("signup.html", email_bool = True, password_bool=False)

            return render_template("signup.html",  email_bool = False, password_bool=True) 
        return render_template("signup.html",  email_bool = False, password_bool=True) 
    else:
        return render_template("signup.html", email_bool=True, password_bool=True)

@app.route('/homepage/<name>', methods=['GET', 'POST'])
def homepage(name):
    if request.method == 'POST':
        return render_template("homepage.html")
    else:
        username = user.find_one({'username': name})
        if username:
            return render_template("homepage.html", user=username)
        
        return "USER NOT FOUND! DUMBASS."




if __name__ == '__main__':
    app.run()