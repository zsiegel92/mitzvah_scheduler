from flask import Flask
import os
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from app import app, db
migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

@manager.command
def populate():
	from models import School
	schools = School.query.all()
	try:
		max_id = max([school.id for school in schools])
	except:
		max_id="00"
	school = School(name='school_'+str(max_id))
	db.session.add(school)
	db.session.commit()


if __name__ == '__main__':
	manager.run()
