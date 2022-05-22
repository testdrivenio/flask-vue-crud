from flask import Flask, jsonify, request
from flask_cors import CORS
from flask import Flask,render_template
from flask_cors import CORS
from flask_restful import Resource, Api, reqparse
from resources.content import Content
from resources.accounts import Accounts,AccountsList
from resources.login import Login
from flask import send_from_directory
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from checktype import *
from db import db, secret_key
from resources.mode import Mode
from resources.playlist import Playlist
from resources.playlists import PlaylistsList, Playlists
from resources.items import Items, ItemsList
from resources.tags import Tags, TagsList

DEBUG = True

# instantiate the app
app = Flask(__name__,
         static_folder="./frontend/dist/static",
         template_folder="./frontend/dist")
app.config.from_object(__name__)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})

app.config["CONTENT_UPLOADS"] = '/app/media'
app.config["CONTENT_UPLOADS_THUMBNAILS"] = '/app/media/thumbnails'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['SECRET_KEY'] = secret_key

api = Api(app)
api.add_resource(Content, '/content/<int:id>', '/content')
migrate = Migrate(app, db, directory='./database/migrations')
manager = Manager(app)
manager.add_command('db', MigrateCommand)
db.init_app(app)

# Endpoints
api.add_resource(Accounts, '/account/<string:username>', '/account')
api.add_resource(AccountsList, '/accounts')
api.add_resource(Login, '/login')
api.add_resource(Playlist, '/playlist/<string:name>', '/playlist')
api.add_resource(Playlists, '/playlists/<string:name>', '/savePlaylist')
api.add_resource(PlaylistsList, '/playlistslist')
api.add_resource(ItemsList, '/items')
api.add_resource(Items, '/item')
api.add_resource(TagsList, '/tags')
api.add_resource(Tags, '/tag')
api.add_resource(Mode, '/mode')


# sanity check route
@app.route('/ping', methods=['GET'])
def ping_pong():
    return jsonify('pong!')

if __name__ == '__main__':
    app.run(port=80, debug=True)

