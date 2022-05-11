import json
from passlib.apps import custom_app_context as pwd_context
from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)
from db import db, secret_key
from flask_httpauth import HTTPBasicAuth
from flask import g, current_app

auth = HTTPBasicAuth()


class AccountsModel(db.Model):
    __tablename__ = 'accounts'

    username = db.Column(db.String(30), primary_key=True, unique=True, nullable=False)
    password = db.Column(db.String(), nullable=False)
    # 0 not admin/ 1 is admin
    is_admin = db.Column(db.Integer, nullable=False)

    def __init__(self, username, is_admin=0):
        self.username = username
        self.is_admin = is_admin

    def json(self):
        return json.loads(json.dumps(self, default=lambda o: {'username': self.username, 'is_admin': self.is_admin}))

    def hash_password(self, password):

        self.password = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password)

    def retrieveAllAccounts(self):
        return AccountsModel.query.all()

    def find_by_username(username):
        try:
            return AccountsModel.query.filter_by(username=username).first()
        except:
             raise Exception("There was a problem finding the username")


    def delete_by_username(username):
        try:
            # saving data
            a = AccountsModel.query.filter_by(username=username).first()
            db.session.delete(a)
            db.session.commit()
        except:
            raise Exception("There was a problem  deleting  on database")

    def save_to_db(self):
        try:# saving data
            db.session.add(self)
            db.session.commit()
            return {"message": "Ok"}, 200
        except:
            raise Exception("There was a problem  saving on database")

    def delete_from_db(self):
        try:
            # saving data
            db.session.remove(self)
            db.session.commit()
        except:
            raise Exception("There was a problem  deleting  on database")

    def undoOperation(self):
        try:
            db.session.rollback()
        except:
            raise Exception("There was a problem rollingback on database")

    def hash_password(self, password):
        self.password = pwd_context.encrypt(password)


    def generate_auth_token(self, expiration=3600):
        s = Serializer(current_app.secret_key, expires_in=expiration)
        return s.dumps({'username': self.username})

    def updateData(self, username, is_admin):
        try:
            self.username = username
            self.is_admin = is_admin
        except:
             raise Exception("There was a problem updating the data  on database")

    def updateRole(self, is_admin):
        try:
            self.is_admin = is_admin
        except:
             raise Exception("There was a problem updating the data  on database")

    def updateUsername(self, username):
        try:
            self.username = username
        except:
             raise Exception("There was a problem updating the data  on database")


    @classmethod
    def verify_auth_token(cls, token):
        s = Serializer(current_app.secret_key)
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None  # valid token, but expired
        except BadSignature:
            return None  # invalid token
        user = cls.query.filter_by(username=data['username']).first()
        g=user
        return user

@auth.verify_password
def verify_password(token, password):
    user=AccountsModel.verify_auth_token(token)
    if user:
        g.user = user
        return user


@auth.get_user_roles
def get_user_roles(user):
    if user.is_admin == 1:
        return['admin']
    else:
        return ['user']

@auth.error_handler
def auth_error(status):
    return {'message': "La sessió ha caducat, inicia sessió de nou"}, 200
