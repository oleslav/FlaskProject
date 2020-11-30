from app import Base, db


class User(Base):
    __tablename__ = "users"
    id = db.Column(db.INTEGER, primary_key=True)
    name = db.Column(db.VARCHAR(20), nullable=False)
    password = db.Column(db.VARCHAR(20), nullable=False)


class Tag(Base):
    __tablename__ = "tags"
    id = db.Column(db.INTEGER, primary_key=True)
    name = db.Column(db.VARCHAR(length=255), nullable=False)


class Note(Base):
    __tablename__ = "notes"
    id = db.Column(db.INTEGER, primary_key=True)
    text = db.Column(db.VARCHAR(404), nullable=False)
    numberEdits = db.Column(db.INTEGER, default=0)
    tag_id = db.Column(db.INTEGER, db.ForeignKey(Tag.id))
    tag = db.relationship("Tag", backref=db.backref("tag"))


class NoteStatistic(Base):
    __tablename__ = "noteStatistic"
    id = db.Column(db.INTEGER, primary_key=True)
    userId = db.Column(db.INTEGER, db.ForeignKey(User.id))
    user = db.relationship(User, backref=db.backref("user"))
    noteId = db.Column(db.INTEGER, db.ForeignKey(Note.id))
    note = db.relationship(Note, backref=db.backref("note"))
    time = db.Column(db.DATETIME, nullable=False)
