# -*- coding: utf-8 -*-
from datetime import datetime
from flask_babelex import gettext
from app import db
from ..utils import DBEnum

class OrderStatusEnum(DBEnum):
    cancelled = gettext('cancelled')
    closed = gettext('closed')
    open = gettext('open')
    pending = gettext('pending')
    paid = gettext('paid')
    sent = gettext('sent')
    received = gettext('received')


class Order(db.Model):
    __tablename__ = 'fp_order'

    id = db.Column(db.Integer, primary_key=True)
    master_uid = db.Column(db.Integer, index=True, default=0)

    # order number id
    rid = db.Column(db.String(11), unique=True, index=True, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('fp_user.id'))
    address_id = db.Column(db.Integer, db.ForeignKey('fp_address.id'))

    description = db.Column(db.String(200))
    pay_money = db.Column(db.Float(10, 2))
    total_money = db.Column(db.Float(10, 2))
    discount_money = db.Column(db.Float(10, 2))
    gift_money = db.Column(db.Float(10, 2))


    freight = db.Column(db.Float(10, 2))


    status = db.Column(db.Enum(*OrderStatusEnum.get_enum_labels()), default=OrderStatusEnum.pending.value)
    payed_at = db.Column(db.DateTime)
    cancelled_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow())
    updated_at = db.Column(db.DateTime, default=datetime.utcnow())

    from_site = db.Column(db.String(60))

    # order and order_detail => 1 to N
    details = db.relationship(
        'OrderDetail', backref='Order', lazy='dynamic'
    )

    def __repr__(self):
        return '<Order {}>'.format(self.rid)

    def __str__(self):
        return self.rid


class OrderDetail(db.Model):
    __tablename__ = 'fp_order_detail'

    id = db.Column(db.Integer, primary_key=True)
    master_uid = db.Column(db.Integer, index=True, default=0)

    order_id = db.Column(db.Integer, db.ForeignKey('fp_order.id'))
    product_id = db.Column(db.Integer, db.ForeignKey('fp_product.id'))
    price = db.Column(db.Float(10, 2))
    quantity = db.Column(db.Integer, default=1)
    delivery_date = db.Column(db.DateTime)
    rate = db.Column(db.Integer, default=0)
    rate_comment = db.Column(db.String(200))

    def __repr__(self):
        return '<OrderDetail {}>'.format(self.id)

    def __str__(self):
        return self.id


class Cart(db.Model):
    __tablename__ = 'fp_cart'

    id = db.Column(db.Integer, primary_key=True)
    master_uid = db.Column(db.Integer, index=True, default=0)

    api_id = db.Column(db.Integer, default=0)
    customer_id = db.Column(db.Integer, default=0)
    session_id = db.Column(db.String(32), nullable=False)
    product_id = db.Column(db.Integer)
    recurring_id = db.Column(db.Integer, default=0)
    option = db.Column(db.Text)
    quantity = db.Column(db.Integer, default=1)

    def __str__(self):
        return self.id

