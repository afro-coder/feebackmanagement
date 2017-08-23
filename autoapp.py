from FMSapp import create_app
from config import config
app = create_app('development')
app.run()
