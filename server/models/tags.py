from db import db
import json


class TagsModel(db.Model):
    __tablename__ = 'tags'  # This is table name

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)

    def __init__(self, name):
        self.name = name

    def json(self):
        return json.loads(json.dumps(self, default=lambda o: {'id': self.id, 'name': self.name}))

    def save_to_db(self):
        try:
            # saving data
            db.session.add(self)
            db.session.commit()
        except:
            raise Exception("Error saving tag in database or duplicated value")

    def delete_from_db(self):
        try:
            # saving data
            db.session.remove(self)
            db.session.commit()
        except:
            raise Exception("Error deleting tag in database")

    @classmethod
    def find_by_id(cls, id):
        return TagsModel.query.filter_by(id=id).first()

    @classmethod
    def find_by_name(cls, name):
        return TagsModel.query.filter_by(name=name).first()

    @classmethod
    def delete_by_name(cls, name):
        try:
            # saving data
            db.session.delete(TagsModel.query.filter_by(name=name).first())
            db.session.commit()
        except:
            raise Exception("Error deleting entry by name in database")

    @classmethod
    def retrieveAllEntries(cls):
        return TagsModel.query.all()

