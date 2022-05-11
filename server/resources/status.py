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

class Status(Resource):
	def get(self):
		getVarFromFile('status')
		if getVarFromFile('status'):
			return {'message': "online"}, 200
		else:
			return {'message': "stop"}, 200

	@auth.login_required()
	def post(self):
		setVarFromFile('status', not getVarFromFile('status'))
		return {'message': "correct"}, 200

