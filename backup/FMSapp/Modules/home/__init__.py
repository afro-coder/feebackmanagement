from flask import Blueprint, render_template, request,current_app,redirect,url_for

from flask_login import current_user
viewhome = Blueprint('viewhome', __name__)
from flask_login import login_required
from ..utils import requires_roles

@viewhome.route('/roletest', methods=['GET'])
@login_required
@requires_roles('teacher')
def role_test():
    return render_template('Landing/index.html')


@viewhome.route('/index', methods=['GET'])
@viewhome.route('/',methods=['GET'])
def home():
    if request.method=='GET':
        if current_user.is_admin() and current_user.is_authenticated:
            return redirect(url_for('admin.index'))
        else:
            return render_template('Landing/index.html')
