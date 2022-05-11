
from flask_restful import Api

from db import db
import json



class ContentModel(db.Model):
    __tablename__ = 'content'  # This is table name

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True, nullable=False)
    path = db.Column(db.String(30), nullable=False)
    size = db.Column(db.String(30), nullable=False)

    def __init__(self, name, path, size):
        self.name = name
        self.path = path
        self.size = size


    def json(self):
        return json.loads(json.dumps(self, default=lambda o: {'id': self.id, 'name': self.name, 'path': self.path,
                                                              'size': self.size}))

    def save_to_db(self):
        try:
        # saving data
            db.session.add(self)
            db.session.commit()
        except:
            raise Exception("Error saving file in database")

    def delete_from_db(self):
        try:
            # saving data
            db.session.remove(self)
            db.session.commit()
        except:
            raise Exception("Error deleting file in database")

    @classmethod
    def find_by_id(cls, id):
        return ContentModel.query.filter_by(id=id).first()

    @classmethod
    def find_by_name(cls, name):
        return ContentModel.query.filter_by(name=name).first()

    @classmethod
    def delete_by_id(cls, id):
        try:
            # saving data
            db.session.delete(ContentModel.query.filter_by(id=id).first())
            db.session.commit()
        except:
            raise Exception("Error deleting artist by id in database")

    def updateData(self, name, path, size):
        try:
            self.name = name
            self.path = path
            self.size = size
        except:
            raise Exception("Error updating event data in database")

