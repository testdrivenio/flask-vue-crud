from flask import Flask
from flask_restful import Resource, Api, reqparse
from models.accounts import AccountsModel
from db import db
from flask_migrate import Migrate
import json
from json import JSONEncoder

class Login(Resource):

    def post(self, id=None):
        parser = reqparse.RequestParser()  # create parameters parser from request

        # define al input parameters need and its type
        parser.add_argument('username', type=str, required=True, help="El camp nom d'usuari no pot estar buit")
        parser.add_argument('password', type=str, required=True, help="El camp de la contrasenya no pot estar buit")

        dades = parser.parse_args()

        if dades['username'] is '' or "":
            return {'message': "Usuari no valid : El camp nom d'usuari no pot estar buit"}, 400

        if dades['password'] is '' or "":
            return {'message': "Usuari no valid : El camp de la contrasenya no pot estar buit"}, 400

        account = AccountsModel.find_by_username(username=dades['username'])

        if not account:
            #return {'message': "Account with username [{}] Not found".format(dades['username'])}, 400
            return {'message': "Contrasenya incorrecta"}, 400

        valid_password = account.verify_password(dades['password'])

        if not valid_password:
            return {'message': "Contrasenya incorrecta"}, 400

        token = account.generate_auth_token()
        return {'token': token.decode('ascii')}, 200
