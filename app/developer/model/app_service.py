from flask import current_app, url_for
from app import db
from app.models import PaginatedAPIMixin


class AppService(PaginatedAPIMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    application_id = db.Column(db.Integer, db.ForeignKey('application.id'))
    service_id = db.Column(db.Integer, db.ForeignKey('service.id'))

    def __repr__(self):
        return '<AppService application:{app} service:{srv}>'.format(app=self.application.name, srv=self.service.name)
   
    def to_dict(self):
        data = {
            'id': self.id
        }
        return data
    
    def from_dict(self, data):
        for field in []:
            if field in data:
                setattr(self, field, data[field])
