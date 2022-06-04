from flask_restful import Resource, reqparse
from models.playlist_names import PlaylistsModel
from models.tags import TagsModel
from models.items import ItemsModel


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
            parser.add_argument('name', type=str, required=True, help="This field cannot be left blank")
            parser.add_argument('items', type=list, required=True, location='json',
                                help="This field cannot be left blank")
            parser.add_argument('tags', type=str, action="append", required=False)

            dades = parser.parse_args()

            if PlaylistsModel.find_by_name(dades['name']):
                return {'message': "Playlist amb ['nom': {} ] ja existeix".format(dades['name'])}, 409
            else:
                new_playlist = PlaylistsModel(dades['name'])
                # TODO: add items and tags and create relation. Need to create a loop
                for tag in dades['tags']:
                    new_tag = TagsModel.find_by_name(name=tag)
                    if new_tag is None:
                        new_tag = TagsModel(name=tag)
                    new_playlist.tags.append(new_tag)
                for item in dades['items']:
                    print(item)
                    new_item = ItemsModel.find_by_name(name=item['name'])
                    if new_item is None:
                        new_item = ItemsModel(name=item['name'],
                                              duration=item['duration'], type=item['type'])
                    new_playlist.items.append(new_item)

                # new_playlist.items.append(new_item)
                # new_playlist.tags.append(tag)
                new_playlist.save_to_db()
                return {'playlist': new_playlist.json()}, 200

        except:
            return {'message': "Hi ha hagut un problema amb la petició"}, 400

        # return {'message': "Petició processada correctament"}, 200


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
