from database import db



class School(db.Model):
	__tablename__ = 'schools'

	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String())

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

	def __init__(self, name):
		self.name = name

	def __repr__(self):
		return '<HebSchool {}, {}>'.format(self.id, self.name)

	def to_dict(self):
		return {'id':self.id,'name':self.name}
