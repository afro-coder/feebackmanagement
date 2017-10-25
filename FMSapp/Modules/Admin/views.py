from . import admin
from flask import request,render_template,url_for,redirect,flash

@admin.route('/',methods=['GET','POST'])
def admin_default():
    return render_template("admin/base.html")
