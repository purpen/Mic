# -*- coding: utf-8 -*-
from datetime import datetime
from app import db

class Address(db.Model):
    __tablename__ = 'fp_address'

    id = db.Column(db.Integer, primary_key=True)
    master_uid = db.Column(db.Integer, index=True, default=0)
    user_id = db.Column(db.Integer, db.ForeignKey('fp_user.id'))

    is_default = db.Column(db.Boolean, default=False)
    line_one = db.Column(db.String(100))
    line_two = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20))
    name_contact = db.Column(db.String(100))
    zipcode = db.Column(db.String(10))
    city = db.Column(db.String(50))
    country = db.Column(db.String(50))
    state = db.Column(db.String(50))

    created_at = db.Column(db.DateTime(), default=datetime.utcnow)
    updated_at = db.Column(db.DateTime(), default=datetime.utcnow)


    def __repr__(self):
        return '<Address {}>'.format(self.name_contact)

    def __str__(self):
        return self.name_contact
