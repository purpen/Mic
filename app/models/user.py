# -*- coding: utf-8 -*-

from datetime import datetime
from flask import current_app
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask_login import UserMixin, AnonymousUserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from ..utils import is_sequence
from app import db, login_manager

# 定义user与role关系的辅助表
user_role_table = db.Table('fp_user_role',
                           db.Column(
                               'user_id', db.Integer, db.ForeignKey('fp_user.id')),
                           db.Column(
                               'role_id', db.Integer, db.ForeignKey('fp_role.id')
                           ))

# 定义role与ability关系的辅助表
role_ability_table = db.Table('fp_role_ability',
                              db.Column(
                                  'role_id', db.Integer, db.ForeignKey('fp_role.id')),
                              db.Column(
                                  'ability_id', db.Integer, db.ForeignKey('fp_ability.id')
                              ))

class User(UserMixin, db.Model):
    __tablename__ = 'fp_user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    confirmed = db.Column(db.Boolean, default=False)

    # 真实资料信息
    name = db.Column(db.String(64))
    location = db.Column(db.String(64))
    about_me = db.Column(db.Text())
    member_since = db.Column(db.DateTime(), default=datetime.utcnow)
    last_seen = db.Column(db.DateTime(), default=datetime.utcnow)

    roles = db.relationship(
        'Role', secondary=user_role_table, backref='users'
    )

    def belong_roles(self):
        return [role.name for role in self.roles]

    def add_roles(self, *roles):
        """添加用户角色"""
        self.roles.extend([role for role in roles if role not in self.roles])

    def remove_roles(self, *roles):
        """删除用户角色"""
        self.roles = [role for role in self.roles if role not in roles]


    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_confirmation_token(self, expiration=3600):
        """生成一个令牌，有效期默认为一小时."""
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm': self.id})

    def confirm(self, token):
        """检验令牌，如果检验通过，则把新添加的confirmed 属性设为True."""
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False

        if data.get('confirm') != self.id:
            return False

        # 更新状态
        self.confirmed = True
        db.session.add(self)
        db.session.commit()

        return True

    def ping(self):
        """每次收到用户的请求时都要调用ping()方法"""
        self.last_seen = datetime.utcnow()
        db.session.add(self)

    # API基于令牌的认证
    def generate_auth_token(self, expiration):
        s = Serializer(current_app.config['SECRET_KEY'],
                       expires_in=expiration)
        return s.dumps({'id': self.id})

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return None

        return User.query.get(data['id'])

    @staticmethod
    def generate_fake(count=100):
        """自动生成测试数据"""
        from sqlalchemy.exc import IntegrityError
        from random import seed
        import forgery_py

        seed()
        for i in range(count):
            u = User(email=forgery_py.internet.email_address(),
                     username=forgery_py.internet.user_name(True),
                     password=forgery_py.lorem_ipsum.word(),
                     confirmed=True,
                     name=forgery_py.name.full_name(),
                     location=forgery_py.address.city(),
                     about_me=forgery_py.lorem_ipsum.sentence(),
                     member_since=forgery_py.date.date(True))
            db.session.add(u)
            try:
                db.session.commit()
            except:
                db.session.rollback()

    def __repr__(self):
        return '<User %r>' % self.username


class Role(db.Model):
    """
    Subclass this for your roles
    """
    __tablename__ = 'fp_role'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True)

    abilities = db.relationship(
        'Ability', secondary=role_ability_table, backref='roles'
    )

    def add_abilities(self, *abilities):
        """批量添加权限"""
        for ability in abilities:
            existing_ability = Ability.query.filter_by(name=ability).first()
            if not existing_ability:
                existing_ability = Ability(ability)
                db.session.add(existing_ability)
                db.session.commit()
            self.abilities.append(existing_ability)

    def remove_abilities(self, *abilities):
        """批量删除权限"""
        for ability in abilities:
            existing_ability = Ability.query.filter_by(name=ability).first()
            if existing_ability and existing_ability in self.abilities:
                self.abilities.remove(existing_ability)

    def __init__(self, name):
        self.name = name.lower()

    def __repr__(self):
        return '<Role {}>'.format(self.name)

    def __str__(self):
        return self.name


class Ability(db.Model):
    __tablename__ = 'fp_ability'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True)

    def __init__(self, name):
        self.name = name.lower()

    def __repr__(self):
        return '<Ability {}>'.format(self.name)

    def __str__(self):
        return self.name


class AnonymousUser(AnonymousUserMixin):
    def belong_roles(self):
        return []

login_manager.anonymous_user = AnonymousUser

@login_manager.user_loader
def load_user(user_id):
    """使用指定的标识符加载用户"""
    return User.query.get(int(user_id))



