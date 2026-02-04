import re, error_enum

def validate_username(username,password):
    # check that value is entered at all
    username_length = len(username)

    if username_length < error_enum.username_min_length:
        return error_enum.invalid_username_length

    # validate the email
    if validate_email(username) == False:
        return error_enum.invalid_email_address


    if validate_password(password) == False:
        return error_enum.invalid_password

    return error_enum.success_validation

def validate_email(email):

    email_pattern = "^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\\.[a-zA-Z0-9-.]+$"

    return bool(re.match(email_pattern,email))

def validate_password(password):
    return bool(re.search(r'\d', password) and len(password) >= 4)
