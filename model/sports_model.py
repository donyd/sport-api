#!/usr/local/bin/python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json
from .settings import app

db = SQLAlchemy(app)

class Event(db.Model):
    __tablename__ = 'event'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(90))
    start_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    sport_id = db.Column(db.Integer, db.ForeignKey('sport.id'))
    sport = db.relationship("Sport", backref=db.backref("sport", uselist=False))

    def add_event(_id, _name, _start_time, _sport_id):
        new_event = Event(id=_id, name=_name, start_time=_start_time, sport_id=_sport_id)
        db.session.add(new_event)

        try:
            db.session.commit()
        except:
            db.session.rollback()
            raise
        finally:
            db.session.close()

    def get_event_by_id(_id):
        return Event.json(Event.query.filter_by(id=_id).first())


    def get_all_events():
        return [Event.json(event) for event in Event.query.all()]

    def __repr__(self):
        event_object = {
            'id': self.id,
            'name': self.name,
            'start_time': self.start_time,
            'sport_id': self.sport_id
        }

        return json.dumps(event_object, default=str)

    def json(self):
        return {
            'id': self.id,
            'name': self.name,
            'start_time': self.start_time,
            'sport_id': self.sport_id
        }



class Sport(db.Model):
    __tablename__ = 'sport'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60))

    def add_sport(_id, _name):
        sport = Sport(id=_id, name=_name)
        db.session.add(sport)

        try:
            db.session.commit()
        except:
            db.session.rollback()
            raise
        finally:
            db.session.close()

    def get_sport_by_id(_id):
        return Sport.json(Sport.query.filter_by(id=_id).first())

    def __repr__(self):
        sport_object = {
            'id': self.id,
            'name': self.name
        }

        return json.dumps(sport_object, default=str)

    def json(self):
        return {
            'id': self.id,
            'name': self.name
        }


class Market(db.Model):
    __tablename__ = 'market'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(70))

    event_id = db.Column(db.Integer, db.ForeignKey('event.id'))
    event = db.relationship("Event", backref=db.backref("market_event", uselist=False))

    sport_id = db.Column(db.Integer, db.ForeignKey('sport.id'))
    sport = db.relationship("Sport", backref=db.backref("market_sport", uselist=False))

    def add_market(_id, _name, _event_id, _sport_id):
        market = Market(id=_id, name=_name, event_id=_event_id, sport_id=_sport_id)
        db.session.add(market)

        try:
            db.session.commit()
        except:
            db.session.rollback()
            raise
        finally:
            db.session.close()

    def get_market_by_id(_id):
        current_market = Market.query.filter_by(id=_id).first()
        return current_market

    def get_market_by_event_id(_event_id):
        return Market.json(Market.query.filter_by(event_id=_event_id).first())

    def get_all_markets():
        return Market.query.all()

    def __repr__(self):
        market_object = {
            'id': self.id,
            'name': self.name,
            'sport_id': self.sport_id
        }

        return json.dumps(market_object, default=str)

    def json(self):
        return {
            'id': self.id,
            'name': self.name,
            'event_id': self.event_id
        }

class Selection(db.Model):
    __tablename__ = 'selection'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(90))
    odds = db.Column(db.Float)

    event_id = db.Column(db.Integer, db.ForeignKey('event.id'))
    event = db.relationship("Event", backref=db.backref("event", uselist=False))

    market_id = db.Column(db.Integer, db.ForeignKey('market.id'))
    market = db.relationship("Market", backref=db.backref("market", uselist=False))

    def add_selection(_id, _name, _odds, _event_id, _market_id):
        selection = Selection(id=_id, name=_name, odds=_odds, event_id=_event_id, market_id=_market_id)
        db.session.add(selection)

        try:
            db.session.commit()
        except:
            db.session.rollback()
            raise
        finally:
            db.session.close()

    def get_selection_by_id(_id):
        return Selection.json(Selection.query.filter_by(id=_id).first())

    def get_selections_by_event_id(_event_id):
        #return Selection.json(Selection.query.filter_by(event_id=_event_id))
        return [Selection.json(selection) for selection in Selection.query.filter_by(event_id=_event_id)]

    def get_all_selections():
        return [Selection.json(selection) for selection in Selection.query.all()]

    def update_odds(_event_id, _selection_id, _odds):
        selection_to_update = Selection.json(Selection.query.filter_by(event_id=_event_id, id=_selection_id))
        selection_to_update.odds = _odds

        db.session.add(selection_to_update)

        try:
            db.session.commit()
        except:
            db.session.rollback()
            raise
        finally:
            db.session.close()


    def __repr__(self):
        selection_object = {
            'id': self.id,
            'name': self.name,
            'odds': self.odds,
            'event_id': self.event_id,
            'market_id': self.market_id
        }

        return json.dumps(selection_object, default=str)

    def json(self):
        return {
            'id': self.id,
            'name': self.name,
            'odds': self.odds,
            'event_id': self.event_id,
            'market_id': self.market_id
        }




