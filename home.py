from flask import Flask, url_for, render_template, session, redirect, request, flash
import os
from termcolor import cprint

app = Flask(__name__)
app.secret_key = os.urandom(24)


@app.route('/')
def index():
    return "Index Page"


@app.route('/hello/')
@app.route('/hello<name>/')
def hello(name=None):
    return render_template("hello.html", name=name)


@app.route('/register')
def registering():
    return "注册网页"


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        session['username'] = request.form['username']
        session['password'] = request.form['password']
        from user import GeneralUser
        user = GeneralUser()

        # user.login_info['uid'] = session['username']
        # user.login_info["passwd"] = session['password']
        # user.login()

        flag = user.login(session['username'], session['password'])
        cprint("登录状况: {}".format(str(flag), 'red'))
        # print(session['username'], session['password'])
        if not flag:
            return redirect(url_for('hello'))
        else:
            return flag
    return render_template('index.html')


@app.route('/user/<username>')
def show_user_profile_by_username(username):
    return "用户 {} 的个人主页".format((username))


@app.route('/user/<int:userid>')
def show_user_profile_by_userid(userid):
    return "用户 {} 的个人主页".format(userid)


if __name__ == "__main__":
    app.run(host='localhost')
