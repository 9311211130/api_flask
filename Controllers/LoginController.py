from Models.Model import Student

__author__ = 'milad'
from flask_restful import Resource

from flask import g
from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth


auth = HTTPBasicAuth()
auth2 = HTTPTokenAuth()


# noinspection PyBroadException
@auth.verify_password
def verify_password(username_or_token, password):
    # first try to authenticate by token
    user = Student.verify_auth_token(username_or_token)
    if not user:
        # try to authenticate with username/password
        try:
            user = Student.get(Student.student_number == username_or_token)
        except:
            user = None
        if not user or not user.verify_password(password):
            return False
    g.user = user
    return True


@auth2.verify_token
def verify_token(token):
    user = Student.verify_auth_token(token)
    if user:
        g.user = user
        return True
    return False


class Login(Resource):
    @auth.login_required
    def get(self):
        token = g.user.generate_auth_token(600)
        print(g.user)
        return {'token': token.decode('ascii'), 'duration': 600, 'lastname': g.user.lastname}

    @auth.login_required
    def post(self):
        token = g.user.generate_auth_token(600)
        return {'token': token.decode('ascii'), 'duration': 600, 'lastname': g.user.lastname}
