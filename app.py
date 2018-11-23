import os, re
import load
from flask import Flask, jsonify, render_template, request, flash, url_for, session, jsonify
from models import db, Time, Instructor, Type, Room, Building, CRN, Number, Name, Course, Subject
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
    if not os.environ.get("DATA_LOADED"):
        load.load(db.session)
        os.environ["DATA_LOADED"] = "1"
    else:
        # Clear data for now
        load.clear_data(db.session)
        del os.environ["DATA_LOADED"]

    app.run()
