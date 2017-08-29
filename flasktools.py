import click
from FMSapp import create_app,db
from flask.cli import FlaskGroup
import os
from FMSapp.models import users
from flask_migrate import Migrate,MigrateCommand
app=create_app('development')
migrate=Migrate(app,db)

def create_cli_app(info):
    return app

@app.shell_context_processor
def make_context():
    return dict(app=app,db=db,users=users)


@click.group(cls=FlaskGroup, create_app=create_cli_app)
@click.option('--debug', is_flag=True, default=False)
def cli(debug):
    if debug:
        os.environ['FLASK_DEBUG'] = '1'


@app.cli.command()
def initdb():
    """Initialize the database."""
    click.echo("done")
    db.create_all()
@app.cli.command()
def migratedb():
    return  MigrateCommand


if __name__ == '__main__':
    cli()
