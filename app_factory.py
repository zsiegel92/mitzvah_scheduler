from flask import Flask
from database import db
import os



# gunicorn_error_logger = logging.getLogger('gunicorn.error')


def create_app(name=__name__):
    app = Flask(__name__,static_folder='mitzvah/static')
    app.config.from_object(os.environ['APP_SETTINGS'])
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    # bcrypt.init_app(app)
    # login_manager.init_app(app)

    return app

