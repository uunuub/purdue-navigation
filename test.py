# SQLAlchemy tools
from datetime import time
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

# Database formats
from models import Time, Instructor, Type, Room, Building, CRN, Number, Name, Course, Subject

# Data gathering
import pandas
from load import db, getSchedule, parseSchedule, storeSchedule, clear_data, load

def addModels(session):
	cname = Name(name="Breadboard Life")
	cnum = Number(number=25000)
	csub = Subject(subject="CS")
	ccrn = CRN(crn=15200)
	cbld = Building(building="LWSN")
	croom = Room(room="B148")
	ctype = Type(stype="LEC")
	cinstr = Instructor(instructor="George Adams")
	ctime = Time(start_time=time(hour=2), end_time=time(hour=3))
	course = Course(name=cname, number=cnum, crn=ccrn, building=cbld, 
				room=croom, stype=ctype, instructor=cinstr, time=ctime)
	
	# Add to database
	session.add(cname)	
	session.add(cnum)
	session.add(csub)
	session.add(cbld)
	session.add(croom)
	session.add(ctype)
	session.add(cinstr)
	session.add(ctime)
	session.commit()

if __name__ == "__main__":
	# Create sqlite engine
	engine = create_engine("sqlite:///test.db")#, echo=True)
	# Generate same schema as the application
	db.metadata.create_all(engine)

	# Establish connection with database
	db_session = sessionmaker(bind=engine)
	session = db_session()

	# Clear all tables in the database
	clear_data(session)
	# Add to tables
	# addModels(session)

	raw_sched = getSchedule()
	course_info = parseSchedule(raw_sched)
	df = storeSchedule(course_info)
	load(session, df)

	session.close()

