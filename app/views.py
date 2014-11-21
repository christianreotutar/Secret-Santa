from flask import render_template, flash, redirect, url_for, send_from_directory
from app import app, db
from .forms import LoginForm
from models import User
from werkzeug import secure_filename
from sqlalchemy import exc
import os

@app.route("/", methods=['GET', 'POST'])
@app.route("/index", methods=['GET', 'POST'])
def index():
    user = {'nickname': 'Caroline'}
    forms = [
        {   'name': 'name',
            'type': 'text'  },
        {   'name': 'email',
            'type': 'text'  },
        {   'name': 'wishlist',
            'type': 'file'  }
    ]
    form = LoginForm()

    if form.validate_on_submit():
        in_name = form.name.data
        in_email = str(form.email.data)
        in_wishlist = secure_filename(form.wishlist.data.filename)
        if allowed_file(in_wishlist):
            form.wishlist.data.save(os.path.join( \
                'app/' + app.config['UPLOAD_FOLDER'], in_wishlist))
        else:
            flash('Not a supported file type. Try txt/pdf/doc/docx.')
            return redirect(url_for('index'))
        flash('Login requested for name="%s", email="%s", wish="%s"' % \
               (in_name, in_email, in_wishlist))

        try:
            newuser = User(name = in_name, email = in_email, \
                        wishlist = in_wishlist)
            db.session.add(newuser)
            db.session.commit()
        except exc.IntegrityError:
            db.session.rollback()
            flash('File ' + in_wishlist + ' already exists.')
            return redirect(url_for('index'))
        return redirect(url_for('uploaded_file', filename=in_wishlist))
 
    return render_template('index.html', title='Secret Santa', \
            user=user, form=form)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.static_folder, filename)

def allowed_file(filename):
    return '.' in filename and \
            filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXT']
