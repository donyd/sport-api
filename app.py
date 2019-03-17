from flask import Flask, jsonify, request, Response, json

app = Flask(__name__)

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
    return jsonify({'events': events})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')