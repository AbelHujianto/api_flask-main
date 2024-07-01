from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token, decode_token
from flask_bcrypt import Bcrypt

from db_helper import get_connection

bcrypt = Bcrypt()
auth_endpoints = Blueprint('auth', __name__)

@auth_endpoints.route('/login', methods=['POST'])
def login():
    """Routes for authentication"""
    if request.content_type == 'application/json':
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
    else:
        username = request.form.get('username')
        password = request.form.get('password')

    if not username or not password:
        return jsonify({"msg": "Username and password are required"}), 400

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    query = "SELECT * FROM users WHERE username = %s AND deleted_at IS NULL"
    request_query = (username,)
    cursor.execute(query, request_query)
    user = cursor.fetchone()
    cursor.close()

    if not user or not bcrypt.check_password_hash(user.get('password'), password):
        return jsonify({"msg": "Bad username or password"}), 401

    access_token = create_access_token(
        identity={'username': username},
        additional_claims={'roles': user.get('roles'), 'id_user': user.get('id_user')}
    )
    decoded_token = decode_token(access_token)
    expires = decoded_token['exp']
    return jsonify({"access_token": access_token, "expires_in": expires, "type": "Bearer"}), 200

@auth_endpoints.route('/register', methods=['POST'])
def register():
    """Routes for register"""
    if request.content_type == 'application/json':
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        roles = data.get('roles', 'umum')  # default role is 'umum' if not provided
    else:
        username = request.form.get('username')
        password = request.form.get('password')
        roles = request.form.get('roles', 'umum')  # default role is 'umum' if not provided

    if not username or not password:
        return jsonify({"msg": "Username and password are required"}), 400

    if roles not in ['umum', 'admin', 'teknisi']:
        return jsonify({"msg": "Invalid role"}), 400

    # To hash a password
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

    connection = get_connection()
    cursor = connection.cursor()
    insert_query = "INSERT INTO users (username, password, roles) values (%s, %s, %s)"
    request_insert = (username, hashed_password, roles)
    cursor.execute(insert_query, request_insert)
    connection.commit()
    new_id = cursor.lastrowid
    cursor.close()
    if new_id:
        return jsonify({"username": username,
                        "password": password }), 201
    return jsonify({"message": "Failed, can't register user"}), 501
