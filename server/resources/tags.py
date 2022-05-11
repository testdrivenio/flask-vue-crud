from flask import Flask, make_response, request

from models.tags import TagsModel
from resources.nextByMode import *


class Tags(Resource):
    # TODO @auth.login_required()
    def post(self):
        parser = reqparse.RequestParser()
        # define al input parameters need and its type
        parser.add_argument('name', type=str, required=True,
                            help="Name  not valid: 'name' not provided")
        dades = parser.parse_args()
        try:
            print(dades['name'])
            tag = TagsModel(name=dades['name'])
            tag.save_to_db()
        except Exception as e:
            return {'message': "Error guardant a la base de dades"}, 400
        return {'message': "Tag amb nom" + dades['name'] + " guardat correctament"}, 200

class TagsList(Resource):
    #TODO @auth.login_required(role='admin')
    def get(self):
        plts = TagsModel.retrieveAllEntries()

        container_items = []
        for a in plts:
            container_items.append(a.json())

        return {'tags': container_items},200
