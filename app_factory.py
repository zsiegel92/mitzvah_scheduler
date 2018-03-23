from flask import Flask
import os
from dateutil.parser import parse

from database import db




# gunicorn_error_logger = logging.getLogger('gunicorn.error')


def _jinja2_filter_datetime(date):
    if not hasattr(date,'strftime'):
        date = parse(date).date()
    return date.strftime('%m/%d/%Y')


def _jinja2_filter_ranking(rank):
    ranks = {-1: "'Would not prefer'", 0: "'No preference'", 1: "'Prefer'"}
    return ranks.get(rank)

def indexer(app):
    def index(path=''):
        return app.send_static_file('index.html')
    return index

def create_app(name=__name__):
    app = Flask(__name__,static_folder='mitzvah/static')
    app.config.from_object(os.environ['APP_SETTINGS'])
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    filters = {'ranking':_jinja2_filter_ranking,'date':_jinja2_filter_datetime}
    for key,filter in filters.items():
        app.jinja_env.filters[key] = filter
    app.add_url_rule('/', 'index', indexer(app))
    app.add_url_rule('/<path:path>', 'index_path', indexer(app))
    return app

