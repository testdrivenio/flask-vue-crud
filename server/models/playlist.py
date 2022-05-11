from flask_restful import Api
from models.content import ContentModel
from db import db
import json
from sqlalchemy.orm import relationship


class PlaylistModel(db.Model):
    __tablename__ = 'playlist'  # This is table name

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, db.ForeignKey('content.name'), unique=True, nullable=False)
    type = db.Column(db.String(8), nullable=False)
    priority = db.Column(db.Integer)
    duration = db.Column(db.Integer)
    path = db.Column(db.String(8), nullable=False)
    played = db.Column(db.Integer)
    content = relationship("ContentModel")  # ,backref=backref("content", uselist=False))

    def __init__(self, name, type, duration):
        self.name = name
        self.type = type
        self.priority = self.id
        self.duration = duration
        # self.path = "./static/" + content.name
        self.path = "./static/" + name  # ContentModel.find_by_id(content_id).json()['name']
        self.played = 0

    def json(self):
        return json.loads(json.dumps(self, default=lambda o: {'id': self.id, 'name': self.name, 'type': self.type,
                                                              'priority': self.priority, 'duration': self.duration,
                                                              'path': self.path, 'played': self.played}))

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
        return PlaylistModel.query.filter_by(id=id).first()

    @classmethod
    def find_by_name(cls, name):
        return PlaylistModel.query.filter_by(name=name).first()

    @classmethod
    def top_by_priority(cls):
        top = PlaylistModel.query.order_by(PlaylistModel.priority).first()
        return top

    @classmethod
    def last_by_priority(cls):
        last = PlaylistModel.query.order_by(PlaylistModel.priority).last()
        return last

    @classmethod
    def update_priority(cls):
        PlaylistModel.query.update({PlaylistModel.priority: PlaylistModel.priority - 1}, synchronize_session='fetch')
        PlaylistModel.query.update({PlaylistModel.id: PlaylistModel.id - 1}, synchronize_session='fetch')
        db.session.commit()

    @classmethod
    def update_id_as_priority(cls):
        PlaylistModel.query.update({PlaylistModel.priority: PlaylistModel.id}, synchronize_session='fetch')
        db.session.commit()

    @classmethod
    def delete_by_priority(cls):
        try:
            # saving data
            db.session.delete(PlaylistModel.query.order_by(PlaylistModel.priority).first())
            db.session.commit()
        except:
            raise Exception("Error deleting entry by priority in database")

    @classmethod
    def delete_by_name(cls, name):
        try:
            # saving data
            db.session.delete(PlaylistModel.query.filter_by(name=name).first())
            db.session.commit()
        except:
            raise Exception("Error deleting entry by priority in database")

    @classmethod
    def retrieveAllEntries(cls):
        return PlaylistModel.query.all()

    @classmethod
    def retrieveByUnplayed(cls):
        return PlaylistModel.query.filter_by(played=0).all()

    @classmethod
    def makeAllUnplayed(cls):
        PlaylistModel.query.update({PlaylistModel.played: 0}, synchronize_session='fetch')
        db.session.commit()
