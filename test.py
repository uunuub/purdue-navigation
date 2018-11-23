import sqlalchemy, datetime
from sqlalchemy.orm import sessionmaker
from app import db, app
from models import Time, Instructor, Type, Room, Building, CRN, Number, Name, Course
from load import getSchedule, parseSchedule

def clear_data(session):
    meta = db.metadata
    for table in reversed(meta.sorted_tables):
        print('Clear table %s' % table)
        session.execute(table.delete())
    session.commit()

def testModels(session):
	cname = Name(name="Computer Architecture")
	print(cname)

	cnum = Number(number=25000)
	print(cnum)

	ccrn = CRN(crn=15200)
	print(ccrn)

	cbld = Building(building="LWSN")
	print(cbld)

	croom = Room(room="B148")
	print(croom)

	ctype = Type(stype="LEC")
	print(ctype)

	cinstr = Instructor(instructor="George Adams")
	print(cinstr)

	ctime = Time(start_time=datetime.time(hour=2), end_time=datetime.time(hour=3))
	print(str(ctime))

	course = Course(name=cname, number=cnum, crn=ccrn, building=cbld, 
				room=croom, stype=ctype, instructor=cinstr, time=ctime)
	
	session.add(cname)	
	session.add(cnum)
	session.add(cbld)
	session.add(croom)
	session.add(ctype)
	session.add(cinstr)
	session.add(ctime)
	session.commit()

	print(course.name)
	print(course.number)
	print(course.crn)
	print(course.building)
	print(course.room)
	print(course.stype)
	print(course.instructor)
	print(course.time)

db.app = app
db.init_app(app)

# Clear all tables in the database
clear_data(db.session)

# Generate schema of tables
db.create_all()

# Add to tables
testModels(db.session)

# raw_sched = getSchedule()
# titles, details = parseSchedule(raw_sched) 

