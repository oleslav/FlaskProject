import datetime
from config import Base, db
from werkzeug.security import generate_password_hash

contribs = db.Table('contribs',
                    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
                    db.Column('note_id', db.Integer, db.ForeignKey('note.id'), primary_key=True)
                    )


class User(Base):
    id = db.Column(db.INTEGER, primary_key=True)
    username = db.Column(db.VARCHAR(20), nullable=False)
    password = db.Column(db.VARCHAR(128), nullable=False)

    def __init__(self, username, password):
        self.username = username
        self.password = generate_password_hash(password)

    def __str__(self):
        return f"<User: {self.username}>"


class Tag(Base):
    id = db.Column(db.INTEGER, primary_key=True)
    name = db.Column(db.VARCHAR(20), nullable=False)

    def __str__(self):
        return f"<Tag: {self.name}>"


class Note(Base):
    id = db.Column(db.INTEGER, primary_key=True)
    text = db.Column(db.VARCHAR(404), nullable=False)
    user_id = db.Column(db.INTEGER, db.ForeignKey(User.id))
    user = db.relationship(User)
    tag_id = db.Column(db.INTEGER, db.ForeignKey(Tag.id))
    tag = db.relationship(Tag, backref=db.backref("tag"))
    co_authorship = db.relationship('User', secondary=contribs, backref=db.backref('contributors', lazy='dynamic'))

    def __str__(self):
        return f"<Note: {self.id}>"


class NoteStatistic(Base):
    id = db.Column(db.INTEGER, primary_key=True)
    user_id = db.Column(db.INTEGER, db.ForeignKey(User.id))
    user = db.relationship(User, backref=db.backref("user"))
    note_id = db.Column(db.INTEGER, db.ForeignKey(Note.id))
    note = db.relationship(Note, backref=db.backref("note"))
    time = db.Column(db.DATETIME, default=datetime.datetime.utcnow, nullable=False)

    def __str__(self):
        return f"<NoteStatistic: {self.id}>"
