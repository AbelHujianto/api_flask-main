from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity

protected_endpoints = Blueprint('data_protected', __name__)

@protected_endpoints.route('/data', methods=['GET'])
@jwt_required()
def get_data():
    """
    Routes for demonstrating protected data endpoints,
    needs JWT to visit this endpoint.
    """
    current_user = get_jwt_identity()  # Ini mengembalikan identitas yang di-set saat membuat token, mungkin username atau id pengguna
    claims = get_jwt()  # Ini mengembalikan seluruh payload JWT
    roles = claims.get('roles', 'umum')
    user_id = claims.get('id_user')  # Ambil id_user dari claims

    if not user_id:
        return jsonify({"error": "User ID not found in token."}), 400

    return jsonify({"message": "OK",
                    "user_logged": user_id,
                    "roles": roles}), 200
