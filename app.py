#!/usr/local/bin/python
from flask import Flask, jsonify, request, Response, json
from model import sports_model
from model.settings import *
from datetime import datetime


events = {
    "id": 8661032861909884000,
    "message_type": "NewEvent",
    "event": {
        "id": 994839351740,
        "name": "Real Madrid vs Barcelona",
        "startTime": "2018-06-20 10:30:00",
        "sport": {
            "id": 221,
            "name": "Football"
        },
        "markets": [
            {
                "id": 385086549360973400,
                "name": "Winner",
                "selections": [
                    {
                        "id": 8243901714083343000,
                        "name": "Real Madrid",
                        "odds": 1.01
                    },
                    {
                        "id": 5737666888266680000,
                        "name": "Barcelona",
                        "odds": 1.01
                    }
                ]
            }
        ]
    }
}

# GET Events
@app.route('/events')
def get_events():
    return jsonify({'events': sports_model.Event.get_all_events()})

# POST /event
@app.route('/events', methods=['POST'])
def add_event():
    request_data = request.get_json()

    if(request_data['message_type'] == "NewEvent"):
        if(validEventData(request_data)):
            sports_model.Event.add_event(request_data['event']['id'], request_data['event']['name'], datetime.now(), request_data['event']['sport']['id'], request_data['event']['markets'][0]['id'])

            response = Response("", 201, mimetype='application/json')
            response.headers['Location'] = "/events/" + str(request_data['id'])
            return response
        else:
            response = Response(json.dumps(request_data), status=400, mimetype="application/json")
            return response


# TODO: Event Data validity stub
def validEventData(eventObject):
    """

    :param eventObject:
                Event data sent from provider
    :return:
                Boolean dependant on data validity
    """
    return True

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')