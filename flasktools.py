import click
from FMSapp import create_app,db
from flask.cli import FlaskGroup
import os
from FMSapp.models import users

app=create_app('development')

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


@cli.command()
@click.option('--dbin')
def initdb():
    """Initialize the database."""
    click.echo("done")
    db.create_all()



if __name__ == '__main__':
    cli()
