from flask import Flask, redirect, render_template
from flask import url_for
from flask import render_template
from datetime import timedelta
from flask import request, session, jsonify
import mysql.connector

mydb=mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
)

app = Flask(__name__)

app.secret_key = '123'
app.config['SESSION_PERMANENT'] = True
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=1)

users_dict = {'user1': {"name": "ofir", "email": "ofir@gmail.com"}, 'user2': {"name": "Abir", "email": "abir@gmail.com"},
              'user3': {"name": "sef", "email": "sed@gmail.com"}, 'user4': {"name": "webi", "email": "webi@gmail.com"},
              'user5': {"name": "maor", "email": "maor@gmail.com"}}
count=len(users_dict)
@app.route('/')
def main():
    return redirect('/home_page')

@app.route('/home_page')
def home():
    return render_template('home_page.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/assignment3_1')
def assignment3_1_func():
    user_info = {'name': 'Ofir', 'email': 'adiriof@post.bgu.ac.il', 'profession': 'Student'}
    hobbies = ('football', 'swimming', 'basketball', 'surfing', 'netflix', 'studying')
    return render_template('assignment3_1.html',
                           user_info=user_info,
                           hobbies=hobbies)


@app.route('/assignment3_2', methods=['GET', 'POST'])
def assignment3_2_func():
    #Registration
    if request.method == 'POST':
        email = request.form['email1']
        name = request.form['name1']
        for user in users_dict:
            if name == users_dict[user]['name']:
                if email == users_dict[user]['email']:
                    session['name'] = name
                    session['logedin'] = True
                    return render_template('assignment3_2.html',
                                           message1='Success',
                                           username=name)
                else:
                    return render_template('assignment3_2.html',
                                           message2='Wrong email!')

            elif name == '' and email == '':
                return render_template('assignment3_2.html',
                                       message4='Please enter details')
        for user in users_dict:
            if email == users_dict[user]['email']:
                return render_template('assignment3_2.html',
                                       message3='Email Already Exist!')
        new_user = "user"+str(len(users_dict)+1)
        users_dict[new_user]={"name":name,"email":email}
        session['name'] = name
        session['logedin'] = True
        return render_template('assignment3_2.html',
                               message1='Success',
                               username=name)
    #Search
    if request.method == 'GET':
        if 'email' in request.args:
            email = request.args['email']
            for user in users_dict:
                if email == users_dict[user]['email']:
                    return render_template('assignment3_2.html',
                                           user_name=users_dict[user]['name'],
                                           user_email=users_dict[user]['email'])
                if email == '':
                    return render_template('assignment3_2.html',
                                           users_dict=users_dict)
            return render_template('assignment3_2.html',
                               message='user not found')
        return render_template('assignment3_2.html')

@app.route('/log_out')
def logout_func():
    session['logedin'] = False
    session.clear()
    return redirect(url_for('assignment3_2_func'))

###### Pages
## assignment4
from pages.assignment4.assignment4 import assignment_4
app.register_blueprint(assignment_4)

if __name__ == '__main__':
    app.run(debug=True)
    app.run()
