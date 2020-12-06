import datetime
from flask_jwt_extended import create_access_token
from werkzeug.security import check_password_hash
from config import *
from models import *
# Checked

def get_current_user():
    return User.query.filter_by(username=get_jwt_identity()).first()

@app.route('/notes', methods=['GET'])
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
            note.text = new_text
            note.numberEdits += 1
            db.session.add(NoteStatistic(note=note, user=get_current_user()))
            db.session.commit()
            return jsonify(status='update note'), 202
        else:
            return jsonify(status='Bad input data'), 204
    elif request.method == 'DELETE':
        note = Note.query.get(note_id)
        if note is None:
            return jsonify(status='article not found'), 404
        db.session.delete(note)
        db.session.commit()
        return jsonify(status='deleted'), 204
    else:
        return jsonify({"msg": "Wrong method"}), 404
