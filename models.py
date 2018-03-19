from database import db


class Student(db.Model):
	__tablename__ = "students"
	id = db.Column(db.Integer,autoincrement=True,unique=True)
	email=db.Column(db.String(),primary_key=True)
	childName=db.Column(db.String(),primary_key=True)
	school = db.relationship("School",back_populates ="students",uselist=False)
	hebSchool = db.relationship("HebSchool",back_populates ="students",uselist=False) #way to make non-list?
	dob  = db.Column(db.DateTime())
	ranking_main=db.Column(db.Integer())
	ranking_familyMinyan=db.Column(db.Integer())
	ranking_torahInTheRound=db.Column(db.Integer())
	atVenue = db.Column(db.Boolean())
	nonDates = db.relationship("nonDates",back_populates="student",uselist=True)
	accommodation = db.Column(db.Text)
	twin = db.Column(db.Boolean())
	school_id = db.Column(db.Integer,db.ForeignKey('schools.id'))
	hebSchool_id = db.Column(db.Integer,db.ForeignKey('hebschools.id'))


class nonDates(db.Model):
	id = db.Column(db.Integer, primary_key=True,autoincrement=True)
	date = db.Column(db.DateTime())
	student = db.relationship("Student",back_populates="nonDates",uselist=False)
	student_id = db.Column(db.Integer,db.ForeignKey('students.id'))

class School(db.Model):
	__tablename__ = 'schools'

	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String())
	students = db.relationship("Student",uselist=True,back_populates="school")
	def __init__(self, name):
		self.name = name

	def __repr__(self):
		return '<School {}, {}>'.format(self.id, self.name)

	def to_dict(self):
		return {'id':self.id,'name':self.name}


class HebSchool(db.Model):
	__tablename__ = 'hebschools'

	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String())
	students = db.relationship("Student",back_populates="hebSchool")

	def __init__(self, name):
		self.name = name

	def __repr__(self):
		return '<HebSchool {}, {}>'.format(self.id, self.name)

	def to_dict(self):
		return {'id':self.id,'name':self.name}
