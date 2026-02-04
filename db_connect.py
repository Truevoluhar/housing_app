from flask import session
import sqlite3
import error_enum
import hash_encyrptor
import user

max_login_attempts = 4

def connect():
    try:
        db_connect = sqlite3.connect('housing_app.db')
        return db_connect
    except:
        print("-- Could not connect to the DB --")
        return False

def init_db():
    connection = connect()
    if connection == False:
        return False
    cursor = connection.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        failed_attempts INTEGER DEFAULT 0,
        locked_out INTEGER DEFAULT 0,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        user_type TEXT DEFAULT 'user',
        session_time TEXT,
        active INTEGER DEFAULT 1
    )''')
    connection.commit()
    connection.close()


def login(username, password):

    connection = connect()

    if connection == False:
        return False

    query = 'SELECT * FROM users WHERE email=?'

    db_cursor = connection.cursor()

    try:

        db_cursor.execute(query, (username,))
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

    query = "UPDATE users SET failed_attempts = ?, locked_out = ? WHERE id = ?"

    val = (attempts, locked_out, user_id)

    db_cursor = db_connect.cursor()

    db_cursor.execute(query, val)

    db_connect.commit()
    db_connect.close()

def check_email_exists(email):
    connection = connect()
    if connection == False:
        return False

    query = 'SELECT COUNT(*) FROM users WHERE email = ?'
    db_cursor = connection.cursor()
    db_cursor.execute(query, (email,))
    result = db_cursor.fetchone()
    connection.close()
    return result[0] > 0

def register_user(first_name, last_name, email, hashed_password):
    connection = connect()
    if connection == False:
        return False

    query = "INSERT INTO users (first_name, last_name, email, password, user_type, active) VALUES (?, ?, ?, ?, ?, ?)"
    val = (first_name, last_name, email, hashed_password, 'user', 1)

    db_cursor = connection.cursor()
    try:
        db_cursor.execute(query, val)
        connection.commit()
        return True
    except:
        return False
    finally:
        connection.close()
