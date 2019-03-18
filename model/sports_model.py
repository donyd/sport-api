#!/usr/local/bin/python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json
from settings import app

db = SQLAlchemy(app)

class Event(db.Model):
    __tablename__ = 'event'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(90))
    start_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    sport_id = db.Column(db.Integer, db.ForeignKey('sport.id'))
    sport = db.relationship("Sport", backref=db.backref("event", uselist=False))

    market_id = db.Column(db.Integer, db.ForeignKey('market.id'))
    market = db.relationship("Market", backref=db.backref("event", uselist=False))

    def add_event(_id, _name, _start_time, _sport_id, _market_id,):
        new_event = Event(id=_id, name=_name, start_time=_start_time, sport_id=_sport_id, market_id=_market_id)
        db.session.add(new_event)

        try:
            db.session.commit()
        except:
            db.session.rollback()
            raise
        finally:
            db.session.close()

    def get_all_events():
        return Event.query.all()

    def __repr__(self):
        event_object = {
            'id': self.id,
            'name': self.name,
            #'start_time': self.start_time,
            'sport_id': self.sport_id,
            'market_id': self.market_id
        }

        return json.dumps(event_object)


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






