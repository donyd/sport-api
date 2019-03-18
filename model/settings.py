#!/usr/local/bin/python
from flask import Flask

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///D:/WorkPad/Dev/sporty_d/api/model/database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False