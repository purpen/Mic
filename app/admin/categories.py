# -*- coding: utf-8 -*-

from flask import render_template, redirect, url_for, flash, request, abort, current_app, jsonify
from flask_babelex import gettext
from flask_sqlalchemy import Pagination
from wtforms import ValidationError

from app.models import Category, CategoryDescription, Language, Asset
from app import db

from . import admin
from .forms import CategoryForm

@admin.route('/categories')
@admin.route('/categories/<int:page>')
def show_categories(page=1):
    per_page = request.args.get('per_page', 10, type=int)

    total = Category.query.count()

    categories = Category.always_category(path=0, page=1, per_page=per_page)

    paginated_categories = []
    for cate in categories:
        category = {
            'id': cate.id,
            'name': cate.name,
            'icon': Asset.query.get(cate.icon_id) if cate.icon_id else None,
            'sort_order': cate.sort_order,
            'status': cate.status
        }
        paginated_categories.append(category)

    pagination = Pagination(query=None, page=1,per_page=per_page,total=total, items=None)

    return render_template('admin/categories/show_list.html',
                           paginated_categories=paginated_categories,
                           pagination=pagination
                           )

@admin.route('/categories/repair')
@admin.route('/categories/repair/<int:parent_id>')
def repair_category_path(parent_id=0):
    Category.repair_categories(parent_id)
    return redirect(url_for('.show_categories'))


@admin.route('/categories/create', methods=['GET', 'POST'])
def create_category():
    form = CategoryForm()
    languages = Language.query.filter_by(status=1).all()
    if form.validate_on_submit():
        # if parent_id有值，则不是一级分类
        if form.parent_id.data:
            form.top.data = False

        # category description ImmutableMultiDict([('csrf_token', 'IjQ2OGZhZjg5NjM0Jk'),
        # ('category_description[1][name]', '数码'), ('category_description[1][description]', '电子'),
        # ('category_description[2][name]', 'shuma'), ('category_description[2][description]', 'dianzi'),
        # ('category_description[3][name]', ''), ('category_description[3][description]', ''),
        # ('parent_id', '0'), ('top', ''), ('icon', '0'), ('cover', '0'), ('sort_order', '1')])

        category_description_list = []
        for lang in languages:
            cate = {}
            cate['language_id'] = lang.id
            cate['name'] = request.form.get('category_description[%d][name]' % lang.id)
            cate['description'] = request.form.get('category_description[%d][description]' % lang.id)
            # todo: validate name
            category_description_list.append(cate)



        # save category
        category = Category(
            top=form.top.data,
            parent_id=form.parent_id.data,
            icon_id=form.icon.data,
            cover_id=form.cover.data,
            sort_order=form.sort_order.data
        )
        db.session.add(category)

        # save category description
        for cate_dict in category_description_list:
            cate_desc = CategoryDescription(category=category, **cate_dict)
            db.session.add(cate_desc)

        db.session.commit()

        #try:
        #    db.session.add(category)
        #    db.session.commit()
        #except:
        #    db.session.rollback()

        # rebuild category path
        Category.repair_categories(category.parent_id)

        flash('Add category is ok!', 'success')

        return redirect(url_for('.show_categories'))

    mode = 'create'
    category = None
    paginated_categories = Category.always_category(path=0, page=1, per_page=100)

    return render_template('admin/categories/create_and_edit.html',
                           form=form,
                           category=category,
                           mode=mode,
                           languages=languages,
                           all_descriptions=None,
                           paginated_categories=paginated_categories)


@admin.route('/categories/<int:id>/edit', methods=['GET', 'POST'])
def edit_category(id):
    mode = 'edit'

    languages = Language.query.filter_by(status=1).all()
    category = Category.query.get_or_404(id)

    form = CategoryForm()
    if form.validate_on_submit():
        category.top = form.top.data
        category.parent_id = form.parent_id.data
        category.icon_id = form.icon.data
        category.cover_id = form.cover.data
        category.sort_order = form.sort_order.data

        # update category description
        for cate_desc in category.category_descriptions:
            lang_id = cate_desc.language_id
            cate_desc.name = request.form.get('category_description[%d][name]' % lang_id)
            cate_desc.description = request.form.get('category_description[%d][description]' % lang_id)

        db.session.commit()

        # rebuild category path
        Category.repair_categories(category.parent_id)

        flash('Edit category is ok!', 'success')

        return redirect(url_for('.show_categories'))

    paginated_categories = Category.always_category(path=0, page=1, per_page=100)

    return render_template('admin/categories/create_and_edit.html',
                           form=form,
                           category=category,
                           mode=mode,
                           languages=languages,
                           all_descriptions=category.all_descriptions(),
                           paginated_categories=paginated_categories)


@admin.route('/categories/delete', methods=['POST'])
def delete_category():
    """批量或单个删除元素"""

    selected_ids = request.form.getlist('selected[]')
    if not selected_ids or selected_ids is None:
        flash('Delete category is null!', 'danger')
        abort(404)

    try:
        for id in selected_ids:
            category = Category.query.get_or_404(int(id))
            if category.has_children():
                flash(gettext("Category[%s] have child node, can't deleted!!!" % category.name), 'danger')
                return redirect(url_for('.show_categories'))

            db.session.delete(category)
            db.session.commit()
    except:
        pass

    flash('Delete category is ok!', 'success')

    return redirect(url_for('.show_categories'))