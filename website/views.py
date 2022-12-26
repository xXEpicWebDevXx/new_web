from flask import Blueprint, render_template,request, redirect, url_for
from flask_login import current_user, login_required
from . import db
from .models import *
from os import path
from werkzeug.utils import secure_filename


views = Blueprint('views', __name__)

@views.route('/')
#@login_required
def home():
    return render_template("homePage.html",user = current_user,imgs = Image.query.filter().all(),users = User.query.filter().all())



UPLOAD_FOLDER = 'website\static\images'


@views.route('/FTP',methods=['GET','POST'])
@login_required
def FTP():
    if request.method == 'POST':
        if 'file' not in request.files:
            print("Missing File")
        file = request.files['file']
        new_file = Image(user_id = current_user.id,suffix = "." + secure_filename(file.filename).split('.')[-1])
        db.session.add(new_file)
        db.session.commit()
        filename = str(new_file.id) +"." +secure_filename(file.filename).split('.')[-1]
        file.save(path.join(UPLOAD_FOLDER, filename))
    return render_template("filetransfare.html")

@views.route('/admin',methods=['GET','POST'])
@login_required
def Administration():
    if current_user.privs !=3:return redirect(url_for('views.home'))



    return render_template('admin.html',user = current_user)

@views.route('/collection',methods=['GET','POST'])
@login_required
def Collection():
    if request.method == 'POST':
        if 'file' not in request.files:
            print("Missing File")
        file = request.files['file']
        new_file = Image(user_id = current_user.id,suffix = "." + secure_filename(file.filename).split('.')[-1])
        db.session.add(new_file)
        db.session.commit()
        filename = str(new_file.id) +"." +secure_filename(file.filename).split('.')[-1]
        file.save(path.join(UPLOAD_FOLDER, filename))
    return render_template('collection.html',user = current_user)



@views.route('/deleteImage/<id>',methods=["POST"])
def DeleteImage(id):
    file = Image.query.filter(Image.id == id).first()
    from os import remove
    remove(path.join(UPLOAD_FOLDER, str(file.id) + file.suffix))
    Image.query.filter(Image.id == id).delete()            #Make more secure(not important)
    db.session.commit()
    return render_template('collection.html',user=current_user)

