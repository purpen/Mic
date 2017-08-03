# -*- coding: utf-8 -*-
from flask import render_template, redirect, url_for, flash, request, abort
from flask_babelex import gettext
from flask_sqlalchemy import Pagination
from flask_login import login_required, current_user

from app.models import Product, Language, Site

from . import admin
from .forms import ProductForm
from ..utils import Master


def _admin_active_menu():
    return dict({
        'current_menu': 'products'
    })


@admin.route('/products')
@admin.route('/products/<int:page>')
@login_required
def show_products(page=1):
    per_page = request.args.get('per_page', 10, type=int)
    status = request.args.get('status', 0, type=int)

    current_site_id = Site.master_site_id(current_user)

    builder = Product.query.filter_by(site_id=current_site_id)
    if status:
        builder = builder.filter_by(status=status)

    paginated_products = builder.order_by(Product.created_at.desc()).paginate(page, per_page)

    if paginated_products:
        paginated_products.offset_start = 1 if page == 1 else (page - 1) * per_page
        paginated_products.offset_end = paginated_products.offset_start + len(paginated_products.items) - 1

    return render_template('admin/products/pro_list.html',
                           paginated_products=paginated_products)


@admin.route('/products/create', methods=['GET', 'POST'])
@login_required
def create_product():
    current_site_id = Site.master_site_id(current_user)
    site = Site.query.get_or_404(current_site_id)

    form = ProductForm()
    if form.validate_on_submit():

        flash('Add product is ok!', 'success')

        return redirect(url_for('.show_products'))

    mode = 'create'
    return render_template('admin/products/create_and_edit.html',
                           form=form,
                           mode=mode,
                           languages=site.languages)


@admin.route('/products/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_product(id):
    pass


@admin.route('/products/delete', methods=['POST'])
@login_required
def delete_product(id):
    pass