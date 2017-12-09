from flask import Blueprint, render_template, request,current_app,redirect

from flask_login import current_user
viewhome = Blueprint('viewhome', __name__)




@viewhome.route('/index', methods=['GET'])
@viewhome.route('/',methods=['GET'])
def home():

    return render_template('Landing/index.html')
