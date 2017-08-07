# -*- coding: utf-8 -*-
from sqlalchemy import text, event
from sqlalchemy.sql import func
from app import db
from app.utils import timestamp
from .settings import Language, Currency

__all__ = [
    'Site',
    'SiteSeo'
]

# site and country => N to N
site_country_table = db.Table(
    'fp_site_country',
    db.Column('site_id', db.Integer, db.ForeignKey('fp_site.id')),
    db.Column('country_id', db.Integer, db.ForeignKey('fp_country.id'))
)

# site and language => N to N
site_language_table = db.Table(
    'fp_site_language',
    db.Column('site_id', db.Integer, db.ForeignKey('fp_site.id')),
    db.Column('language_id', db.Integer, db.ForeignKey('fp_language.id'))
)

# site and currency => N to N
site_currency_table = db.Table(
    'fp_site_currency',
    db.Column('site_id', db.Integer, db.ForeignKey('fp_site.id')),
    db.Column('currency_id', db.Integer, db.ForeignKey('fp_currency.id'))
)


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

    # 行业范围
    domain = db.Column(db.SmallInteger, default=1)
    copyright = db.Column(db.String(100), nullable=True)
    description = db.Column(db.Text)

    # 默认值，语言、国家、币种
    default_country = db.Column(db.Integer, default=0)
    default_language = db.Column(db.Integer, default=0)
    default_currency = db.Column(db.Integer, default=0)

    # 合作伙伴代码
    unicode = db.Column(db.String(64), nullable=True)

    # 状态: 开启、禁用
    status = db.Column(db.Boolean, default=True)

    created_at = db.Column(db.Integer, default=timestamp)
    update_at = db.Column(db.Integer, default=timestamp, onupdate=timestamp)

    # site => country, N => N
    countries = db.relationship(
        'Country', secondary=site_country_table, backref='sites'
    )

    # site => language, N => N
    languages = db.relationship(
        'Language', secondary=site_language_table, backref='sites'
    )

    # site => currency, N => N
    currencies = db.relationship(
        'Currency', secondary=site_currency_table, backref='sites'
    )

    # site => brand, 1 => N
    brands = db.relationship(
        'Brand', backref='site', lazy='dynamic'
    )

    # site => category, 1 => N
    categories = db.relationship(
        'Category', backref='site', lazy='dynamic'
    )

    # site => product, 1 => N
    products = db.relationship(
        'Product', backref='site', lazy='dynamic'
    )


    @property
    def default_currency_unit(self):
        currency = Currency.query.get(int(self.default_currency))
        return currency.code


    def update_languages(self, languages):
        """更新语言选项"""

        # 检测默认语言是否选中，如未选择，则自动添加
        default_language = Language.query.get(int(self.default_language))
        if default_language not in languages:
            languages.append(default_language)

        self.languages = [lang for lang in languages]


    def update_currencies(self, currencies):
        """更新支持的货币"""

        # 检测默认货币是否选中，如未选择，则自动添加
        default_currency = Currency.query.get(int(self.default_currency))
        if default_currency not in currencies:
            currencies.append(default_currency)

        self.currencies = [currency for currency in currencies]


    def update_countries(self, countries):
        """更新支持的国家"""
        self.countries = [country for country in countries]


    @property
    def support_languages(self):
        """官网支持的语言, 默认语言设置为第一个"""
        support_languages =[]
        default_language = None
        for lang in self.languages:
            if lang.id == self.default_language:
                default_language = lang
            else:
                support_languages.append(lang)

        # 默认语言添加至第一个
        support_languages.insert(0, default_language)

        return support_languages


    @staticmethod
    def master_site_id(user):
        """获取官网ID"""
        if user.is_master:
            return user.site_id
        # 如不是主账号
        master_user = User.query.get(user.master_uid)
        return master_user.site_id if master_user else 0

    @staticmethod
    def current_site(master_uid=0, site_id=0):
        """获取当前官网"""
        if site_id:
            return Site.query.get(int(site_id))

        if master_uid:
            return Site.query.filter_by(master_uid=master_uid).first()

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