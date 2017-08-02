# -*- coding: utf-8 -*-
import os, time, hashlib
from datetime import datetime
from flask import current_app, g, render_template, redirect, url_for, flash, request, send_from_directory, jsonify
from werkzeug import secure_filename
from flask_login import login_required
from PIL import Image
from app.models import Asset, Directory
from app import db, uploader
from .forms import UploadForm
from . import admin

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in current_app.config['ALLOWED_EXTENSIONS']


@admin.route('/uploads')
@admin.route('/uploads/<int:page>')
def show_uploads(page=1):
    per_page = request.args.get('per_page', 10, type=int)
    status = request.args.get('status', 0, type=int)

    if not status:
        query = Asset.query
    else:
        query = Asset.query.filter_by(status=status)

    paginated_brands = query.order_by(Asset.created_at.desc()).paginate(page, per_page)

    if paginated_brands:
        paginated_brands.offset_start = 1 if page == 1 else (page - 1) * per_page
        paginated_brands.offset_end = paginated_brands.offset_start + len(paginated_brands.items) - 1

    return render_template('admin/uploads/show_list.html',
                           paginated_brands=paginated_brands)


@admin.route('/uploads/new', methods=['GET', 'POST'])
def new_upload():
    mode = 'create'
    form = UploadForm()

    if request.method == 'POST':
        saved_asset_ids = []
        sub_folder = str(time.strftime('%y%m%d'))
        #for key, file in request.files.iteritems():
        for f in request.files.getlist('file'):
            upload_name = f.filename
            # start to save
            name_prefix = 'admin' + str(time.time())
            name_prefix = hashlib.md5(name_prefix.encode('utf-8')).hexdigest()[:15]

            filename = uploader.save(f, folder=sub_folder, name=name_prefix+'.')

            storage_filepath = uploader.path(filename)

            current_app.logger.warning('upload filename: %s, filepath: %s' % (filename, storage_filepath))

            # get info of upload image
            im = Image.open(storage_filepath)

            size = os.path.getsize(storage_filepath)/1024 # k

            new_asset = Asset(filepath=filename, filename=upload_name, width=im.width, height=im.height, size=size)
            db.session.add(new_asset)
            db.session.commit()

            saved_asset_ids.append(new_asset.id)

        return jsonify({
            'status': 200,
            'ids': saved_asset_ids
        })

    return render_template('admin/uploads/new_upload.html',
                           form=form,
                           mode=mode)

@admin.route('/uploads/find_asset/<int:id>')
def find_asset(id):
    asset = Asset.query.get_or_404(id)

    return jsonify(asset.to_json())