from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = '2F4A8B8690219C1841B865EB87E8EC40281F7784BA16AEF0408DC712A6F3B4D3'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://{user}:{password}@{server}/{database}'.format(
    user='root',
    password='root',
    server='localhost',
    database='Swaggerdb'
)

jwt = JWTManager(app)
db = SQLAlchemy(app)
engine = db.engine
Base = db.Model
jwt = JWTManager(app)

