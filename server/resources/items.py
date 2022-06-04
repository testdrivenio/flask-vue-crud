from flask import Flask, make_response, request
from resources.nextByMode import *

class Items(Resource):
    # TODO @auth.login_required()
    def post(self):
        parser = reqparse.RequestParser()
        # define al input parameters need and its type
        parser.add_argument('name', type=str, required=True,
                            help="Name  not valid: 'name' not provided")
        parser.add_argument('type', type=str, required=True,
                            help="Type not valid: 'type' not provided")
        parser.add_argument('priority', type=int, required=True,
                            help="Priority not valid: 'priority' not provided")
        parser.add_argument('duration', type=int, required=False,
                            help="Duration not valid: 'duration' not provided")
        parser.add_argument('played', type=int, required=True,
                            help="Played not valid: 'played' not provided")
        parser.add_argument('playlist_name', type=str, required=False,  # TODO: change required to True
                            help="Playlist_name not valid: 'playlist_name' not provided")
        dades = parser.parse_args()
        chck = checkType(dades['name'])
        duration = None
        if checkType(dades['name']) == 'notAcceptedType':
            return make_response(("El fitxer no es multimedia", 400))
        if dades['type'] == 'Image':
            if dades['duration'] and int(dades['duration']) > 0:
                duration = int(dades['duration'])
            else:
                duration = 6000

        try:
            item = ItemsModel(name=dades['name'], duration=duration, type=dades['type'])
            # TODO: Create relation between item and playlist
            item.save_to_db()
        except Exception as e:
            return {'message': "Error guardant a la base de dades"}, 400
        return {'message': "Item amb nom" + dades['name'] + " guardat correctament"}, 200


class ItemsList(Resource):
    # TODO @auth.login_required(role='admin')
    def get(self):
        plts = ItemsModel.retrieveAllEntries()

        container_items = []
        for a in plts:
            container_items.append(a.json())

        return {'items': container_items}, 200
