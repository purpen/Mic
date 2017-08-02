# -*- coding: utf-8 -*-
from flask import render_template, redirect, url_for, flash, request, abort, current_app
from flask_login import current_user
from app.models import Brand, Site
from app import db

from . import admin
from .forms import BrandForm, EditBrandForm
from ..utils import Master


@admin.route('/brands')
@admin.route('/brands/<int:page>')
def show_brands(page=1):
    per_page = request.args.get('per_page', 10, type=int)
    status = request.args.get('status', 0, type=int)
    # 获取所属站点
    current_site_id = Site.master_site_id(current_user)

    builder = Brand.query.filter_by(site_id=current_site_id)
    if status:
        builder = builder.filter_by(status=status)

    paginated_brands = builder.order_by(Brand.created_at.desc()).paginate(page, per_page)

    if paginated_brands:
        paginated_brands.offset_start = 1 if page == 1 else (page - 1) * per_page
        paginated_brands.offset_end = paginated_brands.offset_start + len(paginated_brands.items) - 1

    return render_template('admin/brands/show_list.html',
                           paginated_brands=paginated_brands)


@admin.route('/brands/create', methods=['GET', 'POST'])
def create_brand():
    form = BrandForm()
    if form.validate_on_submit():
        master_uid = Master.master_uid()
        current_site = Site.query.filter_by(master_uid=master_uid).first()

        brand = Brand(
            master_uid=master_uid,
            site_id=current_site.id,
            name=form.name.data,
            features=form.features.data,
            description=form.description.data,
            sort_num=form.sort_num.data,
            logo_id=form.logo.data,
            banner_id=form.banner.data
        )
        db.session.add(brand)

        db.session.commit()

        flash('Add brand is ok!', 'success')

        return redirect(url_for('.show_brands'))

    mode = 'create'
    brand = None
    return render_template('admin/brands/submit.html',
                           form=form,
                           brand=brand,
                           mode=mode)


@admin.route('/brands/<int:id>/edit', methods=['GET', 'POST'])
def edit_brand(id):
    brand = Brand.query.get_or_404(id)
    form = EditBrandForm(brand)
    if form.validate_on_submit():
        brand.name = form.name.data
        brand.features = form.features.data
        brand.description = form.description.data
        brand.logo_id = form.logo.data
        brand.banner_id = form.banner.data
        brand.sort_num = form.sort_num.data

        db.session.commit()

        flash('Edit brand is ok!', 'success')

        return redirect(url_for('.show_brands'))

    mode = 'edit'

    form.name.data = brand.name
    form.features.data = brand.features
    form.description.data = brand.description
    form.logo.data = brand.logo_id
    form.banner.data = brand.banner_id
    form.sort_num.data = brand.sort_num

    return render_template('admin/brands/submit.html',
                           form=form,
                           brand=brand,
                           mode=mode)


@admin.route('/brands/delete', methods=['POST'])
def delete_brand():
    """批量或单个删除元素"""
    selected_ids = request.form.getlist('selected[]')
    if not selected_ids or selected_ids is None:
        flash('Delete brand is null!', 'danger')
        abort(404)

    try:
        for id in selected_ids:
            brand = Brand.query.get_or_404(int(id))
            db.session.delete(brand)
        db.session.commit()
    except Exception as ex:
        current_app.logger.warn('Delete brand error: %s' % ex)

    flash('Delete brand is ok!', 'success')

    return redirect(url_for('.show_brands'))