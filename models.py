from dateutil.parser import parse
from datetime import date
import json

from database import db


class Student(db.Model):
	__tablename__ = "students"
	id = db.Column(db.Integer(),primary_key=True)
	school = db.relationship("School",back_populates ="students",uselist=False)
	hebSchool = db.relationship("HebSchool",back_populates ="students",uselist=False) #way to make non-list?
	dob  = db.Column(db.Date())
	email=db.Column(db.String())
	childName=db.Column(db.String())
	ranking_main=db.Column(db.Integer())
	ranking_familyMinyan=db.Column(db.Integer())
	ranking_torahInTheRound=db.Column(db.Integer())
	atVenue = db.Column(db.Boolean())
	over200 = db.Column(db.Boolean())
	accommodation_other = db.Column(db.Text)
	twin = db.Column(db.Boolean())
	school_id = db.Column(db.Integer,db.ForeignKey('schools.id'))
	hebSchool_id = db.Column(db.Integer,db.ForeignKey('hebschools.id'))
	nonDates = db.relationship("NonDate",back_populates="student",uselist=True)
	birthdayDD =db.Column(db.Text)
	bmDD = db.Column(db.Text)

	def __init__(self,rankings,schoolId,school,hebSchoolId,hebSchool,DOB,DOBdd,BMdd,nonDates=[],accommodation=False, **kwargs):

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
	def approx_bm_dd_str(self):
		BMdd=json.loads(self.bmDD)
		return parse(BMdd['hgregorian']).strftime('%m/%d/%Y') +  " (" + BMdd['hdate_str'] + "/" + BMdd['hdate_str_heb'] + ")"
	def birthday_dd_str(self):
		DOBdd=json.loads(self.birthdayDD)
		return self.dob.strftime('%m/%d/%Y') + " (" + DOBdd['hdate_str'] + "/" + DOBdd['hdate_str_heb'] + ")"
	def non_date_string(self):
		nds = [nd.greg.strftime('%m/%d/%Y') for nd in self.nonDates]
		return ", ".join(nds)

	def to_dict(self):
		nds=[{'hgregorian':nd.greg,'hdate_str':nd.hdate_str,'hdate_str_heb':nd.hdate_str_heb} for nd in self.nonDates]
		d = {'email': self.email,
		'childName':self.childName,
		'school':self.school.name,
		'schoolId':self.school.id,
		'hebSchool':self.hebSchool.name,
		'hebSchoolId':self.hebSchool.id,
		'DOB':self.dob,
		'DOBdd':json.loads(self.birthdayDD),
		'BMdd':json.loads(self.bmDD),
		'rankings':[{
		      'name': "Main Sanctuary",
		      'value': self.ranking_main
		    },
		    {
		      'name': "Family Minyan",
		      'value': self.ranking_familyMinyan
		    },
		    {
		      'name': "Torah In The Round",
		      'value': self.ranking_torahInTheRound
		    }],
		 'atVenue':self.atVenue,
		 'over200':self.over200,
		 'nonDates':nds,
		 'accommodation':self.accommodation_other != '',
		 'accommodation_other':self.accommodation_other,
		 'twin':self.twin,
		}
		return d

	def to_csv_row(self):
		a_row = [self.email, self.childName, self.birthday_dd_str(), self.school.name, self.hebSchool.name, self.atVenue, self.over200, self.twin, self.accommodation_other,]

		a_row.append(self.approx_bm_dd_str())
		a_row.append("Main: {}, Family Minyan: {}, Torah in the Round: {}".format(self.ranking_main,self.ranking_familyMinyan,self.ranking_torahInTheRound))
		a_row.append(self.non_date_string())
		return a_row

class NonDate(db.Model):
	__tablename__="nondates"
	id = db.Column(db.Integer, primary_key=True,autoincrement=True)
	greg = db.Column(db.Date())
	hdate_str = db.Column(db.String())
	hdate_str_heb = db.Column(db.String())
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
