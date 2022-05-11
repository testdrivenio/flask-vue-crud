from db import db
import json


class ItemsModel(db.Model):
    __tablename__ = 'items'  # This is table name

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, db.ForeignKey('content.name'), unique=True, nullable=False)
    type = db.Column(db.String(8), nullable=False)
    priority = db.Column(db.Integer)
    duration = db.Column(db.Integer)
    path = db.Column(db.String(8), nullable=False)
    played = db.Column(db.Integer)

    def __init__(self, name, duration, type):
        self.name = name
        self.type = type
        self.priority = self.id
        self.duration = duration
        self.path = "./static/" + name
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
            raise Exception("Error saving item in database")

    def delete_from_db(self):
        try:
            # saving data
            db.session.remove(self)
            db.session.commit()
        except:
            raise Exception("Error deleting item in database")

    @classmethod
    def find_by_id(cls, id):
        return ItemsModel.query.filter_by(id=id).first()

    @classmethod
    def find_by_name(cls, name):
        return ItemsModel.query.filter_by(name=name).first()

    @classmethod
    def delete_by_name(cls, name):
        try:
            # saving data
            db.session.delete(ItemsModel.query.filter_by(name=name).first())
            db.session.commit()
        except:
            raise Exception("Error deleting entry by name in database")

    @classmethod
    def retrieveAllEntries(cls):
        return ItemsModel.query.all()

    @classmethod
    def retrieveByUnplayed(cls):
        return ItemsModel.query.filter_by(played=0).all()

