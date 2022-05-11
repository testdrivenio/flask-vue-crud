from flask import Flask, make_response, request

from server.models.playlist_names import PlaylistsModel
from server.resources.nextByMode import *
import json

class PlaylistsList(Resource):
    #TODO @auth.login_required(role='admin')
    def get(self):
        plts = PlaylistsModel.retrieveAllEntries()

        container_playlists = []
        for a in plts:
            container_playlists.append(a.json())

        return {'playlists': container_playlists},200
