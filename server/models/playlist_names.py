from db import db
import json

from flask import jsonify

playlist_items = db.Table('playlist_items',
                          db.Column('playlist_id', db.Integer, db.ForeignKey('playlist_names.id'), primary_key=True),
                          db.Column('item_id', db.Integer, db.ForeignKey('items.id'), primary_key=True)
                          )

playlist_tags = db.Table('playlist_tags',
                         db.Column('playlist_id', db.Integer, db.ForeignKey('playlist_names.id'), primary_key=True),
                         db.Column('tag_id', db.Integer, db.ForeignKey('tags.id'), primary_key=True)
                         )


class PlaylistsModel(db.Model):
    __tablename__ = 'playlist_names'  # This is table name
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, db.ForeignKey('content.name'), unique=True, nullable=False)
    tags = db.relationship('TagsModel',
                           secondary=playlist_tags)
    items = db.relationship('ItemsModel',
                            secondary=playlist_items)

    def __init__(self, name):
        self.name = name

    def json(self):
        return json.loads(json.dumps
                          (self, default=lambda o: {'id': self.id, 'name': self.name,
                                                    'items': [item.json() for item in self.items],
                                                    'tags': [tag.json() for tag in self.tags]}))

    def save_to_db(self):
        try:
            # saving data
            db.session.add(self)
            db.session.commit()
        except:
            raise Exception("Error saving playlist in database")

    def delete_from_db(self):
        try:
            # saving data
            db.session.remove(self)
            db.session.commit()
        except:
            raise Exception("Error deleting playlist in database")

    @classmethod
    def find_by_id(cls, id):
        return PlaylistsModel.query.filter_by(id=id).first()

    @classmethod
    def find_by_name(cls, name):
        try:
            return PlaylistsModel.query.filter_by(name=name).first()
        except:
             raise Exception("There was a problem finding the username")

    @classmethod
    def delete_by_name(cls, name):
        try:
            # saving data
            db.session.delete(PlaylistsModel.query.filter_by(name=name).first())
            db.session.commit()
        except:
            raise Exception("Error deleting entry by priority in database")

    @classmethod
    def retrieveAllEntries(cls):
        return PlaylistsModel.query.all()
