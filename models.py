from dateutil.parser import parse
from datetime import date
import json

from database import db


class Student(db.Model):
	__tablename__ = "students"
	id = db.Column(db.Integer(),primary_key=True)
	school = db.relationship("School",back_populates ="students",uselist=False)
	hebSchool = db.relationship("HebSchool",back_populates ="students",uselist=False) #way to make non-list?
	dob  = db.Column(db.DateTime())
	email=db.Column(db.String())
	childName=db.Column(db.String())
	ranking_main=db.Column(db.Integer())
	ranking_familyMinyan=db.Column(db.Integer())
	ranking_torahInTheRound=db.Column(db.Integer())
	atVenue = db.Column(db.Boolean())
	accommodation_other = db.Column(db.Text)
	twin = db.Column(db.Boolean())
	school_id = db.Column(db.Integer,db.ForeignKey('schools.id'))
	hebSchool_id = db.Column(db.Integer,db.ForeignKey('hebschools.id'))
	nonDates = db.relationship("NonDate",back_populates="student",uselist=True)
	birthdayDD =db.Column(db.Text)
	bmDD = db.Column(db.Text)

	def __init__(self,rankings,schoolId,school,hebSchoolId,hebSchool,DOB,DOBdd,BMdd,nonDates=[],accommodation=False, **kwargs):
		print("KWARGS ARE:")
		print(kwargs)

		super(Student, self).__init__(**kwargs)
		self.ranking_main=rankings[0]['value']
		self.ranking_familyMinyan=rankings[1]['value']
		self.ranking_torahInTheRound=rankings[2]['value']

		self.dob=parse(DOB).date()

		self.birthdayDD = json.dumps(DOBdd)
		self.bmDD = json.dumps(BMdd)


		self.nonDates=[]
		# for nonDate in nonDates:
		# 	greg = nonDate['greg']
		# 	gdate = date(greg['year'],greg['month'],greg['day'])
		# 	nd = NonDate(greg=gdate)
		# 	nd.student_id = self.id
		# 	self.nonDates.append(nd)
		# 	nd.student=self
		# 	print("APPENDING non-DATE")
		# 	print(f"My id is: {self.id}")
		# 	db.session.add(nd)
		# gregs=[nonDate['greg'] for nonDate in nonDates]
		# self.nonDates=NonDate.cls_construct(gregs)


class NonDate(db.Model):
	__tablename__="nondates"
	id = db.Column(db.Integer, primary_key=True,autoincrement=True)
	greg = db.Column(db.Date())
	student = db.relationship("Student",uselist=False)
	student_id = db.Column(db.Integer,db.ForeignKey('students.id'))
	# parent_id = db.Column(db.Integer,db.ForeignKey("nondates.id"),nullable=True)
	# parent = db.relationship("NonDate",remote_side=[id])

	# def __init__(self,greg):
	# 	self.greg = date(greg['year'],greg['month'],greg['day'])
	# @classmethod
	# def cls_construct(cls,gregs):
	# 	return [cls(greg) for greg in gregs]
class School(db.Model):
	__tablename__ = 'schools'

	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String())
	students = db.relationship("Student",uselist=True,back_populates="school")

	def __repr__(self):
		return '<School {}, {}>'.format(self.id, self.name)

	def to_dict(self):
		return {'id':self.id,'name':self.name}


class HebSchool(db.Model):
	__tablename__ = 'hebschools'

	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String())
	students = db.relationship("Student",back_populates="hebSchool")


	def __repr__(self):
		return '<HebSchool {}, {}>'.format(self.id, self.name)

	def to_dict(self):
		return {'id':self.id,'name':self.name}
