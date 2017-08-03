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


@admin.route('/languages')
@admin.route('/languages/<int:page>')
@login_required
def show_languages(page=1):
    per_page = request.args.get('per_page', 10, type=int)
    status = request.args.get('status', 0, type=int)

    if not status:
        builder = Language.query
    else:
        builder = Language.query.filter_by(status=status)

    paginated_languages = builder.order_by(Language.id.asc()).paginate(page, per_page)

    if paginated_languages:
        paginated_languages.offset_start = 1 if page == 1 else (page - 1) * per_page
        paginated_languages.offset_end = paginated_languages.offset_start + len(paginated_languages.items) - 1

    return render_template('admin/languages/show_list.html',
                           paginated_languages=paginated_languages)


@admin.route('/languages/create', methods=['GET', 'POST'])
@login_required
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

        flash(gettext('Add language is ok!'), 'success')

        return redirect(url_for('.show_languages'))

    mode = 'create'
    return render_template('admin/languages/create_and_edit.html',
                           form=form,
                           mode=mode)


@admin.route('/languages/<int:id>/edit', methods=['GET', 'POST'])
@login_required
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

        flash(gettext('Edit language is ok!'), 'success')

        return redirect(url_for('.show_languages'))

    mode = 'edit'
    form.name.data = language.name
    form.code.data = language.code
    form.locale.data = language.locale
    form.icon.data = language.icon_id
    form.directory.data = language.directory
    form.sort_order.data = language.sort_order
    form.status.data = language.status

    return render_template('admin/languages/create_and_edit.html',
                           form=form,
                           language=language,
                           mode=mode)


@admin.route('/languages/delete', methods=['POST'])
@login_required
def delete_language():
    selected_ids = request.form.getlist('selected[]')
    if not selected_ids or selected_ids is None:
        flash(gettext('Delete language is null!'), 'danger')
        abort(404)

    try:
        for id in selected_ids:
            lang = Language.query.get_or_404(int(id))
            db.session.delete(lang)
        db.session.commit()
    except:
        pass

    flash(gettext('Delete language is ok!'), 'success')

    return redirect(url_for('.show_languages'))


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