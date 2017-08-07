# -*- coding: utf-8 -*-
from flask import render_template, redirect, url_for, flash, request, abort, current_app
from flask_babelex import gettext
from flask_sqlalchemy import Pagination
from flask_login import login_required, current_user

from .. import db
from ..models import Product, ProductDescription, ProductImage, ProductSku, Site, Counter, Category, Brand, Asset
from ..utils import Master, full_response, R201_CREATED, R204_NOCONTENT, custom_status
from . import admin
from .forms import ProductForm, ProductSkuForm


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

    current_site = Site.current_site(master_uid=Master.master_uid())

    builder = Product.query.filter_by(site_id=current_site.id)
    if status:
        builder = builder.filter_by(status=status)

    paginated_products = builder.order_by(Product.created_at.desc()).paginate(page, per_page)

    if paginated_products:
        paginated_products.offset_start = 1 if page == 1 else (page - 1) * per_page
        paginated_products.offset_end = paginated_products.offset_start + len(paginated_products.items) - 1

    return render_template('admin/products/pro_list.html',
                           current_site=current_site,
                           paginated_products=paginated_products)


@admin.route('/products/create', methods=['GET', 'POST'])
@login_required
def create_product():
    current_site = Site.current_site(master_uid=Master.master_uid())
    site_languages = current_site.support_languages
    brands = Brand.query.filter_by(site_id=current_site.id, status=1).all()

    form = ProductForm()
    # 初始品牌选项
    brand_list = [(brand.id, brand.name) for brand in brands]
    brand_list.insert(0, (0, gettext('Select Brand')))
    form.brand_id.choices = brand_list

    if form.validate_on_submit():
        # 检验产品分类
        category_id_list = request.form.getlist('category_id_list')
        current_app.logger.debug('Product category %s' % category_id_list)
        if category_id_list is None or len(category_id_list) == 0:
            flash(gettext("Product category can't empty!"), 'danger')
            return redirect(url_for('.create_product'))

        # 检验产品的主图
        image_list = request.form.getlist('images[]')
        if image_list is None or len(image_list) == 0:
            flash(gettext("Product images can't empty!"), 'danger')
            return redirect(url_for('.create_product'))

        # 检测并构建产品信息
        product_description_list = []
        for lang in site_languages:
            product_name = request.form.get('product_description[%d][name]' % lang.id)
            if product_name is None or product_name == '':
                flash(gettext("Product name can't empty!"), 'danger')
                return redirect(url_for('.create_product'))

            product_description = {}
            product_description['master_uid'] = Master.master_uid()
            product_description['language_id'] = lang.id
            product_description['name'] = product_name
            product_description['description'] = request.form.get('product_description[%d][description]' % lang.id)
            product_description['meta_title'] = request.form.get('product_description[%d][meta_title]' % lang.id)
            product_description['meta_description'] = request.form.get('product_description[%d][meta_description]' % lang.id)
            product_description['meta_keyword'] = request.form.get('product_description[%d][meta_keyword]' % lang.id)

            product_description_list.append(product_description)

        # 保存产品数据
        new_sn = Counter.gen_product_sn()
        product = Product(
            site_id=current_site.id,
            master_uid=Master.master_uid(),
            user_id=current_user.id,
            serial_no = new_sn,
            sku = new_sn,
            cover_id = int(image_list[0]),
            brand_id = form.brand_id.data,
            quantity = form.quantity.data,
            price=form.price.data,
            sort_order=form.sort_order.data,
            type=form.type.data,
            status=form.status.data,
            is_shipping=form.shipping.data,
            date_available=form.date_available.data
        )
        db.session.add(product)

        # 同步更新产品信息
        for product_description in product_description_list:
            product_desc = ProductDescription(product=product, **product_description)
            db.session.add(product_desc)

        # 同步所属分类
        selected_categories = []
        for cate_id in category_id_list:
            category = Category.query.get(int(cate_id))
            selected_categories.append(category)

        product.update_categories(*selected_categories)

        # 同步产品的主图
        counter = 1
        for asset_id in image_list:
            product_image = ProductImage(product=product, **{
                'asset_id': int(asset_id),
                'sort_order': counter
            })
            db.session.add(product_image)

        db.session.commit()

        flash(gettext('Add product is ok!'), 'success')

        return redirect(url_for('.show_products'))
    else:
        current_app.logger.debug('Add product fail: %s' % form.errors)

    mode = 'create'

    # 分类
    paginated_categories = Category.always_category(site_id=current_site.id,
                                                    language_id=current_site.default_language,
                                                    path=0, page=1, per_page=100)

    return render_template('admin/products/create_and_edit.html',
                           form=form,
                           mode=mode,
                           image_list=[],
                           languages=site_languages,
                           current_site=current_site,
                           paginated_categories=paginated_categories)


@admin.route('/products/<string:rid>/edit', methods=['GET', 'POST'])
@login_required
def edit_product(rid):
    product = Product.query.filter_by(sku=rid).first()
    if product is None:
        abort(404)

    current_site = Site.current_site(master_uid=Master.master_uid())
    site_languages = current_site.support_languages
    brands = Brand.query.filter_by(site_id=current_site.id, status=1).all()

    form = ProductForm()
    # 初始品牌选项
    brand_list = [(brand.id, brand.name) for brand in brands]
    brand_list.insert(0, (0, gettext('Select Brand')))
    form.brand_id.choices = brand_list

    if form.validate_on_submit():
        # 检验产品的分类
        category_id_list = request.form.getlist('category_id_list')
        if category_id_list is None or len(category_id_list) == 0:
            flash(gettext("Product category can't empty!"), 'danger')
            return redirect(url_for('.edit_product', rid=rid))

        # 检验产品的主图
        image_list = request.form.getlist('images[]')
        if image_list is None or len(image_list) == 0:
            flash(gettext("Product images can't empty!"), 'danger')
            return redirect(url_for('.edit_product', rid=rid))

        # 同步更新产品信息
        for lang in site_languages:
            product_name = request.form.get('product_description[%d][name]' % lang.id)
            if product_name is None or product_name == '':
                flash(gettext("Product name can't empty!"), 'danger')
                return redirect(url_for('.edit_product', rid=rid))

            # 开始更新
            some_description = ProductDescription.query.filter_by(product_id=product.id, language_id=lang.id).first()
            if some_description:
                some_description.name = product_name
                some_description.description = request.form.get('product_description[%d][description]' % lang.id)
                some_description.meta_title = request.form.get('product_description[%d][meta_title]' % lang.id)
                some_description.meta_description = request.form.get('product_description[%d][meta_description]' % lang.id)
                some_description.meta_keyword = request.form.get('product_description[%d][meta_keyword]' % lang.id)

        # 更新数据
        product.cover_id = int(image_list[0])
        product.brand_id = form.brand_id.data
        product.quantity = form.quantity.data
        product.price = form.price.data
        product.sort_order = form.sort_order.data
        product.type = form.type.data
        product.status = form.status.data
        product.is_shipping = form.shipping.data
        product.date_available = form.date_available.data

        # 同步所属分类
        selected_categories = []
        for cate_id in category_id_list:
            category = Category.query.get(int(cate_id))
            selected_categories.append(category)

        product.update_categories(*selected_categories)

        # 同步更新产品主图
        _update_product_image(product.id, image_list)

        db.session.commit()

        flash(gettext('Update product is ok!'), 'success')

        return redirect(url_for('.show_products'))

    mode = 'edit'
    all_descriptions = {}
    for product_description in product.product_descriptions:
        all_descriptions[product_description.language_id] = product_description

    form.brand_id.data = product.brand_id
    form.quantity.data = product.quantity
    form.price.data = round(product.price, 2)
    form.sort_order.data = product.sort_order
    form.type.data = product.type
    form.status.data = product.status
    form.shipping.data = product.is_shipping
    form.date_available.data = product.date_available

    # 分类
    paginated_categories = Category.always_category(site_id=current_site.id,
                                                    language_id=current_site.default_language,
                                                    path=0, page=1, per_page=100)

    return render_template('admin/products/create_and_edit.html',
                           form=form,
                           mode=mode,
                           product=product,
                           image_list=product.image_list(),
                           languages=site_languages,
                           current_site=current_site,
                           all_descriptions=all_descriptions,
                           selected_categories=[cate.id for cate in product.categories],
                           paginated_categories=paginated_categories)


@admin.route('/products/delete', methods=['POST'])
@login_required
def delete_product(id):
    pass


@admin.route('/product/<string:pid>/show_skus', methods=['GET', 'POST'])
@login_required
def show_skus(pid):
    product_skus = ProductSku.query.filter_by(product_serial_no=pid).all()
    return render_template('/admin/products/show_skus.html',
                           product_skus=product_skus)


@admin.route('/product/<string:pid>/add_sku', methods=['GET', 'POST'])
@login_required
def add_sku(pid):
    product = Product.query.filter_by(serial_no=pid).first()
    form = ProductSkuForm()
    if form.validate_on_submit():
        # 设置默认值
        if not form.sku_cover_id.data:
            default_cover = Asset.query.filter_by(is_default=True).first()
            form.sku_cover_id.data = default_cover.id

        sku = ProductSku(
            product_id=product.id,
            product_serial_no=product.serial_no,
            master_uid=Master.master_uid(),
            serial_no=Counter.gen_product_sn(),
            cover_id=form.sku_cover_id.data,
            s_model=form.s_model.data,
            sale_price=form.sale_price.data,
            s_weight=form.s_weight.data,
            remark=form.remark.data
        )
        db.session.add(sku)

        db.session.commit()

        return full_response(True, R201_CREATED, sku.to_json())

    mode = 'create'
    form.serial_no.data = Counter.gen_product_sn()
    form.sale_price.data = round(product.price, 2)
    form.s_weight.data = product.weight

    return render_template('/admin/products/modal_sku.html',
                           form=form,
                           mode=mode,
                           post_sku_url=url_for('.add_sku', pid=pid),
                           product=product)

@admin.route('/product/edit_sku/<string:rid>', methods=['GET', 'POST'])
@login_required
def edit_sku(rid):
    sku = ProductSku.query.filter_by(serial_no=rid).first()
    product = Product.query.get_or_404(sku.product_id)
    form = ProductSkuForm()
    if form.validate_on_submit():
        sku.cover_id = form.sku_cover_id.data
        sku.s_model = form.s_model.data
        sku.s_weight = form.s_weight.data
        sku.sale_price = form.sale_price.data
        sku.remark = form.remark.data

        db.session.commit()

        return full_response(True, R201_CREATED, sku.to_json())

    mode = 'edit'

    form.serial_no.data = sku.serial_no
    form.sku_cover_id.data = sku.cover_id
    form.sale_price.data = sku.sale_price
    form.s_model.data = sku.s_model
    form.s_weight.data = sku.s_weight
    form.remark.data = sku.remark

    return render_template('/admin/products/modal_sku.html',
                           form=form,
                           mode=mode,
                           product=product,
                           post_sku_url=url_for('.edit_sku', rid=rid),
                           sku=sku)


@admin.route('/product/delete_sku/<string:rid>', methods=['POST'])
@login_required
def delete_sku(rid):
    try:
        sku = ProductSku.query.filter_by(serial_no=rid).first()

        db.session.delete(sku)
        db.session.commit()

        return full_response(True, R204_NOCONTENT, {'id': rid})
    except:
        db.session.rollback()
        return full_response(True, custom_status('Delete sku is failed!', 500))


def _update_product_image(product_id, image_ids):
    """更新产品图片"""
    counter = 1
    for asset_id in image_ids:
        product_image = ProductImage.query.filter_by(product_id=product_id, asset_id=int(asset_id)).first()
        if product_image:
            # 存在，则更新排序
            product_image.sort_order = counter
        else:
            # 不存在，则新增
            product_image = ProductImage(
                product_id= product_id,
                asset_id = int(asset_id),
                sort_order= counter
            )
            db.session.add(product_image)

        counter += 1
