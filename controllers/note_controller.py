import datetime
from flask_jwt_extended import create_access_token
from werkzeug.security import check_password_hash
from config import *
from models import *


def get_current_user():
    return User.query.filter_by(username=get_jwt_identity()).first()


@app.route('/notes', methods=['GET'])
@jwt_required
def get_notes():
    note = Note.query.all()
    note_list = {'note_list': []}
    for i in note:
        note_list['note_list'].append({'id': i.id, 'text': i.text, 'created by': i.user_id})
    return jsonify(note_list)


@app.route('/notes', methods=['POST'])
@jwt_required
def post_notes():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400
    text = request.json.get('text', None)
    if text is None:
        return jsonify(msg="Missing data"), 400
    note = Note(text=text, user=get_current_user())
    db.session.add(note)
    db.session.add(NoteStatistic(note=note, user=get_current_user()))
    db.session.commit()
    return jsonify({"msg": "Note successfully added"}), 200


@app.route('/notes/<note_id>', methods=['GET'])
@jwt_required
def get_notes_get_by_id(note_id):
    note = Note.query.get(note_id)
    if note is None:
        return jsonify(status='article not found'), 404
    return jsonify(article={'id': note.id, 'text': note.text}), 200


@app.route('/notes/<note_id>', methods=['PUT'])
@jwt_required
def put_notes_get_by_id(note_id):
    note = Note.query.get(note_id)
    if note is None:
        return jsonify(status='article not found'), 404

    note_from_user = Note.query.filter(User.contributors.any(id=note_id)).all()
    user = get_current_user()

    allowed = False
    if note.user_id == user.id:
        allowed = True
    else:
        for i in note_from_user:
            if i.id == user.id:
                allowed = True
                break

    if not allowed:
        return jsonify({"msg": "User dont have a permission to modify note"}), 403

    new_text = request.json.get('text', None)
    if new_text:
        db.session.add(NoteStatistic(note=note, user=user))
        note.text = new_text
        db.session.commit()
        return jsonify(status='update note'), 202
    else:
        return jsonify(status='Bad input data'), 404


@app.route('/notes/<note_id>', methods=['DELETE'])
@jwt_required
def delete_notes_get_by_id(note_id):
    user = get_current_user()
    note = Note.query.get(note_id)
    if note is None:
        return jsonify(status='article not found'), 404

    if user.id != note.user_id:
        return jsonify({"msg": "User have a permission to delete note"}), 403
    db.session.delete(note)
    db.session.commit()
    return jsonify(status='deleted'), 204


@app.route('/permit', methods=['POST'])
@jwt_required
def permit_user_by_id():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400

    user_id = int(request.json.get('user_id', None))
    note_id = int(request.json.get('note_id', None))

    user = get_current_user()
    note = Note.query.get(note_id)

    if user is None:
        return jsonify({"msg": "Bad user_id"}), 404

    if note is None:
        return jsonify({"msg": "Bad note_id"}), 404

    if user.id != note.user_id:
        return jsonify({"msg": "User have a permission to add new contributors"}), 403

    if (not user_id) or (not note_id):
        return jsonify({"msg": "Bad data"}), 404

    notes_from_note = Note.query.filter(Note.co_authorship.any(id=note_id)).all()
    notes_from_user = Note.query.filter(User.contributors.any(id=user_id)).all()

    user_counter = 0
    for i in notes_from_note:
        for note in notes_from_user:
            if i.id == note.id:
                return jsonify({"msg": "Alredy exists"}), 409
        user_counter += 1
    if user_counter > 5:
        return jsonify({"msg": "Too many editors"}), 403

    note = Note.query.get(note_id)
    user = User.query.get(user_id)
    note.co_authorship.append(user)
    db.session.commit()
    return jsonify({"msg": "New permision for user successfully added"}), 200
