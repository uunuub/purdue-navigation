import os, re
from flask import Flask, jsonify, render_template, request, flash, url_for, session, jsonify
from models import db, Time, Instructor, Type, Room, Building, CRN, Number, Name, Course
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