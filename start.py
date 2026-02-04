from flask import Flask, render_template, request, url_for, redirect, session

import db_connect
import format_validator as fv
import hash_encyrptor
import error_enum

app = Flask(__name__)
app.secret_key = 'tonis_key'

# Initialize database
db_connect.init_db()

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return render_template('signup.html', payload=[])

    if request.method == 'POST':
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        email = request.form.get('email')
        password = request.form.get('password')

        # Validate input
        validation_result = fv.validate_registration(email, password, first_name, last_name)

        if validation_result != error_enum.success_validation:
            error_message = error_enum.error_list[validation_result]
            payload = {"err_msg": error_message}
            return render_template('signup.html', payload=payload)

        # Check if email already exists
        if db_connect.check_email_exists(email):
            payload = {"err_msg": error_enum.error_list[error_enum.email_already_exists]}
            return render_template('signup.html', payload=payload)

        # Hash password
        hashed_password = hash_encyrptor.hash(password)

        # Register user
        if db_connect.register_user(first_name, last_name, email, hashed_password):
            payload = {"err_msg": error_enum.error_list[error_enum.registration_success]}
            return render_template('signup.html', payload=payload)
        else:
            payload = {"err_msg": "Registration failed. Please try again."}
            return render_template('signup.html', payload=payload)

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
