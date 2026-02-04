from flask import session
import mysql.connector
import error_enum
import hash_encyrptor
import user

max_login_attempts = 4

def connect():

    returnVar = False

    try:
        db_connect = mysql.connector.connect(
            host="{YOUR_HOST}",
            user="{YOUR_DB_USER}",
            password="{YOUR_DB_PASS}",
            database="{YOUR_DB}"
        )

        returnVar = db_connect

    except:
        print("-- Could not connect to the DB --")

    return returnVar


def login(username, password):

    connection = connect()

    if connection == False:
        return False

    query = 'SELECT * FROM users WHERE email="'+username+'"'

    db_cursor = connection.cursor()

    try:

        db_cursor.execute(query)
        result = db_cursor.fetchone()

        if result:
            current_user = user.user(result)

            if current_user.active == 1 and current_user.locked_out == 0:

                if password == current_user.password:

                    session['first_name'] = current_user.first_name
                    session['last_name'] = current_user.last_name
                    session['email'] = current_user.email
                    session['user_type'] = current_user.user_type
                    session['logged_in'] = True

                    update_fail_attempts(current_user.id, 0)

                    return error_enum.success_login

                else:

                    if current_user.locked_out == 0:
                        user_id = current_user.id
                        attempts = current_user.failed_attempts+1

                        locked_out = 0

                        if attempts > max_login_attempts:
                            locked_out = 1

                        update_fail_attempts(user_id, attempts,locked_out)

                return False
            else:
                return False

            return True

    except:
        return False

def is_user_logged_in():

    if session.get('logged_in') == True:
        return True
    else:
        return False

def clear_session():
    session.clear()

def update_fail_attempts(user_id,attempts,locked_out = 0):

    db_connect = connect()

    if db_connect == False:
        return False

    query = "UPDATE users SET failed_attempts = %s, locked_out = %s WHERE id = %s"

    val = (attempts, locked_out, user_id)

    db_cursor = db_connect.cursor()

    db_cursor.execute(query, val)

    db_connect.commit()
