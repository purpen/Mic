# -*- coding: utf-8 -*-
from sqlalchemy import text, event
from sqlalchemy.sql import func
from app import db
from app.utils import timestamp

__all__ = [
    'Site',
    'SiteSeo'
]

class Site(db.Model):
    """官网信息"""

    __tablename__ = 'fp_site'

    id = db.Column(db.Integer, primary_key=True)
    master_uid = db.Column(db.Integer, index=True, default=0)
    name = db.Column(db.String(64), unique=True, index=True, nullable=False)
    # 生成编号
    serial_no = db.Column(db.String(32), unique=True, index=True, nullable=False)
    # 默认域名(系统默认生成)
    visit_url = db.Column(db.String(100), unique=True, nullable=False)
    # 绑定的独立域名
    site_domain = db.Column(db.String(100), unique=True, nullable=True)
    favicon = db.Column(db.String(100), nullable=True)
    # 套餐标准，1、免费版 2、vip版本 3、定制版
    pricing = db.Column(db.SmallInteger, default=1)

    locale = db.Column(db.String(4), default='zh')
    country = db.Column(db.String(30), nullable=True)
    currency = db.Column(db.String(10), default='CNY')
    # 行业范围
    domain = db.Column(db.SmallInteger, default=1)
    copyright = db.Column(db.String(100), nullable=True)
    description = db.Column(db.Text)

    # 合作伙伴代码
    unicode = db.Column(db.String(64), nullable=True)

    # 状态: 开启、禁用
    status = db.Column(db.Boolean, default=True)

    created_at = db.Column(db.Integer, default=timestamp)
    update_at = db.Column(db.Integer, default=timestamp, onupdate=timestamp)

    # site => brand, 1 => N
    brands = db.relationship(
        'Brand', backref='site', lazy='dynamic'
    )

    @staticmethod
    def master_site_id(user):
        """获取官网ID"""
        if user.is_master:
            return user.site_id
        # 如不是主账号
        master_user = User.query.get(user.master_uid)
        return master_user.site_id if master_user else 0

    @staticmethod
    def make_unique_serial_no():
        serial_no = Counter.gen_store_sn()
        if Site.query.filter_by(serial_no=serial_no).first() == None:
            return serial_no
        while True:
            new_serial_no = Counter.gen_store_sn()
            if Site.query.filter_by(serial_no=new_serial_no).first() == None:
                break
        return new_serial_no

    @staticmethod
    def on_sync_change(mapper, connection, target):
        """同步事件"""
        target.visit_url = target.serial_no

    def __repr__(self):
        return '<Site {}>'.format(self.name)


class SiteSeo(db.Model):
    """店铺SEO优化设置"""

    __tablename__ = 'fp_site_seo'

    __table_args__ = (
        db.PrimaryKeyConstraint('site_id', 'language_id'),
    )

    site_id = db.Column(db.Integer, db.ForeignKey('fp_site.id'))
    language_id = db.Column(db.Integer, db.ForeignKey('fp_language.id'))

    title = db.Column(db.String(255), nullable=True)
    description = db.Column(db.String(255), nullable=True)
    keywords = db.Column(db.String(255), nullable=True)


    def __repr__(self):
        return '<SiteSeo {}>'.format(self.site_id)


# 添加监听事件, 实现触发器
event.listen(Site, 'before_insert', Site.on_sync_change)