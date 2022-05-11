from flask import Flask, make_response, request
from resources.nextByMode import *
from models.content import ContentModel


class PlaylistEntry(Resource):
    @auth.login_required()
    def post(self):
        parser = reqparse.RequestParser()
        # define al input parameters need and its type
        parser.add_argument('name', type=str, required=True, help="Path  not valid: 'path' not provided")
        parser.add_argument('duration', nullable=True, help="duration  not valid: 'duration' not provided")
        parser.add_argument('type', nullable=False, help="duration  not valid: 'duration' not provided")
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
            # contentFile=ContentModel.find_by_name(dades['name'])
            # playlist_entry = PlaylistModel(content_id=contentFile.id, duration=duration, type=dades['type'])
            playlist_entry = PlaylistModel(name=dades['name'], duration=duration, type=dades['type'])
            playlist_entry.save_to_db()
            PlaylistModel.update_id_as_priority()
        except:
            return make_response(("No s'ha pogut afegir " + dades[
                'name'] + ": L'Entrada de la playlist que intentes afegir ja existeix", 400))

        return make_response(("Entrada de la playlist correctament afegida " + dades['name'], 200))

    @auth.login_required()
    def delete(self, name):
        try:
            content = PlaylistModel.find_by_name(name).json()
            name = content['name']
            response = "Entrada de la playlist 'nom': " + str(name) + "esborrada"
            PlaylistModel.delete_by_name(name)
        except:
            return {'message': "Entrada de la playlist ['nom': {} ] no trobada".format(nom)}, 404
        return {'message': response}, 200


class Playlist(Resource):
    @auth.login_required()
    def get(self):
        entries = PlaylistModel.retrieveAllEntries()
        container_entries = []
        for e in entries:
            container_entries.append(e.json())
        return {'Playlist': container_entries}


class NextEntry(Resource):

    def get(self):
        forced_next = getVarFromFile('forced_next')
        if forced_next:
            forced_next_metadata = getVarFromFile('forced_next_metadata')
            next = json.loads(json.dumps(forced_next_metadata))
            setVarFromFile('forced_next', False)
            return {'metadata': next}, 200
        else:
            next = getNext()
        return {'metadata': next}, 200

    @auth.login_required()
    def post(self):
        setVarFromFile('forced_next', True)
        parser = reqparse.RequestParser()
        # define al input parameters need and its type
        parser.add_argument('name', type=str, required=True, help="Path  not valid: 'path' not provided")
        parser.add_argument('duration', nullable=True, help="duration  not valid: 'duration' not provided")
        parser.add_argument('type', nullable=False, help="duration  not valid: 'duration' not provided")
        dades = parser.parse_args()
        duration = None
        if checkType(dades['name']) == 'notAcceptedType':
            return make_response(("El fitxer no es multimedia", 400))
        if dades['type'] == 'Image':
            if dades['duration'] and int(dades['duration']) > 0:
                duration = int(dades['duration'])
            else:
                duration = 6000
        setVarFromFile('forced_next_metadata',
                       {'path': "./static/" + dades['name'], 'duration': duration, 'type': dades['type']})
        return {'message': "Petició de reproducció processada correctament"}, 200
