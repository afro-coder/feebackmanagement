import os
from FMSapp import create_app,db
from FMSapp.models.users import User
from config import config
from flask_script import Manager,Shell
import click
from flask_migrate import Migrate,MigrateCommand
app = create_app(os.getenv('dev') or 'development')

manager=Manager(app)
migrate=Migrate(app,db)
@app.shell_context_processor
def make_shell_context():
    return dict(app=app,db=db)

manager.add_command("shell",Shell(make_context=make_shell_context()))
manager.add_command("db",MigrateCommand)

#@app.cli.command()
#@click.option()

if __name__ == '__main__':
    manager.run()
