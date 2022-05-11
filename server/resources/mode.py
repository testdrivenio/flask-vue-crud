from flask import Flask
from flask_restful import Resource, Api
from flask import request, redirect
from werkzeug.utils import secure_filename
import json
from flask_restful import Resource, Api
from flask import request, redirect
from flask_restful import reqparse
from werkzeug.utils import secure_filename
import os
import datetime
from models.playlist import PlaylistModel
from variable_store import *
from checktype import *
from models.accounts import g, AccountsModel
from models.accounts import auth

class Mode(Resource):

	def get(self):
		return {'message': getVarFromFile('mode')}, 200

	@auth.login_required()
	def put(self):
		parser = reqparse.RequestParser()  # create parameters parser from request
		parser.add_argument('mode', type=str, required=True, help="This field cannot be left blanck")
		dades = parser.parse_args()
		setVarFromFile('first', True)
		setVarFromFile('mode', dades['mode'])
		return {'message': "correct"}, 200

