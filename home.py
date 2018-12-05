from flask import Flask, session, request, render_template, redirect, url_for
import os
from termcolor import cprint
from gameflask.code.user import GeneralUser

# 传递根目录
app = Flask(__name__)

# session
app.secret_key = os.urandom(24)


# 用于测试的hello
@app.route('/hello/')
@app.route('/hello<name>/')
def hello(name=None):
    return render_template("hello.html", name=name)


# 默认路径访问登录页面
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/register')
def registering():
    return "注册网页"


# 默认路径访问用户页面
@app.route('/main/')
def main():
    return render_template('main.html')


'''
index点击Login触发的路由事件
session读取网页发来的表单信息（Username，Password）
判断信息（弹窗，直接返回原网页）
返回用户页面main.html
'''


@app.route('/login', methods=['POST', 'GET'])
def getLoginRequest():
    if request.method == 'POST':
        session['username'] = request.form['username']
        session['password'] = request.form['password']
        user = GeneralUser()

        # print('username',request.form.get('username'))
        # print('password',request.form.get('password'))
        # print(session['username'], session['password'])

        user.login_info['uid'] = session['username']
        user.login_info["passwd"] = session['password']
        # flag = user.login(session['username'], session['password'])
        flag = 0
        cprint("登录状况: {}".format(str(flag), 'red'))

        if not flag:
            return redirect(url_for('main'))
        return render_template('index.html')


'''
目前完成
'''


@app.route('/main/pokemon')
def showpokemon():
    return render_template('mainpage/pokemon/pokemon.html')


@app.route('/main/handbook')
def showhandbook():
    return render_template('mainpage/handbook/handbook.html')


@app.route('/user/<username>')
def show_user_profile_by_username(username):
    return "用户 {} 的个人主页".format((username))


@app.route('/user/<int:userid>')
def show_user_profile_by_userid(userid):
    return "用户 {} 的个人主页".format(userid)


# 程序入口
if __name__ == "__main__":
    app.run(host='localhost')
