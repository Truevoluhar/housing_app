from flask import Flask, render_template, request, url_for, redirect, session

import db_connect
import format_validator as fv
import hash_encyrptor
import error_enum

app = Flask(__name__)
app.secret_key = 'tonis_key'

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/signup')
def signup():
    return render_template('signup.html', payload=[])

@app.route('/dashboard')
def dashboard():

    if db_connect.is_user_logged_in():
        return render_template('dashboard.html')
    else:
        db_connect.clear_session()
        return redirect(url_for('login'))

@app.route('/logout')
def logout():

    db_connect.clear_session()

    return redirect(url_for('login'))

@app.route('/login',methods = ['GET','POST'])
def login():

    if request.method == 'GET':

        if db_connect.is_user_logged_in():
            return redirect(url_for('dashboard'))

        return render_template('login.html', payload=[])

    if request.method == 'POST':

        passed_username = request.form.get('email')
        passed_password = request.form.get('password')

        validation_result = fv.validate_username(passed_username, passed_password)

        if validation_result == error_enum.success_validation:

            result = hash_encyrptor.hash(passed_password)

            login_result = db_connect.login(passed_username, result)

            if login_result == error_enum.success_login:
               return redirect(url_for('dashboard'))
            else:
                payload = {
                    "err_msg": "Invalid credentials"
                }

                return render_template('login.html', payload=payload)



        else:

            error_message = error_enum.error_list[validation_result]

            payload = {
                "err_msg": error_message
            }

            return render_template('login.html', payload=payload)




if __name__ == '__main__':
    app.run(debug=True)
