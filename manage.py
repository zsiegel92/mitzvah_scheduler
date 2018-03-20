from flask import Flask
import os
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from app import app, db
from models import Student, School,HebSchool,NonDate

migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

@manager.shell
def make_shell_context():
	return dict(app=app, db=db, Student=Student,School=School,HebSchool=HebSchool,NonDate=NonDate)

@manager.command
def populate():
	# from models import School,HebSchool
	names = ['Lainer School']
	for name in names:
		school = School.query.filter_by(name=name).first()
		if school is None:
			school = School(name=name)
		db.session.add(school)
	db.session.commit()
	hNames = ["Temple Isaiah"]
	for name in hNames:
		school = HebSchool.query.filter_by(name=name).first()
		if school is None:
			school = HebSchool(name=name)
		db.session.add(school)
	db.session.commit()

@manager.command
def delete_all():
	# from models import School,Student
	for s in Student.query.all():
	 	db.session.delete(s)
	db.session.commit()

if __name__ == '__main__':
	manager.run()
