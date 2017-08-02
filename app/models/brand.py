# -*- coding: utf-8 -*-
from datetime import datetime
from .asset import Asset
from app import db
from ..constant import BRAND_STATUS

class Company(db.Model):
    __tablename__ = 'fp_company'

    id = db.Column(db.Integer, primary_key=True)
    master_uid = db.Column(db.Integer, index=True, default=0)

    full_name = db.Column(db.String(50), index=True)
    address = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    time_limit = db.Column(db.String(50))
    business_scope = db.Text()

    # company and brand => 1 to N
    brands = db.relationship(
        'Brand', backref='company', lazy='dynamic'
    )

    def __repr__(self):
        return '<Company {}>'.format(self.full_name)

    def __str__(self):
        return self.full_name


class Brand(db.Model):
    __tablename__ = 'fp_brand'

    id = db.Column(db.Integer, primary_key=True)

    master_uid = db.Column(db.Integer, index=True, default=0)
    # 所属的官网
    site_id = db.Column(db.Integer, db.ForeignKey('fp_site.id'))

    name = db.Column(db.String(64), index=True)
    features = db.Column(db.String(100))
    description = db.Column(db.Text())

    logo_id = db.Column(db.Integer, default=0)
    banner_id = db.Column(db.Integer, default=0)

    company_id = db.Column(db.Integer, db.ForeignKey('fp_company.id'))

    # sort number
    sort_num = db.Column(db.SmallInteger, default=1)
    # status: 1、default; -1、online
    status = db.Column(db.SmallInteger, default=1)
    # whether recommend
    is_recommended = db.Column(db.Boolean, default=False)

    created_at = db.Column(db.DateTime(), index=True, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime(), default=datetime.utcnow)

    # brand and product => 1 to N
    products = db.relationship(
        'Product', backref='brand', lazy='dynamic'
    )

    @property
    def status_label(self):
        for status in BRAND_STATUS:
            if status[0] == self.status:
                return status

    def __repr__(self):
        return '<Brand {}>'.format(self.name)




    @property
    def logo(self):
        """logo asset info"""
        return Asset.query.get(self.logo_id) if self.logo_id else None


    @property
    def banner(self):
        """brand asset info"""
        return Asset.query.get(self.banner_id) if self.banner_id else None