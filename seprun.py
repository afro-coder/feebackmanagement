import os
from FMSapp import create_app,db
from flask_migrate import Migrate
from FMSapp.models import users
from flask.cli import FlaskGroup

app = create_app(os.environ.get('DEV', 'development'))
migrate=Migrate(app,db)

@app.shell_context_processor
def make_context():
    return dict(app=app,db=db,users=users)

@app.cli.command()
def initdb():
    db.create_all()
    #with app.app_context():

@app.cli.command(help="debug ")
def debug():
    print("done")
    os.environ['FLASK_DEBUG'] = '1'


#if __name__ == '__main__':
#    cli()
# @app.cli.command
# @click.option('--db')
# def dbm(db)
