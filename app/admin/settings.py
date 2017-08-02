# -*- coding: utf-8 -*-
from flask import render_template, redirect, url_for, flash, request, abort, current_app
from flask_login import login_required, current_user
from flask_babelex import gettext

from .forms import LanguageForm, EditLanguageForm, CountryForm, EditCountryForm, CurrencyForm, SiteForm
from app.models import Language, Country, Currency, LengthClass, LengthClassDescription, WeightClass, \
    WeightClassDescription, Site, Counter, User

from .. import db
from ..utils import Master, gen_serial_no
from . import admin


@admin.route('/site', methods=['GET', 'POST'])
@login_required
def site():
    form = SiteForm()
    site = Site.query.filter_by(master_uid=Master.master_uid()).first()
    if form.validate_on_submit():
        if site is None:
            # 新增店铺
            new_site = Site(
                master_uid = Master.master_uid(),
                serial_no = Site.make_unique_serial_no(),
                name = form.name.data,
                domain = form.domain.data,
                description = form.description.data
            )
            db.session.add(new_site)
            site_id = new_site.id
        else:
            site.name = form.name.data
            site.domain = form.domain.data
            site.description = form.description.data

            site_id = site.id

        # 更新配置状态
        master = User.query.get_or_404(Master.master_uid())
        master.mark_as_setting(site_id)

        db.session.commit()

        flash(gettext('Update site info is ok!'), 'success')

        return redirect(url_for('admin.index'))
    else:
        current_app.logger.debug('Update site is fail: %s!' % form.errors)

    # 支持的语言
    languages = Language.query.filter_by(status=1).all()
    # 支持的货币
    currencies = Currency.query.order_by(Currency.id.asc()).all()

    # 初始化数据
    if site is not None:
        form.name.data = site.name
        form.copyright.data = site.copyright
        form.description.data = site.description
        form.status.data = site.status

    return render_template('admin/stores/settings.html',
                           form=form,
                           site=site,
                           languages=languages,
                           currencies=currencies)

@admin.route('/languages')
@admin.route('/languages/<int:page>')
def show_languages(page=1):
    per_page = request.args.get('per_page', 10, type=int)
    status = request.args.get('status', 0, type=int)

    if not status:
        query = Language.query
    else:
        query = Language.query.filter_by(status=status)

    paginated_languages = query.order_by(Language.id.asc()).paginate(page, per_page)

    if paginated_languages:
        paginated_languages.offset_start = 1 if page == 1 else (page - 1) * per_page
        paginated_languages.offset_end = paginated_languages.offset_start + len(paginated_languages.items) - 1

    return render_template('admin/languages/show_list.html',
                           paginated_languages=paginated_languages)


@admin.route('/languages/create', methods=['GET', 'POST'])
def create_language():
    form = LanguageForm()
    if form.validate_on_submit():
        language = Language(
            name=form.name.data,
            code=form.code.data,
            locale=form.locale.data,
            icon_id=form.icon.data,
            directory=form.directory.data,
            sort_order=form.sort_order.data,
            status=form.status.data
        )
        db.session.add(language)

        flash('Add language is ok!', 'success')

        return redirect(url_for('.show_languages'))

    mode = 'create'
    language = None
    return render_template('admin/languages/create_and_edit.html',
                           form=form,
                           mode=mode,
                           language=language
                        )


@admin.route('/languages/<int:id>/edit', methods=['GET', 'POST'])
def edit_language(id):
    language = Language.query.get_or_404(id)
    form = EditLanguageForm(language)
    if form.validate_on_submit():
        language.name = form.name.data
        language.code = form.code.data,
        language.locale = form.locale.data,
        language.icon_id = form.icon.data,
        language.directory = form.directory.data,
        language.sort_order = form.sort_order.data,
        language.status = form.status.data

        db.session.commit()

        flash('Edit language is ok!', 'success')

        return redirect(url_for('.show_languages'))

    mode = 'edit'
    return render_template('admin/languages/create_and_edit.html',
                           form=form,
                           language=language,
                           mode=mode)


@admin.route('/languages/delete', methods=['POST'])
def delete_language():
    selected_ids = request.form.getlist('selected[]')
    if not selected_ids or selected_ids is None:
        flash('Delete language is null!', 'danger')
        abort(404)

    try:
        for id in selected_ids:
            lang = Language.query.get_or_404(int(id))
            db.session.delete(lang)
            db.session.commit()
    except:
        pass

    flash('Delete language is ok!', 'success')

    return redirect(url_for('.show_languages'))


'''Settings currency'''

@admin.route('/currencies')
@admin.route('/currencies/<int:page>')
def show_currencies(page=1):
    per_page = request.args.get('per_page', 10, type=int)

    paginated_currencies = Currency.query.order_by(Currency.id.asc()).paginate(page, per_page)

    if paginated_currencies:
        paginated_currencies.offset_start = 1 if page == 1 else (page - 1) * per_page
        paginated_currencies.offset_end = paginated_currencies.offset_start + len(paginated_currencies.items) - 1

    return render_template('admin/currency/show_list.html',
                           paginated_currencies=paginated_currencies)


@admin.route('/currencies/create', methods=['GET', 'POST'])
def create_currency():
    form = CurrencyForm()
    if form.validate_on_submit():
        currency = Currency(
            title=form.title.data,
            code=form.code.data,
            symbol_left=form.symbol_left.data,
            symbol_right=form.symbol_right.data,
            decimal_place=form.decimal_place.data,
            value=form.value.data,
            status=form.status.data
        )
        db.session.add(currency)

        flash('Add currency is ok!', 'success')
        return redirect(url_for('.show_currencies'))

    mode = 'create'
    return render_template('admin/currency/create_and_edit.html',
                           mode=mode,
                           form=form
                           )


@admin.route('/currencies/<int:id>/edit', methods=['GET', 'POST'])
def edit_currency(id):
    currency = Currency.query.get_or_404(id)
    form = CurrencyForm()
    if form.validate_on_submit():
        form.populate_obj(currency)
        db.session.commit()

        flash('Edit currency is ok!', 'success')
        return redirect(url_for('.show_currencies'))

    mode = 'edit'
    form.title.data = currency.title
    form.code.data = currency.code
    form.symbol_left.data = currency.symbol_left
    form.symbol_right.data = currency.symbol_right
    form.decimal_place.data = currency.decimal_place
    form.value.data = currency.value
    form.status.data = currency.status

    return render_template('admin/currency/create_and_edit.html',
                           mode=mode,
                           form=form
                           )


@admin.route('/currencies/delete', methods=['POST'])
def delete_currency():
    selected_ids = request.form.getlist('selected[]')
    if not selected_ids or selected_ids is None:
        flash('Delete currency is null!', 'danger')
        abort(404)

    try:
        for id in selected_ids:
            currency = Currency.query.get_or_404(int(id))
            db.session.delete(currency)
        db.session.commit()

        flash('Delete currency is ok!', 'success')
    except:
        db.session.rollback()
        flash('Delete currency is error!!!', 'danger')

    return redirect(url_for('.show_currencies'))




@admin.route('/countries')
@admin.route('/countries/<int:page>')
def show_countries(page=1):
    per_page = request.args.get('per_page', 10, type=int)

    paginated_countries = Country.query.order_by(Country.id.asc()).paginate(page, per_page)

    if paginated_countries:
        paginated_countries.offset_start = 1 if page == 1 else (page - 1) * per_page
        paginated_countries.offset_end = paginated_countries.offset_start + len(paginated_countries.items) - 1

    return render_template('admin/country/show_countries.html',
                           paginated_countries=paginated_countries)


@admin.route('/countries/create', methods=['GET', 'POST'])
def create_country():
    form = CountryForm()
    if form.validate_on_submit():
        country = Country(
            name=form.name.data,
            iso_code_2=form.iso_code_2.data,
            iso_code_3=form.iso_code_3.data,
            address_format=form.address_format.data,
            postcode_required=form.postcode_required.data,
            status=form.status.data
        )
        try:
            db.session.add(country)
            db.session.commit()
        except:
            db.session.rollback()
            flash('Add Country is fail!' , 'danger')
            return redirect(url_for('.create_country'))

        flash('Add country is ok!', 'success')

        return redirect(url_for('.show_countries'))

    mode = 'create'
    return render_template('admin/country/create_and_edit.html',
                           form=form,
                           mode=mode
                           )


@admin.route('/countries/<int:id>/edit', methods=['GET', 'POST'])
def edit_country(id):
    country = Country.query.get_or_404(id)
    form = EditCountryForm(country)
    if form.validate_on_submit():
        form.populate_obj(country)
        db.session.commit()

        flash('Edit country is ok!', 'success')
        return redirect(url_for('.show_countries'))

    mode = 'edit'
    # populate data for form
    form.name.data = country.name
    form.iso_code_2.data = country.iso_code_2
    form.iso_code_3.data = country.iso_code_3
    form.address_format.data = country.address_format
    form.postcode_required.data = country.postcode_required
    form.status.data = country.status

    return render_template('admin/country/create_and_edit.html',
                           form=form,
                           country=country,
                           mode=mode)


@admin.route('/countries/delete', methods=['GET', 'POST'])
def delete_country():
    selected_ids = request.form.getlist('selected[]')
    if not selected_ids or selected_ids is None:
        flash('Delete country is null!', 'danger')
        abort(404)

    try:
        for id in selected_ids:
            country = Country.query.get_or_404(int(id))
            db.session.delete(country)
            db.session.commit()

        flash('Delete country is ok!', 'success')
    except:
        db.session.rollback()
        flash('Delete country is error!!!', 'danger')

    return redirect(url_for('.show_countries'))


@admin.route('/zones')
@admin.route('/zones/<int:page>')
def show_zones(page=1):
    pass


@admin.route('/geo_zones')
@admin.route('/geo_zones/<int:page>')
def show_geo_zones(page=1):
    pass


@admin.route('/lengths')
@admin.route('/lengths/<int:page>')
def show_lengths(page=1):
    per_page = request.args.get('per_page', 10, type=int)

    paginated_lengths = LengthClass.query.order_by(LengthClass.id.asc()).paginate(page, per_page)

    if paginated_lengths:
        paginated_lengths.offset_start = 1 if page == 1 else (page - 1) * per_page
        paginated_lengths.offset_end = paginated_lengths.offset_start + len(paginated_lengths.items) - 1

    return render_template('admin/lengths/show_list.html',
                           paginated_lengths=paginated_lengths)


@admin.route('/lengths/create', methods=['GET', 'POST'])
def create_length():
    languages = Language.query.filter_by(status=1).all()
    if request.method == 'POST':
        value = request.form.get('value')
        if value is None or value == '':
            flash('Value cant empty!', 'danger')
            return redirect(url_for('.create_length'))

        length_class_description = []
        for lang in languages:
            length = {}
            length['language_id'] = lang.id
            length['title'] = request.form.get('length_class_description[%d][title]' % lang.id)
            length['unit'] = request.form.get('length_class_description[%d][unit]' % lang.id)
            length_class_description.append(length)

        try:
            length_class = LengthClass(value=value)
            db.session.add(length_class)

            for length_dict in length_class_description:
                length_description = LengthClassDescription(length_class=length_class, **length_dict)
                db.session.add(length_description)

            db.session.commit()
        except:
            db.session.rollback()
            flash('Add length class is fail!', 'danger')
            return redirect(url_for('.create_length'))

        flash('Add length class is ok!', 'success')

        return redirect(url_for('.show_lengths'))

    mode = 'create'
    length_class = None
    language_descriptions = None
    return render_template('admin/lengths/create_and_edit.html',
                           mode=mode,
                           languages=languages,
                           length_class=length_class,
                           language_descriptions=language_descriptions
                           )


@admin.route('/lengths/<int:id>/edit', methods=['GET', 'POST'])
def edit_length(id):
    length_class = LengthClass.query.get_or_404(id)
    languages = Language.query.filter_by(status=1).all()

    if request.method == 'POST':
        value = request.form.get('value')
        if value is None or value == '':
            flash('Value cant empty!', 'danger')
            return redirect(url_for('.create_length'))

        try:
            length_class.value = value

            for lang_version in length_class.length_descriptions:
                lang_id = lang_version.language_id
                lang_version.title = request.form.get('length_class_description[%d][title]' % lang_id)
                lang_version.unit = request.form.get('length_class_description[%d][unit]' % lang_id)

            db.session.commit()
        except TypeError as e:
            db.session.rollback()
            flash('Add length class is fail [%s]!' % e.args, 'danger')
            return redirect(url_for('.edit_length', id=id))

        flash('Add length class is ok!', 'success')
        return redirect(url_for('.show_lengths'))

    mode = 'edit'
    return render_template('admin/lengths/create_and_edit.html',
                           mode=mode,
                           languages=languages,
                           length_class=length_class,
                           language_descriptions=length_class.language_descriptions()
                           )

@admin.route('/lengths/delete', methods=['POST'])
def delete_length():
    selected_ids = request.form.getlist('selected[]')
    if not selected_ids or selected_ids is None:
        flash('Delete length class is null!', 'danger')
        abort(404)

    try:
        for id in selected_ids:
            length_class = LengthClass.query.get_or_404(int(id))
            db.session.delete(length_class)
        db.session.commit()

        flash('Delete length class is ok!', 'success')
    except:
        db.session.rollback()
        flash('Delete length class is error!!!', 'danger')

    return redirect(url_for('.show_lengths'))


@admin.route('/weights')
@admin.route('/weights/<int:page>')
def show_weights(page=1):
    per_page = request.args.get('per_page', 10, type=int)

    paginated_weights = WeightClass.query.order_by(WeightClass.id.asc()).paginate(page, per_page)

    if paginated_weights:
        paginated_weights.offset_start = 1 if page == 1 else (page - 1) * per_page
        paginated_weights.offset_end = paginated_weights.offset_start + len(paginated_weights.items) - 1

    return render_template('admin/weights/show_list.html',
                           paginated_weights=paginated_weights)



@admin.route('/weights/create', methods=['GET', 'POST'])
def create_weight():
    languages = Language.query.filter_by(status=1).all()
    if request.method == 'POST':
        value = request.form.get('value')
        if value is None or value == '':
            flash('Value cant empty!', 'danger')
            return redirect(url_for('.create_weight'))

        weight_class_description = []
        for lang in languages:
            length = {}
            length['language_id'] = lang.id
            length['title'] = request.form.get('weight_class_description[%d][title]' % lang.id)
            length['unit'] = request.form.get('weight_class_description[%d][unit]' % lang.id)
            weight_class_description.append(length)

        try:
            weight_class = WeightClass(value=value)
            db.session.add(weight_class)

            for weight_dict in weight_class_description:
                weight_description = WeightClassDescription(weight_class=weight_class, **weight_dict)
                db.session.add(weight_description)

            db.session.commit()
        except:
            db.session.rollback()
            flash('Add weight class is fail!', 'danger')
            return redirect(url_for('.create_weight'))

        flash('Add weight class is ok!', 'success')

        return redirect(url_for('.show_weights'))

    mode = 'create'
    weight_class = None
    language_descriptions = None
    return render_template('admin/weights/create_and_edit.html',
                           mode=mode,
                           languages=languages,
                           weight_class=weight_class,
                           language_descriptions=language_descriptions
                           )

@admin.route('/weights/<int:id>/edit', methods=['GET', 'POST'])
def edit_weight(id):
    weight_class = WeightClass.query.get_or_404(id)
    languages = Language.query.filter_by(status=1).all()

    if request.method == 'POST':
        value = request.form.get('value')
        if value is None or value == '':
            flash('Value cant empty!', 'danger')
            return redirect(url_for('.create_weight'))

        try:
            weight_class.value = value

            for lang_version in weight_class.weight_descriptions:
                lang_id = lang_version.language_id
                lang_version.title = request.form.get('weight_class_description[%d][title]' % lang_id)
                lang_version.unit = request.form.get('weight_class_description[%d][unit]' % lang_id)

            db.session.commit()
        except TypeError as e:
            db.session.rollback()
            flash('Add weight class is fail [%s]!' % e.args, 'danger')
            return redirect(url_for('.edit_weight', id=id))

        flash('Add weight class is ok!', 'success')
        return redirect(url_for('.show_weights'))

    mode = 'edit'
    return render_template('admin/weights/create_and_edit.html',
                           mode=mode,
                           languages=languages,
                           weight_class=weight_class,
                           language_descriptions=weight_class.language_descriptions()
                           )


@admin.route('/weights/delete', methods=['POST'])
def delete_weight():
    selected_ids = request.form.getlist('selected[]')
    if not selected_ids or selected_ids is None:
        flash('Delete weight class is null!', 'danger')
        abort(404)

    try:
        for id in selected_ids:
            weight_class = WeightClass.query.get_or_404(int(id))
            db.session.delete(weight_class)

        db.session.commit()

        flash('Delete weight class is ok!', 'success')
    except:
        db.session.rollback()
        flash('Delete weight class is error!!!', 'danger')

    return redirect(url_for('.show_weights'))