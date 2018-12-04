import os, re

import click
import json
from flask import Flask, jsonify, render_template, request, abort
from flask import flash, url_for, session, jsonify, Response, send_from_directory
from flask_script import Manager, Server
from flask_migrate import Migrate

from models import db, Time, Instructor, Type, Room, Building, CRN, Number, Name, Course, Subject
from load import getSchedule, parseSchedule, storeSchedule, load, clear_data

from datetime import datetime
app = Flask(__name__, static_folder='./build')
migrate = Migrate(app, db)

# Load config
app.config.from_object("config")

# Init database
db.init_app(app)
db.create_all(app=app)

@app.shell_context_processor
def make_shell_context():
	return {
		"db": db,
		"Time": Time, 
		"Instructor": Instructor, 
		"Type": Type, 
		"Room": Room, 
		"Building": Building, 
		"CRN": CRN, 
		"Number": Number, 
		"Name": Name, 
		"Course": Course, 
		"Subject": Subject
	}

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

@app.route("/api/courses")
def api_courses():
	if not request.args.get("building") or not request.args.get("room"):
		return jsonify({"message": "no building or room given"})

	# Query with given parameter strings
	join_tables = Course.query.join(Room).join(Building)
	option = join_tables.filter(Room.room.like(request.args.get("room"))).all()

	# Get dictionary of the courses
	courses = {"Courses": [course.to_json() for course in option]}
	return jsonify(courses)

@app.route("/api/buildings/<building>", methods=["GET"])
def api_building_rooms(building):
	# Check if building exists
	query_building = Building.query.filter(Building.building.like(building + "%")).first()
	if not query_building:
		abort(404)

	print(query_building.building)
	# Get all rooms with its time
	roomsTime = {}
	roomsAvail = {}
	for room in query_building.rooms:
		# Get all courses with current room
		times = []
		for course in Course.query.join(Room).join(Time).filter(Course.room == room).all():
			times.append((course.time.start_time, course.time.end_time))
		
		roomsTime[room.room] = sorted(times)


	# Get current time
	curTime = datetime.now().time()
	# curTime = datetime.strptime("11:21", "%H:%M").time()
	# Set availability of each room
	for room, classTimes in roomsTime.items():
		# Set initial flags
		free = True
		changet = datetime.strptime("23:59", "%H:%M").time()
	
		# Go through all time frames
		for tframe in classTimes:
			if curTime < tframe[0]:

				free = True
				changet = tframe[0]
				break
			# Check if it's occupied
			elif curTime < tframe[1]:
				free = False
				changet = tframe[1]
				break
		
		roomsAvail[room] = (free, changet.strftime("%H:%M"))

	return jsonify(roomsAvail)

@app.route("/api/buildings", methods=["GET"])
def api_buildings():
	# Query for all buildings
	query = Building.query.all()
	buildings = {"Buildings": [building.building for building in query]}

	return jsonify(buildings)

# Serve React App
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path != "" and os.path.exists("./build/" + path):
        return send_from_directory('./build', path)
    else:
        return send_from_directory('./build', 'index.html')

if __name__ == "__main__":
	# Check environmental variable to see if data's loadeds
	# del os.environ["DATA_LOADED"]
	app.run(host="0.0.0.0", port=20000)
