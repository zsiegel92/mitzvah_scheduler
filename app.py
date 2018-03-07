from flask import Flask,jsonify
import os

from database import db
from models import School

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

def pre_dict(queries):
    return list(map(lambda x: x.to_dict(),queries))

@app.route("/")
def index():
	return app.send_static_file('index.html')

@app.route("/api/schools/")
def get_schools():
    return jsonify(pre_dict(School.query.all())),200

@app.route("/api/schools/id/<id>")
def get_school(id):
    return jsonify(School.query.filter_by(id=id).first().to_dict()),200

@app.route("/api/schools/add")
def add_school():
    pass

if __name__=="__main__":
	app.run(debug=True)
