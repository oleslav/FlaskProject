from flask_jwt_extended import create_access_token
from werkzeug.security import check_password_hash
from config import *
from models import *


@app.route('/user', methods=['POST'])
def create_user():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400
    username = request.json.get('username', None)
    password = request.json.get('password', None)
    if not username:
        return jsonify({
            "errors": [{
                    "status": "400",
                    "source": {"pointer": None},
                    "title": "Invalid Attribute",
                    "detail": "Missing username parameter"
                }]}), 400
    if not password:
        return jsonify({"msg": "Missing password parameter"}), 400
    if username == '' or password == '':
        return jsonify({"msg": "Bad username or password"}), 401
    db.session.add(User(username=username, password=password))
    db.session.commit()
    return jsonify({"Success": "User has been created"}), 200


@app.route('/user/login', methods=['GET'])
def user_login():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400
    username = request.json.get('username', None)
    password = request.json.get('password', None)
    current_user = User.query.filter_by(username=username)
    for i in current_user:
        if check_password_hash(i.password, password):
            return jsonify(access_token=create_access_token(identity=username)), 200
    else:
        return jsonify({"Error": "Wrong password"}), 401


@app.route('/user/logout', methods=['GET'])
def user_logout():
    return ''


@app.route('/userstats/<user_id>', methods=['GET'])
def get_userstats_by_id(user_id):
    return ''
