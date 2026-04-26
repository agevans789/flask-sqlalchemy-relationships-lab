from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.ext.associationproxy import association_proxy

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)

# Many-to-Many Association Table
speaker_session = db.Table(
    'speaker_session',
    metadata,
    db.Column('speaker_id', db.Integer, db.ForeignKey('speakers.id'), primary_key=True),
    db.Column('session_id', db.Integer, db.ForeignKey('sessions.id'), primary_key=True)
)

class Event(db.Model):
    __tablename__ = 'events'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    location = db.Column(db.String, nullable=False)

    # Relationship: Event -> Sessions (One-to-Many)
    sessions = db.relationship('Session', back_populates='event', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Event {self.id}, {self.name}, {self.location}>'

class Session(db.Model):
    __tablename__ = 'sessions'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    start_time = db.Column(db.DateTime)
    
    # Foreign Key for One-to-Many
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'))

    # Relationship: Session -> Event
    event = db.relationship('Event', back_populates='sessions')
    
    # Relationship: Session <-> Speaker (Many-to-Many)
    speakers = db.relationship('Speaker', secondary=speaker_session, back_populates='sessions')

    def __repr__(self):
        return f'<Session {self.id}, {self.title}, {self.start_time}>'

class Speaker(db.Model):
    __tablename__ = 'speakers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)

    # Relationship: Speaker <-> Bio (One-to-One)
    bio = db.relationship('Bio', back_populates='speaker', uselist=False, cascade='all, delete-orphan')
    
    # Relationship: Speaker <-> Session (Many-to-Many)
    sessions = db.relationship('Session', secondary=speaker_session, back_populates='speakers')

    def __repr__(self):
        return f'<Speaker {self.id}, {self.name}>'

class Bio(db.Model):
    __tablename__ = 'bios'
    id = db.Column(db.Integer, primary_key=True)
    bio_text = db.Column(db.Text, nullable=False)
    
    # Foreign Key for One-to-One
    speaker_id = db.Column(db.Integer, db.ForeignKey('speakers.id'), unique=True)

    # Relationship: Bio -> Speaker
    speaker = db.relationship('Speaker', back_populates='bio')

    def __repr__(self):
        return f'<Bio {self.id}, {self.bio_text[:20]}...>'

