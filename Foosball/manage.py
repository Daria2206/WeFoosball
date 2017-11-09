import os

from app import create_app, db
from app.models import Team, User
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)

def make_shell_context():
    return dict(app=app, db=db, User=User, Team=Team)
manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    # This option is enabled for testing only.
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1' 
    manager.run()
