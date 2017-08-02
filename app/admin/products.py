# -*- coding: utf-8 -*-

from flask import render_template, redirect, url_for, flash, request, abort

from app.models import Product, Language

from . import admin
from .forms import ProductForm


def _admin_active_menu():
    return dict({
        'current_menu': 'products'
    })

@admin.route('/products')
@admin.route('/products/<int:page>')
def show_products(page=1):
    per_page = request.args.get('per_page', 10, type=int)
    status = request.args.get('status', 0, type=int)

    if not status:
        query = Product.query
    else:
        query = Product.query.filter_by(status=status)

    paginated_products = query.order_by(Product.created_at.desc()).paginate(page, per_page)

    if paginated_products:
        paginated_products.offset_start = 1 if page == 1 else (page - 1) * per_page
        paginated_products.offset_end = paginated_products.offset_start + len(paginated_products.items) - 1

    return render_template('admin/products/pro_list.html',
                           paginated_products=paginated_products
                           )


@admin.route('/products/create', methods=['GET', 'POST'])
def create_product():
    form = ProductForm()
    if form.validate_on_submit():

        flash('Add product is ok!', 'success')

        return redirect(url_for('.show_products'))

    product = None
    mode = 'create'
    languages = Language.query.filter_by(status=1).all()
    return render_template('admin/products/create_and_edit.html',
                           form=form,
                           product=product,
                           mode=mode,
                           languages=languages
                           )


@admin.route('/products/<int:id>/edit', methods=['GET', 'POST'])
def edit_product(id):
    pass


@admin.route('/products/delete', methods=['POST'])
def delete_product(id):
    pass