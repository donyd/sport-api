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
@app.route('/api/events/<int:id>')
def get_event_by_id(id):
    event_returned = sports_model.Event.get_event_by_id(id)
    event_id = event_returned.get('id')
    sport_id = event_returned.get('sport_id')

    market_returned = sports_model.Market.get_market_by_event_id(id)
    selections_returned = sports_model.Selection.get_all_selections()
    sport_returned = sports_model.Sport.get_sport_by_id(sport_id)
    response_url = "http://127.0.0.1:5000/api/events/" + str(event_id)
    event = {
        'event': {
            'id': event_id,
            'url': response_url,
            'name': event_returned.get('name'),
            'startTime': event_returned.get('start_time'),
            'sport': {
                'id': sport_id,
                'name': sport_returned.get('name'),
            },
            'markets': [
                {
                    'id': market_returned.get('id'),
                    'name': market_returned.get('name'),
                    'selections': [
                        selections_returned
                    ]
                }
            ]
        }
    }

    # return jsonify({'event': {
    #     'id': event_id,
    #     'url': response_url,
    #     'name': dict_event.get('name'),
    #     'startTime': dict_event.get('start_time'),
    #     'sport': {
    #         'id': dict_event.get('sport_id'),
    #         'name': 'Test'#dict_sport.get('name')
    #     },
    #     'markets': [
    #         {
    #             'id': dict_market['id'],
    #             'name': dict_market.get('name'),
    #             'selections': [
    #                 {
    #                     dict_selections
    #                 }
    #             ]
    #         }
    #     ]
    #
    # }})
    return jsonify(event)
    #print(sports_model.Event.get_event_by_id(id))
    #return jsonify({'event': sports_model.Event.get_event_by_id(id)})
    #return jsonify({'events': sports_model.Event.get_all_events()})


# POST /event
@app.route('/api/events', methods=['POST'])
def add_event():
    request_data = request.get_json()

    if(request_data['message_type'] == "NewEvent"):
        if(validEventData(request_data)):
            sports_model.Event.add_event(request_data['event']['id'], request_data['event']['name'], datetime.now(), request_data['event']['sport']['id'])
            sports_model.Market.add_market(request_data['event']['markets'][0]['id'], request_data['event']['markets'][0]['name'], request_data['event']['id'], request_data['event']['sport']['id'])

            if ((request_data['event']['sport']['name'] == "Golf") and (len(request_data['event']['markets'][0]['selections']) > 2)):
                sports_model.Selection.add_selection(request_data['event']['markets'][0]['selections'][0]['id'], request_data['event']['markets'][0]['selections'][0]['name'], request_data['event']['markets'][0]['selections'][0]['odds'], request_data['event']['id'], request_data['event']['markets'][0]['id'])
                sports_model.Selection.add_selection(request_data['event']['markets'][0]['selections'][1]['id'], request_data['event']['markets'][0]['selections'][1]['name'], request_data['event']['markets'][0]['selections'][1]['odds'], request_data['event']['id'], request_data['event']['markets'][0]['id'])
                sports_model.Selection.add_selection(request_data['event']['markets'][0]['selections'][2]['id'], request_data['event']['markets'][0]['selections'][2]['name'], request_data['event']['markets'][0]['selections'][2]['odds'], request_data['event']['id'], request_data['event']['markets'][0]['id'])
            else:
                sports_model.Selection.add_selection(request_data['event']['markets'][0]['selections'][0]['id'], request_data['event']['markets'][0]['selections'][0]['name'], request_data['event']['markets'][0]['selections'][0]['odds'], request_data['event']['id'], request_data['event']['markets'][0]['id'])
                sports_model.Selection.add_selection(request_data['event']['markets'][0]['selections'][1]['id'], request_data['event']['markets'][0]['selections'][1]['name'], request_data['event']['markets'][0]['selections'][1]['odds'], request_data['event']['id'], request_data['event']['markets'][0]['id'])

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

def event_reformation():
    pass
