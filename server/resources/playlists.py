from server.models.playlist_names import PlaylistsModel
from server.resources.nextByMode import *
import json


class Playlists(Resource):
    # TODO @auth.login_required(role='admin')
    def get(self, name):
        try:
            pl = PlaylistsModel.find_by_name(name).json()
        except Exception as e:
            return {'message': "Playlist no  trobada"}, 400
        return {'playlist': pl}, 200

    # @auth.login_required(role='admin')
    def post(self):
        try:
            parser = reqparse.RequestParser()  # create parameters parser from request

            # define al input parameters need and its type
            parser.add_argument('name', type=str, required=True, help="This field cannot be left blanck")
            parser.add_argument('items', type=str, required=True, help="This field cannot be left blanck")
            parser.add_argument('tags', type=str)

            dades = parser.parse_args()

            if PlaylistsModel.find_by_name(dades['name']):
                return {'message': "Playlist amb ['nom': {} ] ja existeix".format(dades['nom'])}, 409
            else:
                new_playlist = PlaylistsModel(name=dades['name'])
                # TODO: add items and tags and create relation
                new_playlist.save_to_db()
                return {'playlist': new_playlist.json()}, 200

        except:
            return {'message': "Ha hagut un problema amb la petició"}, 400

        return {'message': "Petició processada correctament"}, 200


class PlaylistsList(Resource):
    # TODO @auth.login_required(role='admin')
    def get(self):
        plts = PlaylistsModel.retrieveAllEntries()
        container_playlists = []
        for a in plts:
            print(a)
            print(type(a))
            container_playlists.append(a.json())

        return {'playlists': container_playlists}, 200
