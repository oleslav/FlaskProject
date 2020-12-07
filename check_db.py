from models import *

if __name__ == '__main__':
    db.create_all()

    user1 = User(username="Olaf", password="1111")
    user2 = User(username="Bengin", password="1111")
    user3 = User(username="Maira", password="1111")

    tag1 = Tag(name='cook')
    tag2 = Tag(name='music')

    note1 = Note(text="Some text", user=user1, tag=tag1)
    note2 = Note(text="Some text", user=user1, tag=tag2)

    note_statistic1 = NoteStatistic(user=user1, note=note2)
    note_statistic2 = NoteStatistic(user=user3, note=note1)

    db.session.add(user1)
    db.session.add(user2)
    db.session.add(user3)
    db.session.commit()

    db.session.add(tag1)
    db.session.add(tag2)
    db.session.commit()

    db.session.add(note1)
    db.session.add(note2)
    db.session.commit()

    db.session.add(note_statistic1)
    db.session.add(note_statistic2)
    db.session.commit()

    note1.co_authorship.append(user3)
    note1.co_authorship.append(user2)
    note2.co_authorship.append(user3)
    db.session.commit()
