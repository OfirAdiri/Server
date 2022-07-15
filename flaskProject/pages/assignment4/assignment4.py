from flask import Blueprint, render_template, request, jsonify, redirect
import mysql.connector
import requests

# assignment4 blueprint definition
assignment_4 = Blueprint('assignment_4', __name__, static_folder='static', static_url_path='/assignment4', template_folder='templates')

# Routes
@assignment_4.route('/assignment4')
def redirect_homepage():
    return render_template('assignment4.html')


# ------------------------------------------------- #
# ------------- DATABASE CONNECTION --------------- #
# ------------------------------------------------- #
def interact_db(query, query_type: str):
    return_value = False
    connection = mysql.connector.connect(host='localhost',
                                         user='root',
                                         passwd='root',
                                         database='mydb')
    cursor = connection.cursor(named_tuple=True)

    try:
        cursor.execute(query)
    except Exception as e:
        print(e)

    if query_type == 'commit':
        # Use for INSERT, UPDATE, DELETE statements.
        # Returns: The number of rows affected by the query (a non-negative int).
        connection.commit()
        return_value = True

    if query_type == 'fetch':
        # Use for SELECT statement.
        # Returns: False if the query failed, or the result of the query if it succeeded.
        query_result = cursor.fetchall()
        return_value = query_result

    connection.close()
    cursor.close()
    return return_value

# -------------------- INSERT --------------------- #
# ------------------------------------------------- #
@assignment_4.route('/insert_user', methods=['POST'])
def insert_user():
    user_name = request.form['user-name']
    user_email = request.form['user-email']

    ## select all user:
    query = 'select * from users'
    users_list = interact_db(query, query_type='fetch')

    message_for_user = 'משתמש נרשם בהצלחה!'
    for user in users_list:
        if user.email == user_email:
            message_for_user = 'המשתמש כבר קיים במאגר!'

    query = "INSERT INTO users(name, email) VALUES ('%s', '%s')" % (user_name, user_email)
    interact_db(query=query, query_type='commit')
    return render_template('/assignment4.html', message_for_user=message_for_user)

# ------------------- SELECT ---------------------- #
# ------------------------------------------------- #
@assignment_4.route('/select-users')
def select_users():
    query = 'select * from users'
    users_list = interact_db(query, query_type='fetch')
    return render_template('assignment4.html', users=users_list)


# -------------------- DELETE --------------------- #
# ------------------------------------------------- #
@assignment_4.route('/delete_user', methods=['POST'])
def delete_user_func():
    user_email = request.form['user_email']

    ## select all user:
    query = 'select * from users'
    users_list = interact_db(query, query_type='fetch')

    message_for_user = 'משתמש לא קיים במאגר!'

    for user in users_list:
        if user.email == user_email:
            message_for_user = 'משתמש נמחק בהצלחה!'

    query = "DELETE FROM users WHERE email='%s';" % user_email
    interact_db(query, query_type='commit')
    return render_template('/assignment4.html', message_for_delete=message_for_user)


# -------------------- UPDATE --------------------- #
# ------------------------------------------------- #
@assignment_4.route('/update_user', methods=['POST'])
def update_user_func():
    message_for_user = ""
    user_name = request.form['user-name-update']
    user_email = request.form['user-email']
    if(user_name == "" and user_email == ""):
        message_for_user = "לא הוכנסו ערכים לשינוי!"
    else:
        query = "UPDATE users SET name='%s' WHERE email='%s'" % (user_name, user_email)
        message_for_user = "שם משתמש עודכן!"
        interact_db(query, query_type='commit')
        return render_template('/assignment4.html', message_for_update=message_for_user)


    return render_template('/assignment4.html', message_for_user=message_for_user)

# -------------  --- SELECT-JSON ------------------ #
# ------------------------------------------------- #
@assignment_4.route('/assignment4/users')
def select_users_json():
    query = 'select * from users'
    users_list = interact_db(query, query_type='fetch')

    users_dict = {}
    for row in users_list:
        users_dict[row.email] = {
            'name': row.name,
            'email': row.email
        }

    print(users_dict)
    return jsonify(users_dict)
# ------------------------------------------------- #
@assignment_4.route('/outer_source')
def outer_source():
    return render_template('assignment4_outer_source.html')

@assignment_4.route('/fetch_from_backend')
def outer_source_fetch_data():
    user_number = request.args['user_number_2']
    res = requests.get(f"https://reqres.in/api/users/{user_number}")
    return render_template('assignment4_outer_source.html', request_data=res.json()['data'])


@assignment_4.route('/restapi_users')
def usersApi():
    user_id = request.args['id']
    if user_id =="":
        return jsonify ("[1],RONALDO,RONALDO@CRIS.COM")
    return redirect(f'/restapi_users/{user_id}')


@assignment_4.route('/restapi_users/<user_id>')
def printuserjson(user_id):
    query = "select * from users"
    users_list = interact_db(query, query_type='fetch')
    for user in users_list:
        if user_id == str(user.id):
            return jsonify(user)
    return jsonify("User not found")