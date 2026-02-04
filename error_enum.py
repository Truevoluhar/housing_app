invalid_username_length = 1
invalid_email_address = 2
invalid_password = 3
success_validation = 4
success_login = 8

username_min_length = 7

logged_user_non_existent = 5
logger_user_locked_out = 6
logged_user_invalid_pw = 7

# Registration errors
email_already_exists = 9
first_name_too_short = 10
last_name_too_short = 11
registration_success = 12

error_list ={
    1 : "Username should be at least "+str(username_min_length)+" characters",
    2: "Invalid format of the email address provided",
    3: "Invalid credentials - error text from enumeration",
    9: "Email already exists. Please try logging in instead.",
    10: "First name must be at least 2 characters long.",
    11: "Last name must be at least 2 characters long.",
    12: "Registration successful! Please log in."
}
