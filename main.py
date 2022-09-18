import time
from flask import Flask, render_template, redirect, url_for, request, flash, jsonify, session
from pymongo import MongoClient
from forms import GetStarted, SignUp, SignIn, SignOut
from functools import wraps
from turbo_flask import Turbo
import uuid
import random

app = Flask(__name__)
turbo = Turbo(app)
app.secret_key = 'HTM'
cluster = "mongodb://localhost:27017"
client = MongoClient(cluster)
db = client['practice']
htm_data = db.htm

male_pic = ['https://images.unsplash.com/photo-1500648767791-00dcc994a43e?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxzZWFyY2h8Mnx8bWFsZSUyMGF2YXRhcnxlbnwwfHwwfHw%3D&auto=format&fit=crop&w=1000&q=60', \
            'https://images.unsplash.com/photo-1566492031773-4f4e44671857?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxzZWFyY2h8M3x8bWFsZSUyMGF2YXRhcnxlbnwwfHwwfHw%3D&auto=format&fit=crop&w=1000&q=60',\
            'https://images.unsplash.com/photo-1570295999919-56ceb5ecca61?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxzZWFyY2h8NHx8bWFsZSUyMGF2YXRhcnxlbnwwfHwwfHw%3D&auto=format&fit=crop&w=1000&q=60', \
            'https://images.unsplash.com/photo-1568602471122-7832951cc4c5?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxzZWFyY2h8NXx8bWFsZSUyMGF2YXRhcnxlbnwwfHwwfHw%3D&auto=format&fit=crop&w=1000&q=60', \
            'https://images.unsplash.com/photo-1535713875002-d1d0cf377fde?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxzZWFyY2h8N3x8bWFsZSUyMGF2YXRhcnxlbnwwfHwwfHw%3D&auto=format&fit=crop&w=1000&q=60', \
            'https://images.unsplash.com/photo-1534030347209-467a5b0ad3e6?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=387&q=80', \
            'https://images.unsplash.com/photo-1463453091185-61582044d556?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxzZWFyY2h8OXx8Z2F5JTIwbWFsZSUyMGF2YXRhcnxlbnwwfHwwfHw%3D&auto=format&fit=crop&w=1000&q=60', \
            'https://images.unsplash.com/photo-1440133197387-5a6020d5ace2?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxzZWFyY2h8MTB8fGdheSUyMG1hbGUlMjBhdmF0YXJ8ZW58MHx8MHx8&auto=format&fit=crop&w=1000&q=60', \
            ]

female_pic = ['https://images.unsplash.com/photo-1591865501237-e9ae721d7ba7?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxzZWFyY2h8Mnx8ZmVtYWxlJTIwYXZhdGF5fGVufDB8fDB8fA%3D%3D&auto=format&fit=crop&w=1000&q=60', \
            'https://images.unsplash.com/photo-1441123694162-e54a981ceba5?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxzZWFyY2h8M3x8ZmVtYWxlJTIwYXZhdGF5fGVufDB8fDB8fA%3D%3D&auto=format&fit=crop&w=1000&q=60', \
            'https://images.unsplash.com/photo-1513097847644-f00cfe868607?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxzZWFyY2h8NXx8ZmVtYWxlJTIwYXZhdGF5fGVufDB8fDB8fA%3D%3D&auto=format&fit=crop&w=1000&q=60', \
            'https://images.unsplash.com/photo-1585220809051-f34c47ab0554?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxzZWFyY2h8N3x8ZmVtYWxlJTIwYXZhdGF5fGVufDB8fDB8fA%3D%3D&auto=format&fit=crop&w=1000&q=60', \
            'https://images.unsplash.com/photo-1488228469209-c141f8bcd723?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxzZWFyY2h8OHx8ZmVtYWxlJTIwYXZhdGF5fGVufDB8fDB8fA%3D%3D&auto=format&fit=crop&w=1000&q=60', \
            'https://images.unsplash.com/photo-1481824429379-07aa5e5b0739?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxzZWFyY2h8OXx8ZmVtYWxlJTIwYXZhdGF5fGVufDB8fDB8fA%3D%3D&auto=format&fit=crop&w=1000&q=60', \
            'https://images.unsplash.com/photo-1464863979621-258859e62245?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxzZWFyY2h8MTB8fGZlbWFsZSUyMGF2YXRheXxlbnwwfHwwfHw%3D&auto=format&fit=crop&w=1000&q=60', \
            'https://images.unsplash.com/photo-1492106087820-71f1a00d2b11?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxzZWFyY2h8MTF8fGZlbWFsZSUyMGF2YXRheXxlbnwwfHwwfHw%3D&auto=format&fit=crop&w=1000&q=60', \
            ]

# match function
def common_member(a, b):
    a_set = set(a)
    b_set = set(b)
    return a_set & b_set


class User:
    def start_session(self, user):
        session['logged_in'] = True
        session['user'] = user
        return jsonify(user), 200

    def signup(self, user_data):
        user = {
            "_id": user_data['_id'],
            "name": user_data['name'],
            "email": user_data['email'],
            "gender": user_data['gender'],
            "dob": user_data['dob'],
            "height": user_data['height'],
            "profession": user_data['profession'],
            "profile": user_data['profile'],
            "category": user_data['category'],
            "interest": user_data['interest'],
            "password": user_data['password']
        }
        htm_data.insert_one(user)
        flash("")
        return self.start_session(user)

    def signin(self, user_data):
        user = {
            "_id": user_data['_id'],
            "name": user_data['name'],
            "email": user_data['email'],
            "gender": user_data['gender'],
            "dob": user_data['dob'],
            "passion": user_data['height'],
            "profession": user_data['profession'],
            "profile": user_data['profile'],
            "category": user_data['category'],
            "interest": user_data['interest'],
            "password": user_data['password']
        }
        return self.start_session(user)

    def details(self):
        return session['user']

    def signout(self):
        session.clear()
        flash("Signed Out")
        return redirect('/')

@app.after_request
def after_request(response):
    # if the response has the turbo-stream content type, then append one more
    # stream with the contents of the alert section of the page
    if response.headers['Content-Type'].startswith(
            'text/vnd.turbo-stream.html'):
        response.response.append(turbo.update(
            render_template('alert.html'), 'alert').encode())
        if response.content_length:
            response.content_length += len(response.response[-1])
    return response


def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            return redirect("/")
    return wrap


@app.route("/", methods=['GET', 'POST'])
def index():
    begin = GetStarted()
    if begin.validate_on_submit():
        return redirect(url_for('login'))
    return render_template('index.html', begin=begin)


@app.route("/register", methods=['GET', 'POST'])
def sign_up_in():
    signup = SignUp()
    user = User()
    name_error = ''
    if signup.signup.data and signup.validate():
        print('Sign Up')
        category = []
        name = request.form['name']
        email = request.form['email']
        gender = request.form['gender']
        dob = request.form['dob']
        height = request.form['height']
        profession = request.form['profession']
        interest = request.form['interest']
        password = request.form['password']
        for x in request.form.getlist('category'):
            category.append(x)
        confirm_password = request.form['confirm_password']
        result = htm_data.find_one({'email': email})

        if result is not None:
            flash("User already exists")

        elif password != confirm_password:
            flash("Passwords don't match")

        else:
            if(gender == 'Male'):
                choice = random.choice(male_pic)
            elif(gender == 'Female'):
                choice = random.choice(female_pic)
            else:
                choice = 'https://www.computerhope.com/jargon/g/guest-user.jpg'
            user_data = {
                '_id': uuid.uuid4().hex,
                'name': name,
                'email': email,
                'profile': choice,
                'gender': gender,
                "dob": dob,
                "height": height,
                "profession": profession,
                'interest': interest,
                'category': category,
                'password': password
            }
            user.signup(user_data)
            time.sleep(1)
            return redirect(url_for('profile'))

        if turbo.can_stream():
            return turbo.stream(turbo.update(name_error, 'name_error'))
    return render_template("register.html", signup=signup)


@app.route("/login/", methods=['GET', 'POST'])
def login():
    signin = SignIn()
    user = User()
    name_error = ''
    if signin.signin.data and signin.validate():
        print('Sign In')
        email = request.form['email']
        password = request.form['password']
        user_data = htm_data.find_one({'email': email})
        if user_data is None:
            flash("No such email exist")
        elif password != user_data['password']:
            flash("Incorrect Password")
        else:
            user.signin(user_data)
            time.sleep(1)
            return redirect(url_for('profile'))

        if turbo.can_stream():
            return turbo.stream(turbo.update(name_error, 'name_error'))
    return render_template("sign_in.html", signin=signin)

@app.route("/profile", methods=['GET', 'POST'])
@login_required
def profile():
    signout = SignOut()
    user = User()
    if signout.signout() and request.form.get('btn') == 'Sign Out':
        user.signout()
        time.sleep(1)
        return redirect(url_for('index'))
    if signout.find_match() and request.form.get('btn') == 'Find Match':
        return redirect(url_for('find'))
    return render_template('profile.html', signout=signout)


@app.route("/find/", methods=['GET', 'POST'])
@login_required
def find():
    user = User()
    match_list = []
    category = session['user']['category']
    for x in htm_data.find():
        if(x['email'] != session['user']['email'] and common_member(x['category'], category) and x['gender'] == session['user']['interest'] and x['interest'] == session['user']['gender']):
            match_list.append(x)
    return render_template('match.html', match_list=match_list)


@app.route("/signout", methods=['GET', 'POST'])
def signout():
    user = User()
    return user.signout()


if __name__ == "__main__":
    app.run(use_reloader=True)
