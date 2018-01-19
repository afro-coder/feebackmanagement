from ..admin_blueprint import AdminBlueprint


#This generates a blueprint not an admin view

admin=AdminBlueprint('admin_user',__name__,
#url_prefix='/admin1',
static_folder='static',
static_url_path='/static',
template_folder='templates',base_template='admin/admin_base.html')



from . import views
