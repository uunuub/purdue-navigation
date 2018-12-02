import os, re

import click
from flask import Flask, jsonify, render_template, request 
from flask import flash, url_for, session, jsonify, Response
from flask_script import Manager, Server

from models import db, Time, Instructor, Type, Room, Building, CRN, Number, Name, Course, Subject
from load import getSchedule, parseSchedule, storeSchedule, load, clear_data
app = Flask(__name__)

# Load config
app.config.from_object("config")

# Init database
db.init_app(app)
db.create_all(app=app)

@app.cli.command()
def init():
	with app.app_context():
		# Log Loading
		app.logger.info("Start Loading Data...")
		
		# Clear data in database
		clear_data(db.session, db.metadata)

		# Get Raw HTML with schedule
		raw_sched = getSchedule()

		# Parse HTML and store schedule into dataframe
		course_info = parseSchedule(raw_sched)
		df = storeSchedule(course_info)

		# Load data into database
		load(db.session, df)

		app.logger.info("Finished Loading Data...")

@app.route("/api/courses", methods=["GET"])
def courses():
	join_tables = Course.query.join(Name).join(Number).join(Type).join(Building)
	option = join_tables.filter(Number.number.like(18000)).all()

	print(type(option[0]))
	return jsonify(option[0])

@app.route("/")
def index():
	"""Check for API_KEY"""
	if not os.environ.get("API_KEY"):
		raise RuntimeError("API_KEY not set")
	#return render_template("index.html", key=os.environ.get("API_KEY"))
	return render_template("hello.html")

if __name__ == "__main__":
	# Check environmental variable to see if data's loadeds
	# del os.environ["DATA_LOADED"]
	app.run()