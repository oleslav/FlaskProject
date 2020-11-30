from models import *
import datetime


user = User(name="Test", password="1234")
user1 = User(name="User1", password="4321")
tag = Tag(name="Detective")
note = Note(text="Some text", tag=tag)
stat = NoteStatistic(user=user, note=note, time=datetime.datetime.now())
db.session.add(user)
db.session.add(user1)
db.session.add(tag)
db.session.add(note)
db.session.add(stat)

db.session.commit()