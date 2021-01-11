from app import app, db

user = {
    "id": 1,
    "username": "fayon",
    "password": "123"
}


client = app.test_client()


def get_token():
    return dict(client.get('/user/login', json={'username': user["username"], 'password': user["password"]}).json)['access_token']


def test_start():
    db.create_all()
    create_user()
    assert True


def create_user():
    client.post('/user', json={'username': user["username"], 'password': user["password"]})


def test_get_notes():
    res = client.get('/notes', headers={'Authorization': 'Bearer ' + str(get_token())})
    assert res.status_code == 200


def test_post_notes():
    json = {
        "id": 1,
        "text": "Text 1",
        "user_id": 1,
        "tag": "Tag 1"
    }
    res = client.post('/notes', json=json, headers={'Authorization': 'Bearer ' + str(get_token())})
    assert res.status_code == 200


def test_post_notes_400():
    json = None
    res = client.post('/notes', json=json, headers={'Authorization': 'Bearer ' + str(get_token())})
    assert res.status_code == 400


def test_get_notes_by_id():
    res = client.get('/notes/1', headers={'Authorization': 'Bearer ' + str(get_token())})
    assert res.status_code == 200


def test_get_notes_by_id_404():
    res = client.get('/notes/0', headers={'Authorization': 'Bearer ' + str(get_token())})
    assert res.status_code == 404


def test_put_notes_by_id():
    json = {
        "text": "Put 1",
        "user_id": 1,
        "tag": "Put Tag 1"
    }
    res = client.put('/notes/1', json=json, headers={'Authorization': 'Bearer ' + str(get_token())})
    assert res.status_code == 202


def test_put_notes_by_id_404():
    json = {
        "text": "Put 1",
        "user_id": 1,
        "tag": "Put Tag 1"
    }
    res = client.put('/notes/0', json=json, headers={'Authorization': 'Bearer ' + str(get_token())})
    assert res.status_code == 404


def test_permit_user_by_id():
    json = {
        "note_id": 1
    }
    res = client.post('/permit', json=json, headers={'Authorization': 'Bearer ' + str(get_token())})
    assert res.status_code == 200


def test_permit_user_by_id_400():
    json = None
    res = client.post('/permit', json=json, headers={'Authorization': 'Bearer ' + str(get_token())})
    assert res.status_code == 400


def test_permit_user_by_id_404():
    json = {
        "note_id": 0
    }
    res = client.post('/permit', json=json, headers={'Authorization': 'Bearer ' + str(get_token())})
    assert res.status_code == 404


def test_delete_notes_by_id():
    res = client.delete('/notes/1', headers={'Authorization': 'Bearer ' + str(get_token())})
    assert res.status_code == 204


def test_delete_notes_by_id_404():
    res = client.delete('/notes/0', headers={'Authorization': 'Bearer ' + str(get_token())})
    assert res.status_code == 404


def test_create_user():
    json = {
        'username': user["username"],
        'password': "111"
    }
    res = client.post('/user', json=json)
    assert res.status_code == 200


def test_create_user_400():
    json = None
    res = client.post('/user', json=json)
    assert res.status_code == 400


def test_create_user_no_data():
    json = {
        'username': '',
        'password': ''
    }
    res = client.post('/user', json=json)
    assert res.status_code == 400


def test_user_login():
    json = {
        'username': user["username"],
        'password': user["password"]
    }
    res = client.get('/user/login', json=json)
    assert res.status_code == 200


def test_user_login_400():
    json = None
    res = client.get('/user/login', json=json)
    assert res.status_code == 400


def test_user_login_401():
    json = {
        'username': user["username"],
        'password': "1234123"
    }
    res = client.get('/user/login', json=json)
    assert res.status_code == 401


def test_user_logout():
    res = client.get('/user/logout')
    assert res.status_code == 200


def test_get_userstats_by_id():
    res = client.get('/userstats/1', headers={'Authorization': 'Bearer ' + str(get_token())})
    assert res.status_code == 200