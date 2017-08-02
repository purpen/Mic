# -*- coding: utf-8 -*-
from ..utils import timestamp
from app import db, uploader


class Directory(db.Model):
    """Directory of the assets"""
    __tablename__ = 'fp_directory'

    id = db.Column(db.Integer, primary_key=True)
    master_uid = db.Column(db.Integer, index=True, default=0)
    site_id = db.Column(db.Integer, index=True, default=0)
    name = db.Column(db.String(50), index=True)
    user_id = db.Column(db.Integer, default=0)
    parent_id = db.Column(db.Integer, default=0)
    top = db.Column(db.SmallInteger, default=0)
    type = db.Column(db.SmallInteger, default=1)

    # directory and asset, 1 to N
    assets = db.relationship(
        'Asset', backref='directory', lazy='dynamic'
    )

    def __repr__(self):
        return '<Directory {}>'.format(self.name)


class Asset(db.Model):
    """Asset table.(image、file、video、pdf)"""
    __tablename__ = 'fp_asset'

    id = db.Column(db.Integer, primary_key=True)
    master_uid = db.Column(db.Integer, index=True, default=0)
    site_id = db.Column(db.Integer, index=True, default=0)

    user_id = db.Column(db.Integer, default=0)

    directory_id = db.Column(db.Integer, db.ForeignKey('fp_directory.id'))

    filepath = db.Column(db.String(128), unique=True, nullable=False)
    filename = db.Column(db.String(255), nullable=False)
    duration = db.Column(db.Float, nullable=True)
    size = db.Column(db.Float, nullable=True)
    width = db.Column(db.Integer, default=0)
    height = db.Column(db.Integer, default=0)
    mime = db.Column(db.String(64), nullable=True)
    type = db.Column(db.SmallInteger, default=1)

    state = db.Column(db.SmallInteger, default=1)
    created_at = db.Column(db.Integer, default=timestamp)
    updated_at = db.Column(db.Integer, default=timestamp, onupdate=timestamp)


    @property
    def view_url(self):
        return uploader.url(self.filepath)


    def __repr__(self):
        return '<Asset {}>'.format(self.filepath)


    def to_json(self):
        """资源和JSON的序列化转换"""
        json_asset = {
            'id': self.id,
            'view_url': uploader.url(self.filepath),
            'filepath': self.filepath,
            'filename': self.filename,
            'created_at': self.created_at
        }
        return json_asset
