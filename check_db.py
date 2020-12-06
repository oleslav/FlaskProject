from models import *

if __name__ == '__main__':
    db.create_all()

    # print(User.query.limit(100).all())
    # print(User.query.get(1))
    # user = User(name="Test", password="1234")
    # user1 = User(name="User1", password="4321")
    # tag = Tag(name="Detective")
    # note = Note(text="Some text", tag=tag)
    # stat = NoteStatistic(user=user, note=note, time=datetime.datetime.now())
    # db.session.add(user)
    # db.session.add(user1)
    # db.session.add(tag)
    # db.session.add(note)
    # db.session.add(stat)
    # db.session.commit()
