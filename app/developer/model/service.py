from flask import current_app, url_for
from app import db
from app.models import PaginatedAPIMixin


class Service(PaginatedAPIMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    description = db.Column(db.String(140))
    applications = db.relationship('AppService',
                               foreign_keys='AppService.service_id',
                               backref='service', 
                               lazy='dynamic')

    def __repr__(self):
        return '<Service {}>'.format(self.name)
   
    def to_dict(self):
        data = {
            'id': self.id,
            'name': self.username,
            'description': self.description
        }
        return data
    
    def from_dict(self, data):
        for field in ['name', 'description']:
            if field in data:
                setattr(self, field, data[field])
