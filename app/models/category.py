# -*- coding: utf-8 -*-
from sqlalchemy import text
from datetime import datetime
from .asset import Asset
from app import db


# product and tag => N to N
product_tag_table = db.Table('fp_product_tag',
                           db.Column(
                               'product_id', db.Integer, db.ForeignKey('fp_product.id')),
                           db.Column(
                               'tag_id', db.Integer, db.ForeignKey('fp_tag.id'))
                           )

# product and category => N to N
product_category_table = db.Table('fp_product_category',
                                  db.Column(
                                      'product_id', db.Integer, db.ForeignKey('fp_product.id')),
                                  db.Column(
                                      'category_id', db.Integer, db.ForeignKey('fp_category.id'))
                                  )

class Category(db.Model):
    __tablename__ = 'fp_category'

    id = db.Column(db.Integer, primary_key=True)
    master_uid = db.Column(db.Integer, index=True, default=0)

    parent_id = db.Column(db.Integer, default=0)
    top = db.Column(db.Boolean, default=True)
    sort_order = db.Column(db.Integer, default=1)

    icon_id = db.Column(db.Integer, default=0)
    cover_id = db.Column(db.Integer, default=0)

    status = db.Column(db.Boolean, default=False)
    type = db.Column(db.Enum('group', 'store'), default='store')

    created_at = db.Column(db.DateTime(), default=datetime.utcnow)
    updated_at = db.Column(db.DateTime(), default=datetime.utcnow)

    # N => N
    products = db.relationship(
        'Product', secondary=product_category_table, backref='categories'
    )

    # 1 => N
    category_descriptions = db.relationship(
        'CategoryDescription', backref='category', lazy='dynamic'
    )

    # all parent ids
    parent_ids = []

    @staticmethod
    def top_categories():
        """get top categories"""
        return Category.query.filter_by(parent_id=0).all()


    @classmethod
    def always_category(cls, path=0, page=1, per_page=20):
        """get category tree"""
        sql = "select cp.category_id, GROUP_CONCAT(cd1.name ORDER BY cp.level SEPARATOR '&nbsp;&nbsp;&gt;&nbsp;&nbsp;') AS name, c1.id, c1.status, c1.icon_id, c1.sort_order from fp_category_path cp " \
              "LEFT JOIN fp_category c1 ON (cp.category_id=c1.id) " \
              "LEFT JOIN fp_category c2 ON (cp.path_id=c2.id)" \
              "LEFT JOIN fp_category_description AS cd1 ON (cp.path_id = cd1.category_id) " \
              "LEFT JOIN fp_category_description AS cd2 ON (cp.category_id=cd2.category_id) WHERE cd1.language_id=1 AND cd2.language_id=1"

        sql += ' GROUP BY cp.category_id'
        sql += ' ORDER BY c1.sort_order DESC'

        if page == 1:
            offset = 0
        else:
            offset = (page - 1)*per_page

        sql += ' LIMIT %d, %d' % (offset, per_page)

        return db.engine.execute(text(sql))


    def all_descriptions(self):
        """get all descriptions and to dict"""
        all_descriptions = {}
        for cate_desc in self.category_descriptions:
            all_descriptions[cate_desc.language_id] = cate_desc
        return all_descriptions


    @classmethod
    def repair_categories(cls, parent_id=0):
        """repair category path"""

        categories = Category.query.filter_by(parent_id=parent_id).all()

        for cate in categories:
            db.engine.execute("DELETE FROM `fp_category_path` WHERE category_id=%d" % cate.id)

            level = 0

            categories_paths = CategoryPath.query.filter_by(category_id=parent_id).order_by(
                CategoryPath.level.asc()).all()
            for cp in categories_paths:
                cp = CategoryPath(category_id=cate.id, path_id=cp.path_id, level=level)
                db.session.add(cp)

                level += 1

            db.engine.execute(
                'REPLACE INTO `fp_category_path` SET category_id=%d, path_id=%d, level=%d' % (cate.id, cate.id, level))

            db.session.commit()

            Category.repair_categories(cate.id)


    def has_children(self):
        """whether or not a child node"""
        return self.query.filter_by(parent_id=self.id).first()


    @property
    def icon(self):
        """icon asset info"""
        return Asset.query.get(self.icon_id) if self.icon_id else None


    @property
    def cover(self):
        """cover asset info"""
        return Asset.query.get(self.cover_id) if self.cover_id else None


    def __repr__(self):
        return '<Category {}>'.format(self.id)


    def __str__(self):
        return self.id


class CategoryDescription(db.Model):
    __tablename__ = 'fp_category_description'

    __table_args__ = (
        db.PrimaryKeyConstraint('category_id', 'language_id'),
    )

    category_id = db.Column(db.Integer, db.ForeignKey('fp_category.id'))
    language_id = db.Column(db.Integer, db.ForeignKey('fp_language.id'))

    name = db.Column(db.String(64), unique=True, index=True)
    description = db.Column(db.String(140))
    meta_title = db.Column(db.String(255), nullable=True)
    meta_description = db.Column(db.String(255), nullable=True)
    meta_keyword = db.Column(db.String(255), nullable=True)

    def __str__(self):
        return self.name


class CategoryPath(db.Model):
    __tablename__ = 'fp_category_path'

    __table_args__ = (
        db.PrimaryKeyConstraint('category_id', 'path_id'),
    )

    category_id = db.Column(db.Integer, db.ForeignKey('fp_category.id'))
    path_id = db.Column(db.Integer, default=0)
    level = db.Column(db.Integer, default=0)

    def __str__(self):
        return '<CategoryPath %s,%s>' % (self.category_id, self.path_id)


class Banner(db.Model):
    __tablename__ = 'fp_banner'

    id = db.Column(db.Integer, primary_key=True)
    master_uid = db.Column(db.Integer, index=True, default=0)

    name = db.Column(db.String(64), nullable=False)
    status = db.Column(db.SmallInteger, default=0)

    def __str__(self):
        return self.name


class BannerImage(db.Model):
    __tablename__ = 'fp_banner_image'

    id = db.Column(db.Integer, primary_key=True)
    master_uid = db.Column(db.Integer, index=True, default=0)

    banner_id = db.Column(db.Integer, db.ForeignKey('fp_banner.id'))
    language_id = db.Column(db.Integer, db.ForeignKey('fp_language.id'))
    title = db.Column(db.String(64), nullable=False)
    link = db.Column(db.String(255))
    image = db.Column(db.Integer, db.ForeignKey('fp_asset.id'))
    sort_order = db.Column(db.Integer, default=0)

    def __str__(self):
        return self.title


class Tag(db.Model):
    __tablename__ = 'fp_tag'

    id = db.Column(db.Integer, primary_key=True)
    master_uid = db.Column(db.Integer, index=True, default=0)

    name = db.Column(db.String(20), unique=True, index=True)
    sim_name = db.Column(db.String(100))

    products = db.relationship(
        'Product', secondary=product_tag_table, backref='tags'
    )

    def __repr__(self):
        return '<Tag {}>'.format(self.name)

    def __str__(self):
        return self.name

