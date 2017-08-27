from . import auth
from .forms import RegForm
from flask import request,render_template,url_for,redirect

@auth.route('/register', methods=['GET','POST'])
def register():
    form=RegForm()

    if request.method == "POST" and form.validate():
        return "Sucess"
    return render_template('Landing/Regform.html',form=form)
