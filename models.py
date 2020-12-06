import datetime

from config import Base, db
from werkzeug.security import generate_password_hash


class User(Base):
    __tablename__ = "users"
    id = db.Column(db.INTEGER, primary_key=True)
    username = db.Column(db.VARCHAR(20), nullable=False)
    password = db.Column(db.VARCHAR(128), nullable=False)

    def __init__(self, username, password):
        self.username = username
        self.password = generate_password_hash(password)

    def __str__(self):
        return f"<User: {self.username}>"


class Tag(Base):
    __tablename__ = "tags"
    id = db.Column(db.INTEGER, primary_key=True)
    name = db.Column(db.VARCHAR(length=255), nullable=False)

    def __str__(self):
        return f"<Tag: {self.name}>"


class Note(Base):
    __tablename__ = "notes"
    id = db.Column(db.INTEGER, primary_key=True)
    text = db.Column(db.VARCHAR(404), nullable=False)
    numberEdits = db.Column(db.INTEGER, default=0)
    tag_id = db.Column(db.INTEGER, db.ForeignKey(Tag.id))
    tag = db.relationship("Tag", backref=db.backref("tag"))

    def __str__(self):
        return f"<Note: {self.id}>"


class NoteStatistic(Base):
    __tablename__ = "noteStatistic"
    id = db.Column(db.INTEGER, primary_key=True)
    userId = db.Column(db.INTEGER, db.ForeignKey(User.id))
    user = db.relationship(User, backref=db.backref("user"))
    noteId = db.Column(db.INTEGER, db.ForeignKey(Note.id))
    note = db.relationship(Note, backref=db.backref("note"))
    time = db.Column(db.DATETIME, default=datetime.datetime.utcnow, nullable=False)

    def __str__(self):
        return f"<NoteStatistic: {self.id}>"
