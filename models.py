from flask_sqlalchemy import SQLAlchemy

# Intatiate SQLAlchemy object
db = SQLAlchemy()

# Base model for other to inherit from
class Base(db.Model):
	__abstract__ = True

	# Base attributes
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
	date_created = db.Column(db.DateTime, default=db.func.current_timestamp(),
							onupdate=db.func.current_timestamp())

# Model for course time
class Time(Base):
	__tablename__ = "time" 
	start_time = db.Column(db.Time(timezone=True))
	end_time = db.Column(db.Time(timezone=True))

	def __repr__(self):
		return (self.start_time.strftime("%H:%M") + " - " + self.end_time.strftime("%H:%M"))

# Model for instructor
class Instructor(Base):
	__tablename__ = "instructor" 
	instructor = db.Column(db.String(50), unique=True)

	def __repr__(self):
		return self.instructor

# Model for course type
class Type(Base):
	__tablename__ = "type" 
	stype = db.Column(db.String(50), unique=True)
	
	def __repr__(self):
		return self.stype
 
# Model for room
class Room(Base):
	__tablename__ = "room" 
	room = db.Column(db.String(50))
	
	def __repr__(self):
		return self.room
 
# Model for building
class Building(Base):
	__tablename__ = "building" 
	building = db.Column(db.String(50), unique=True)
	
	def __repr__(self):
		return self.building

# Model for crn
class CRN(Base):
	__tablename__ = "crn" 
	crn = db.Column(db.Integer, unique=True)
	
	def __repr__(self):
		return str(self.crn)

# Model for course number
class Number(Base):
	__tablename__ = "number" 
	number = db.Column(db.Integer, unique=True)

	def __repr__(self):
		return str(self.number)

# Model for course subject
class Subject(Base):
	__tablename__ = "subject" 
	subject = db.Column(db.String(50), unique=True)

	def __repr__(self):
		return self.subject

# Model for course name
class Name(Base):
	__tablename__ = "name" 
	name = db.Column(db.String(50), unique=True)

	def __repr__(self):
		return self.name

# Model for course
class Course(Base):
	__tablename__ = "course" 
	# Foreign Keys of other tables
	name_id = db.Column(db.Integer, db.ForeignKey("name.id"))
	number_id = db.Column(db.Integer, db.ForeignKey("number.id"))
	subject_id = db.Column(db.Integer, db.ForeignKey("subject.id"))
	crn_id = db.Column(db.Integer, db.ForeignKey("crn.id"))
	building_id = db.Column(db.Integer, db.ForeignKey("building.id"))
	room_id = db.Column(db.Integer, db.ForeignKey("room.id"))
	type_id = db.Column(db.Integer, db.ForeignKey("type.id"))
	instructor_id = db.Column(db.Integer, db.ForeignKey("instructor.id"))
	time_id = db.Column(db.Integer, db.ForeignKey("time.id"))
	# Bitwise operations will be used to extract available days
	days = db.Column(db.CHAR(1), default=0) 

	# Connect other models to Course
	name = db.relationship("Name", backref=db.backref("courses", lazy="dynamic"))
	number = db.relationship("Number", backref=db.backref("courses", lazy="dynamic"))
	subject = db.relationship("Subject", backref=db.backref("courses", lazy="dynamic"))
	crn = db.relationship("CRN", backref=db.backref("courses", lazy="dynamic"))
	building = db.relationship("Building", backref=db.backref("courses", lazy="dynamic"))
	room = db.relationship("Room", backref=db.backref("courses", lazy="dynamic"))
	stype = db.relationship("Type", backref=db.backref("courses", lazy="dynamic"))
	instructor = db.relationship("Instructor", backref=db.backref("courses", lazy="dynamic"))
	time = db.relationship("Time", backref=db.backref("courses", lazy="dynamic"))








