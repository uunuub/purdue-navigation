import os, re
import load
from flask import Flask, jsonify, render_template, request, flash, url_for, session, jsonify
from models import db, Time, Instructor, Type, Room, Building, CRN, Number, Name, Course, Subject
from load import getSchedule, parseSchedule, storeSchedule, load, clear_data
app = Flask(__name__)

# Load config
app.config.from_object("config")

# Init database
db.init_app(app)
db.create_all(app=app)

@app.route("/")
def index():
    """Check for API_KEY"""
    if not os.environ.get("API_KEY"):
        raise RuntimeError("API_KEY not set")
    #return render_template("index.html", key=os.environ.get("API_KEY"))
    return render_template("hello.html")

if __name__ == "__main__":
    print("started")
    # Check environmental variable to see if data's loadeds
    # Load data if it hasn't been
    # Clear data for now
    clear_data(db.session, db.session.metadata)
    # del os.environ["DATA_LOADED"]

    # Generate same schema as the application
    # db.metadata.create_all(engine)

    # Establish connection with database
    # db_session = sessionmaker(bind=engine)
    # session = db_session()

    # Clear all tables in the database
    # clear_data(session)
    # Add to tables
    # addModels(session)

    raw_sched = getSchedule()
    course_info = parseSchedule(raw_sched)
    df = storeSchedule(course_info)
    load(db.session, df)

    app.run()
