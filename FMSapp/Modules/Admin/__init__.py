from ..admin_blueprint import AdminBlueprint
from flask_admin import AdminIndexView



admin=AdminBlueprint('admin',__name__,
#url_prefix='/admin1',
static_folder='static',
static_url_path='/static/admin',
template_folder='templates',base_template='admin/admin_base.html')



from . import views
