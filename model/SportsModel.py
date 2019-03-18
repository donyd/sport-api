#!/usr/local/bin/python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import json
from settings import app

db = SQLAlchemy(app)

class Event(db.Model):
    __tablename__ = 'event'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(90))
    start_time = db.Column(db.DateTime, nullable=False)

    sport_id = db.Column(db.Integer, db.ForeignKey('sport.id'))
    sport = db.relationship("Sport", backref=db.backref("event", uselist=False))

    market_id = db.Column(db.Integer, db.ForeignKey('market.id'))
    market = db.relationship("Market", backref=db.backref("event", uselist=False))


class Sport(db.Model):
    __tablename__ = 'sport'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60))

class Market(db.Model):
    __tablename__ = 'market'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(70))

    selection_id = db.Column(db.Integer, db.ForeignKey('selection.id'))
    selection = db.relationship("Selection", backref = db.backref("market"))

class Selection(db.Model):
    __tablename__ = 'selection'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(90))
    odds = db.Column(db.Integer)






