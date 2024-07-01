import os
from flask import Blueprint, jsonify, request
from form_validation import get_form_data
from db_helper import get_connection

consultation_endpoints = Blueprint('consultation', __name__)

@consultation_endpoints.route('/read_consultation', methods=['GET'])
def read():
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    select_query = "SELECT * FROM consultation"
    cursor.execute(select_query)
    results = cursor.fetchall()
    cursor.close()  # Close the cursor after query execution
    return jsonify({"message": "OK", "datas": results}), 200

@consultation_endpoints.route('/create_consultation', methods=['POST'])
def create_consultation():
    """Route to create a consultation"""
    try:
        # Mengambil data dari request
        data = request.get_json()
        required_fields = ["id_admin", "id_request", "id_user", "judul", "deskripsi"]
        
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            return jsonify({"err_message": f"Missing required field(s): {', '.join(missing_fields)}"}), 400

        id_admin = data["id_admin"]
        id_request = data["id_request"]
        id_user = data["id_user"]
        judul = data["judul"]
        deskripsi = data["deskripsi"]

        connection = get_connection()
        cursor = connection.cursor()
        
        insert_query = """
            INSERT INTO consultation (id_admin, id_request, id_user, judul, deskripsi)
            VALUES (%s, %s, %s, %s, %s)
        """
        consultation_insert = (id_admin, id_request, id_user, judul, deskripsi)
        cursor.execute(insert_query, consultation_insert)
        connection.commit()
        new_id = cursor.lastrowid
        
        cursor.close()
        connection.close()
        
        if new_id:
            return jsonify({"message": "Inserted", "consultation_id": new_id}), 201
        return jsonify({"message": "Can't Insert Data"}), 500

    except Exception as e:
        return jsonify({"message": str(e)}), 500
    
@consultation_endpoints.route('/delete_consultation/<int:id_konsultasi>', methods=['DELETE'])
def delete_consultation(id_konsultasi):
    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        query = "DELETE FROM consultation WHERE id_konsultasi = %s"
        values = (id_konsultasi,)

        cursor.execute(query, values)
        connection.commit()

        cursor.close()
        connection.close()

        if cursor.rowcount > 0:
            return jsonify({"message": "Data consultation berhasil dihapus"}), 200
        else:
            return jsonify({"message": "Data consultation dengan ID tersebut tidak ditemukan"}), 404

    except Exception as e:
        return jsonify({"message": str(e)}), 500
    
@consultation_endpoints.route('/update_consultation/<int:id_konsultasi>', methods=['PUT'])
def update_consultation(id_konsultasi):
    try:
        judul = request.json.get('judul')
        deskripsi = request.json.get('deskripsi')
        id_admin = request.json.get('id_admin')
        id_request = request.json.get('id_request')
        id_user = request.json.get('id_user')

        if not all([judul, deskripsi, id_admin, id_request, id_user]):
            return jsonify({"message": "Missing required fields"}), 400

        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        query = """
        UPDATE consultation 
        SET judul = %s, deskripsi = %s, id_admin = %s, id_request = %s, id_user = %s
        WHERE id_konsultasi = %s
        """
        values = (judul, deskripsi, id_admin, id_request, id_user, id_konsultasi)

        cursor.execute(query, values)
        connection.commit()

        if cursor.rowcount > 0:
            success = True
        else:
            success = False
        cursor.close()
        connection.close()

        if success:
            return jsonify({"message": "Updated"}), 200
        return jsonify({"message": "Cannot update data"}), 500

    except Exception as e:
        return jsonify({"message": str(e)}), 500
