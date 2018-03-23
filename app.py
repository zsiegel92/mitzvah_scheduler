from flask import Flask,jsonify, request,make_response,render_template
from dateutil.parser import parse
from datetime import date
import io, csv
# If the mimetype is application/json, request.json will contain the parsed JSON data. Otherwise this will be None.
# otherwise use request.get_json()
from rq import Queue
from rq.job import Job

from worker import conn
from app_factory import create_app
from database import db
from models import School, HebSchool, Student,NonDate
from emailer import Emailer

q = Queue(connection=conn)
emailer=Emailer(q)

# app = Flask(__name__,static_folder='mitzvah/static')
# app.config.from_object(os.environ['APP_SETTINGS'])
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# db.init_app(app)
app = create_app(__name__)

def pre_dict(queries):
	return list(map(lambda x: x.to_dict(),queries))

# @app.route("/")
# def index():
#   # return "hello"
#   return app.send_static_file('index.html')

# Program catch-all for routes to send the static index.html file to the current app
# @app.route('/', defaults={'path': ''})
# @app.route('/<path:path>')
# def index(path=''):
# 	return app.send_static_file('index.html')

# @app.route('/<path:path>')
# def static_proxy(path):
#   # send_static_file will guess the correct MIME type
#   return app.send_static_file(path)

@app.route("/api/schools/")
def get_schools():
	schools = School.query.all()
	if len(schools)>0:
		return jsonify(pre_dict(School.query.all())),200
	else:
		return jsonify([]),200

@app.route("/api/hebschools/")
def get_hebschools():
	schools = HebSchool.query.all()
	if len(schools)>0:
		return jsonify(pre_dict(HebSchool.query.all())),200
	else:
		return jsonify([]),200




@app.route("/api/hebschools/id/<id>")
def get_hebschool(id):
	school = HebSchool.query.filter_by(id=id).first()
	if school is not None:
		return jsonify(school.to_dict()),200
	else:
		return jsonify(['no hebrew schools with that id']),200


@app.route("/api/schools/id/<id>")
def get_school(id):
	school = School.query.filter_by(id=id).first()
	if school is not None:
		return jsonify(school.to_dict()),200
	else:
		return jsonify(['no schools with that id']),200

@app.route("/api/schools/add")
def add_school():
	pass

@app.route("/api/hebschools/add")
def add_hebschool():
	pass

# @app.route('/test_email')
# def test_email():
# 	s=Student.query.filter_by(email="zsiegel92@gmail.com").first()
# 	q.enqueue_call(func=send_submission_email,kwargs = {'student_id':s.id},result_ttl=5000)
# 	return jsonify({}),200

@app.route('/api/submission',methods=['GET', 'POST'])
def submit():
	d=request.json
	for (k,v) in d.items():
		print(f'{k} : {v}')

	# s = Student(email=d['email'],childName=d['childName'], atVenue = d['atVenue'], accommodation_other = d['accommodation_other'], twin = d['twin'],rankings=d['rankings'],schoolId=d['schoolId'],hebSchoolId=d['hebSchoolId'],school=d['school'],hebSchool=d['hebSchool'],DOB=d['DOB'])
	s= Student(**d)
	db.session.add(s)
	# db.session.flush()
	# db.session.refresh(s)
	db.session.commit()
	# db.session.add(s)
	nonDates=d['nonDates']
	for nonDate in nonDates:
		greg = nonDate['greg']
		gdate = date(greg['year'],greg['month'],greg['day'])
		nd = NonDate(greg=gdate)
		nd.hdate_str=nonDate['hdate_str']
		nd.hdate_str_heb = nonDate['hdate_str_heb']
		nd.student_id = s.id
		s.nonDates.append(nd)
		nd.student=s
		print("APPENDING non-DATE")
		print(f"student_id is: {s.id}")
		db.session.add(nd)

	sch = School.query.filter_by(id=d['schoolId']).first()
	if sch is None:
		sch = School()
		sch.name = d['school']
		db.session.add(sch)
		db.session.commit()
		sch.students.append(s)
	else:
		sch.students.append(s)
	hSch = HebSchool.query.filter_by(id=d['hebSchoolId']).first()
	if hSch is None:
		hSch = HebSchool()
		hSch.name = d['hebSchool']
		db.session.add(hSch)
		hSch.students.append(s)
	else:
		hSch.students.append(s)
	db.session.commit()
	q.enqueue_call(func=send_submission_email,kwargs = {'student_id':s.id},result_ttl=5000)
	return jsonify({"resp":"good!"}), 200


def send_submission_email(student_id):
	s = Student.query.filter_by(id=student_id).first()
	if s is None:
		return
	subject = "B'nai Mitzvah information received"
	html_body = render_template('emails/submission.html',student=s)
	text_message = html_body
	html = '<html><head></head><body>{body}</body></html>'.format(body=html_body)
	emailer.send_html(s.email,html_message=html,subject=subject,text_message=text_message)

# Fields called in submission.component.html:
#   formService.entry['DOB'] | date
#   formService.entry['DOBdd'].hdate_str
#   formService.entry['DOBdd'].hdate_str_heb
#   formService.entry['BMdd'].hgregorian | date
#   formService.entry['BMdd'].hdate_str
#   formService.entry['BMdd'].hdate_str_heb
#   let nd of formService.entry['nonDates']
#       nd.hgregorian | date
#       nd.hdate_str
#       nd.hdate_str_heb
@app.route("/api/submissions",methods=["GET","POST"])
def get_submissions():
	if request.json.get('code')==app.config['ADMIN_CODE']:
		students = Student.query.all()
		subs = [student.to_dict() for student in students]
		status = 200
	else:
		subs = []
		status = 401
	return jsonify(subs),status

# retreived:
#   subs['DOB'] | date
#   subs['DOBdd'].hdate_str
#   subs['DOBdd'].hdate_str_heb
#   subs['BMdd'].hgregorian | date
#   subs['BMdd'].hdate_str
#   subs['BMdd'].hdate_str_heb
#   let nd of subs['nonDates']
#       nd.hgregorian | date
#       nd.hdate_str
#       nd.hdate_str_heb
@app.route("/api/submissions_csv/<code>",methods=["GET"])
def get_submissions_csv(code):
	if code==app.config['ADMIN_CODE']:
		students = Student.query.all()
		subs = [student.to_csv_row() for student in students]
		headers = ["Email","Child Name", "Date of Birth", "School", "Religious School","Reception at Services Venue?","Over 200 guests?", "Is a twin?", "Additional Accommodation","Approximate BM Date","Venue Rankings","Dates Unavailable"]
		dest = io.StringIO()
		writer = csv.writer(dest)
		writer.writerow(headers)
		for row in subs:
			writer.writerow(row)
		output = make_response(dest.getvalue(),200)
		output.headers["Content-Disposition"] = "attachment; filename=mitzvah_students.csv"
		output.headers["Content-type"] = "text/csv"
	else:
		output = make_response(jsonify([]),401)

	return output


# # error handlers
# @app.errorhandler(404)
# def page_not_found(e):
#   return render_template('404.html'), 404

# @app.route('/favicon.ico')
# def favicon():
#   return send_static_file('favicon.ico')


if __name__=="__main__":
	app.run(debug=True)
