from flask import Flask,jsonify
import os

from database import db
from models import School

app = Flask(__name__,static_folder='mitzvah/static')
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

def pre_dict(queries):
	return list(map(lambda x: x.to_dict(),queries))

# @app.route("/")
# def index():
# 	# return "hello"
# 	return app.send_static_file('index.html')

# Program catch-all for routes to send the static index.html file to the current app
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def index(path):
	return app.send_static_file('index.html')

# @app.route('/<path:path>')
# def static_proxy(path):
# 	# send_static_file will guess the correct MIME type
# 	return app.send_static_file(path)

@app.route("/api/schools/")
def get_schools():
	schools = School.query.all()
	if len(schools)>0:
		return jsonify(pre_dict(School.query.all())),200
	else:
		return jsonify(['no schools']),200
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


# # error handlers
# @app.errorhandler(404)
# def page_not_found(e):
# 	return render_template('404.html'), 404

# @app.route('/favicon.ico')
# def favicon():
# 	return send_static_file('favicon.ico')


if __name__=="__main__":
	app.run(debug=True)
