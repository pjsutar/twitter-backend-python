from flask import Blueprint, jsonify, abort, request
from ..models import Tweet, User, db

import hashlib
import secrets


def scramble(password: str):
    """Hash and salt the given password"""
    salt = secrets.token_hex(16)
    return hashlib.sha512((password + salt).encode('utf-8')).hexdigest()


# Blueprint
bp = Blueprint('users', __name__, url_prefix='/users')


# Index Users Endpoint
@bp.route('', methods=['GET'])  # decorator takes path and list of HTTP verbs
def index():
    users = User.query.all()  # ORM performs SELECT query
    result = []
    for t in users:
        result.append(t.serialize())  # build list of Users as dictionaries
    return jsonify(result)  # return JSON response


# Show Users Endpoint
@bp.route('/<int:id>', methods=['GET'])
def show(id: int):
    t = User.query.get_or_404(id)
    return jsonify(t.serialize())


# Create Tweet Endpoint
@bp.route('', methods=['POST'])
def create():
    # Username must be 3 char or longer and password must be 8 char or longer
    if len(request.json['username']) < 3 and len(request.json['password']) < 8:
        return abort(400)

    # construct User
    t = User(
        username=request.json['username'],
        password=scramble(request.json['password'])
    )
    db.session.add(t)  # prepare CREATE statement
    db.session.commit()  # execute CREATE statement
    return jsonify(t.serialize())


# Delete Tweet Endpoint
@bp.route('/<int:id>', methods=['DELETE'])
def delete(id: int):
    t = User.query.get_or_404(id)
    try:
        db.session.delete(t)  # prepare DELETE statement
        db.session.commit()  # execute DELETE statement
        return jsonify(True)
    except:
        # something went wrong :(
        return jsonify(False)


# Update User Endpoint
@bp.route('/<int:id>', methods=['PUT'])
def update(id: int):
    t = User.query.get_or_404(id)

    # Update User
    # If username or password not in request
    if 'username' not in request.json and 'password' not in request.json:
        return abort(400)

    # If username is provided in request body
    if 'username' in request.json:
        t.username = request.json['username']

    # If password is provided in request body
    if 'password' in request.json:
        t.password = scramble(request.json['password'])

    # db.session.add(t)  # prepare CREATE statement
    db.session.commit()  # execute CREATE statement
    return jsonify(True)
