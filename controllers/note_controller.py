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
        note_list['note_list'].append({'id': i.id, 'text': i.text, 'edited': i.numberEdits})
    return jsonify(note_list)


@app.route('/notes', methods=['POST'])
@jwt_required
def post_notes():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400
    text = request.json.get('text', None)
    if text is None:
        return jsonify(msg="Missing data"), 400
    note = Note(text=text)
    db.session.add(note)
    db.session.add(NoteStatistic(note=note, user=get_current_user()))
    db.session.commit()
    return jsonify({"msg": "Note successfully added"}), 200


@app.route('/notes/<note_id>', methods=['GET', 'PUT', 'DELETE'])
@jwt_required
def notes_get_by_id(note_id):
    if request.method == 'GET':
        note = Note.query.get(note_id)
        if note is None:
            return jsonify(status='article not found'), 404
        return jsonify(article={'id': note.id, 'text': note.text}), 200
    elif request.method == 'PUT':
        note = Note.query.get(note_id)
        if note is None:
            return jsonify(status='article not found'), 404
        new_text = request.json.get('text', None)
        if new_text:
            print(get_current_user())
            print(get_current_user().id)
            if NoteStatistic.query.filter(
                    NoteStatistic.noteId == note_id,
                    NoteStatistic.noteId == get_current_user().id
            ) is None:
                note.numberEdits += 1

            if note.numberEdits > 5:
                return jsonify({"msg": "Too many editors"}), 403
            note.text = new_text
            db.session.add(note)
            db.session.add(NoteStatistic(note=note, user=get_current_user()))
            db.session.commit()
            return jsonify(status='update note'), 202
        else:
            return jsonify(status='Bad input data'), 204
    elif request.method == 'DELETE':
        note = Note.query.get(note_id)
        if note is None:
            return jsonify(status='article not found'), 404
        note_statistic = NoteStatistic.query.filter_by(note_id=note_id).first()
        if not note_statistic is None:
            db.session.delete(note_statistic)
        db.session.delete(note)
        db.session.commit()
        return jsonify(status='deleted'), 204
    else:
        return jsonify({"msg": "Wrong method"}), 404


@app.route('/permit', methods=['POST'])
@jwt_required
def permit_user_by_id():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400

    user_id = int(request.json.get('user_id', None))
    note_id = int(request.json.get('note_id', None))

    if (not user_id) or (not note_id):
        return jsonify({"msg": "Bad data"}), 404
    permisions = Permisions.query.filter_by()
    if permisions > 5:
        return jsonify({"msg": "Too many editors"}), 403

    new_user = User.query.filter_by(id=user_id).first()

    if new_user is None:
        return jsonify({"msg": "Wrong method"}), 406

    permit = Permisions(userId=user_id, noteId=note_id)
    db.session.add(permit)
    db.session.commit()

    return jsonify({"msg": "New permision for user successfully added"}), 200
