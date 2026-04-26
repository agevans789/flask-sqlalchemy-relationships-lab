#!/usr/bin/env python3

from flask import Flask, jsonify, make_response
from flask_migrate import Migrate

from models import db, Event, Session, Speaker, Bio

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

# TODO: add functionality to all routes

@app.route('/events')
def get_events():
    events = []
    for event in Event.query.all():
        events.append({
            'id': event.id,
            'name': event.name,
            'location': event.location
        })
    return make_response(jsonify(events), 200)


@app.route('/events/<int:id>/sessions')
def get_event_sessions(id):
    event = Event.query.get(id)
    if not event:
        return make_response(jsonify({'error': 'Event not found'}), 404)
    sessions = []
    for session in event.sessions:
        sessions.append({
            'id': session.id,
            'title': session.title,
            'start_time': session.start_time
        })
    return make_response(jsonify(sessions), 200)


@app.route('/speakers')
def get_speakers():
    speakers = []
    for speaker in Speaker.query.all():
        speakers.append({
            'id': speaker.id,
            'name': speaker.name
        })
    return make_response(jsonify(speakers), 200)


@app.route('/speakers/<int:id>')
def get_speaker(id):
    speaker = Speaker.query.filter_by(id=id).first()
    if not speaker:
        return make_response(jsonify({"error": "Speaker not found"}), 404)
    
    # Flatten the bio_text into the main dictionary
    speaker_dict = {
        "id": speaker.id,
        "name": speaker.name,
        "bio_text": speaker.bio.bio_text if speaker.bio else "No bio available"
    }
    return make_response(jsonify(speaker_dict), 200)


@app.route('/sessions/<int:id>/speakers')
def get_session_speakers(id):
    session = Session.query.filter_by(id=id).first()
    if not session:
        return make_response(jsonify({"error": "Session not found"}), 404)
    
    speakers = []
    for s in session.speakers:
        speakers.append({
            "id": s.id,
            "name": s.name,
            # Every speaker in this list must also include the bio_text key
            "bio_text": s.bio.bio_text if s.bio else "No bio available"
        })
    return make_response(jsonify(speakers), 200)



if __name__ == '__main__':
    app.run(port=5555, debug=True)