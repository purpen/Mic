# -*- coding: utf-8 -*-
import time
from sqlalchemy import text, event
from sqlalchemy.sql import func
from app import db
from app.utils import timestamp

from .asset import Asset

__all__ = [
    'Language',
    'Currency',
    'Country',
    'Zone',
    'ZoneGeoZone',
    'Counter'
]

class Language(db.Model):
    __tablename__ = 'fp_language'

    id = db.Column(db.Integer, primary_key=True)
    master_uid = db.Column(db.Integer, index=True, default=0)
    name = db.Column(db.String(64), unique=True, index=True, nullable=False)
    code = db.Column(db.String(5), unique=True, nullable=False)
    locale = db.Column(db.String(255), nullable=False)
    icon_id = db.Column(db.Integer, default=0)
    directory = db.Column(db.String(32))
    sort_order = db.Column(db.Integer, default=1)
    status = db.Column(db.SmallInteger, default=1)

    @property
    def icon(self):
        """logo asset info"""
        return Asset.query.get(self.icon_id) if self.icon_id else None

    def __repr__(self):
        return '<Language {}>'.format(self.name)



class Currency(db.Model):
    __tablename__ = 'fp_currency'

    id = db.Column(db.Integer, primary_key=True)
    master_uid = db.Column(db.Integer, index=True, default=0)
    title = db.Column(db.String(32), unique=True, nullable=False)
    code = db.Column(db.String(3), nullable=False)
    symbol_left = db.Column(db.String(12), nullable=True)
    symbol_right = db.Column(db.String(12), nullable=True)
    decimal_place = db.Column(db.String(1), nullable=False)
    value = db.Column(db.Float(15, 8), nullable=False)
    status = db.Column(db.SmallInteger, default=1)
    updated_at = db.Column(db.Integer, default=timestamp, onupdate=timestamp)
    last_updated = db.Column(db.Integer, default=timestamp)


    def __str__(self):
        return self.title


class Country(db.Model):
    __tablename__ = 'fp_country'

    id = db.Column(db.Integer, primary_key=True)
    master_uid = db.Column(db.Integer, index=True, default=0)
    name = db.Column(db.String(128), unique=True, index=True, nullable=False)
    iso_code_2 = db.Column(db.String(2), nullable=True)
    iso_code_3 = db.Column(db.String(3), nullable=True)
    address_format = db.Column(db.String(255), nullable=True)
    postcode_required = db.Column(db.Boolean, default=False)
    status = db.Column(db.SmallInteger, default=1)


    def __str__(self):
        return self.name



class Zone(db.Model):
    __tablename__ = 'fp_zone'

    id = db.Column(db.Integer, primary_key=True)
    master_uid = db.Column(db.Integer, index=True, default=0)
    country_id = db.Column(db.Integer, db.ForeignKey('fp_country.id'))
    name = db.Column(db.String(128), nullable=False)
    code = db.Column(db.String(32), nullable=False)
    status = db.Column(db.SmallInteger, default=1)

    def __str__(self):
        return self.name


class GeoZone(db.Model):
    __tablename__ = 'fp_geo_zone'

    id = db.Column(db.Integer, primary_key=True)
    master_uid = db.Column(db.Integer, index=True, default=0)
    name = db.Column(db.String(32))
    description = db.Column(db.String(255))
    created_at = db.Column(db.Integer, default=timestamp)
    updated_at = db.Column(db.Integer, default=timestamp, onupdate=timestamp)

    def __str__(self):
        return self.name


class ZoneGeoZone(db.Model):
    __tablename__ = 'fp_zone_geo_zone'

    id = db.Column(db.Integer, primary_key=True)
    master_uid = db.Column(db.Integer, index=True, default=0)
    country_id = db.Column(db.Integer, db.ForeignKey('fp_country.id'))
    zone_id = db.Column(db.Integer, db.ForeignKey('fp_zone.id'))
    geo_zone_id = db.Column(db.Integer, db.ForeignKey('fp_geo_zone.id'))
    created_at = db.Column(db.Integer, default=timestamp)
    updated_at = db.Column(db.Integer, default=timestamp, onupdate=timestamp)

    def __str__(self):
        return 'Zone to Zone %s' % self.id


class Counter(db.Model):
    """总计数器"""

    __tablename__ = 'fp_counter'

    id = db.Column(db.Integer, primary_key=True)
    total_count = db.Column(db.Integer, default=1)

    @staticmethod
    def get_next_sequence():
        current_counter = Counter.query.first()
        if current_counter is not None:
            total_count = current_counter.total_count
            # 同步递增
            current_counter.total_count += 1
        else:
            total_count = 1
            new_counter = Counter(total_count=total_count)
            db.session.add(new_counter)

        return total_count


    @staticmethod
    def gen_store_sn(length=7):
        serial_no = '2'
        rd = str(Counter.get_next_sequence())
        z = ''
        if len(rd) < length:
            for i in range(length - len(rd)):
                z += '0'

        return ''.join([serial_no, z, rd])


    @staticmethod
    def gen_user_xid(length=8):
        serial_no = '1'
        serial_no += time.strftime('%d')
        rd = str(Counter.get_next_sequence())
        z = ''
        if len(rd) < length:
            for i in range(length - len(rd)):
                z += '0'

        return ''.join([serial_no, z, rd])

    def __repr__(self):
        return '<Counter {}>'.format(self.id)