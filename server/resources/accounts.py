from flask import Flask
from flask_restful import Resource, Api, reqparse
from db import db
from flask_migrate import Migrate
import json
from json import JSONEncoder
from models.accounts import AccountsModel
from flask_httpauth import HTTPBasicAuth
from models.accounts import g
from models.accounts import auth


class Accounts(Resource):
    def get(self, username):
        try:
            account = AccountsModel.find_by_username(username).json()
        except Exception as e:
            return {'message': "Usuari no  trobat"}, 400
        return {'account': account}, 200

    @auth.login_required(role='admin')
    def post(self, id=None):
        try:
            parser = reqparse.RequestParser()  # create parameters parser from request

            # define al input parameters need and its type
            parser.add_argument('username', type=str, required=True, help="This field cannot be left blanck")
            parser.add_argument('password', type=str)

            dades = parser.parse_args()
            if AccountsModel.find_by_username(dades['username']):
                return {'message': "Usari amb ['username': {} ] ja existeix".format(dades['username'])}, 409
            else:
                new_account = AccountsModel(username=dades['username'])
                new_account.hash_password(dades['password'])
                new_account.save_to_db()
                return {'account': new_account.json()}, 200

        except:
            return {'message': "Ha hagut un problema amb la petició"}, 400

        return {'message': "Petició processada correctament"}, 200

    @auth.login_required(role='admin')
    def delete(self, username):
        try:
            AccountsModel.delete_by_username(username)
        except:
            return {'message': "Usari amb  ['username': {} ] no trobat".format(username)}, 400
        return {'message': "Usari amb ['username': {} ] esborrat correctament".format(username)}, 200

    @auth.login_required(role='admin')
    def put(self, username):
        try:
            parser = reqparse.RequestParser()  # create parameters parser from request

            # define al input parameters need and its type
            parser.add_argument('username', type=str)
            parser.add_argument('password', type=str)
            parser.add_argument('is_admin')
            dades = parser.parse_args()

            if AccountsModel.find_by_username(username):
                """
                if dades['username']:
                    if dades['is_admin']:
                        account.updateData(username=dades['username'],is_admin=dades['is_admin'])
                    else:
                        account.updateData(username=account.json()['username'],is_admin=dades['is_admin'])
               
                account=AccountsModel.find_by_username(username)
                if dades['username'] and dades['is_admin']:
                    account.updateData(username=dades['username'],is_admin=dades['is_admin'])
            
                elif dades['is_admin'] and not dades['username']:
                    account.updateData(username=username,is_admin=dades['is_admin'])

                elif dades['username'] and not dades['is_admin']:
                    account.updateData(username=dades['username'],is_admin=account.json()['is_admin'])

                else:
                    print('is_admin & username won"t change')
                 """
                account=AccountsModel.find_by_username(username)
                try:
                    if dades['username']:
                        account.updateUsername(dades['username'])
                        account.save_to_db()
                        account=AccountsModel.find_by_username(dades['username'])
                except:
                    return {'message': "Usari amb ['username': {} ] no modificat, problema amb username ".format(username)}, 400

                try:
                    if dades['is_admin']:
                        #return {'message': "dades['is_admin']: " + dades['is_admin']}, 400
                        account.updateRole(dades['is_admin'])
                except:
                    return {'message': "Usari amb ['username': {} ] no modificat, problema amb is_admin ".format(username)}, 400

                try:
                    if dades['password'] :
                        account.hash_password(dades['password'])
                except:
                    return {'message': "Usari amb ['username': {} ] no modificat, problema amb password ".format(username)}, 400

                account.save_to_db()
                return {'message': "Usari amb ['username': {} ] modificat correctament".format(username)}, 200

            else:
                return {'message': "Usari amb  ['username': {} ] no trobat".format(username)}, 400
        except:
            return {'message': "Usari amb ['username': {} ] no modificat ".format(username)}, 400
        return {'message': "Petició processada correctament"}, 200


class AccountsList(Resource):
    #TODO @auth.login_required(role='admin')
    def get(self):
        acc = AccountsModel.retrieveAllAccounts(self)

        container_accounts = []
        for a in acc:
            container_accounts.append(a.json())

        return {'accounts': container_accounts},200
