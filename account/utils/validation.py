import re


def email_validation(email):
    return bool(re.search('^[\w\-\.]+@([\w-]+\.)+[\w-]{2,}$', email))


def login_validation(login):
    return bool(len(login) >= 4)


def password_validation(password):
    return bool(len(password) >= 4)


def validate(user):
    return bool(email_validation(user.email) and 
                login_validation(user.login) and 
                password_validation(user.password)
            )