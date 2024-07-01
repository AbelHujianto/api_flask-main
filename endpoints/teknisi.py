import os
from flask import Blueprint, jsonify, request
from form_validation import get_form_data
from db_helper import get_connection

teknisi_endpoints = Blueprint('teknisi', __name__)

@teknisi_endpoints.route('/read_teknisi', methods=['GET'])
def read_teknisi():
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    select_query = "SELECT * FROM teknisi"
    cursor.execute(select_query)
    results = cursor.fetchall()
    cursor.close()  # Close the cursor after query execution
    return jsonify({"message": "OK", "datas": results}), 200

@teknisi_endpoints.route('/read_teknisibyID', methods=['GET'])
def read_teknisi_by_ID():
    id_user = request.args.get('id_user')  # Get id_user from the request parameters
    if not id_user:
        return jsonify({"message": "id_user is required"}), 400

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    
    select_query = "SELECT * FROM teknisi WHERE id_user = %s"
    cursor.execute(select_query, (id_user,))
    
    results = cursor.fetchall()
    cursor.close()  # Close the cursor after query execution
    
    return jsonify({"message": "OK", "datas": results}), 200


@teknisi_endpoints.route('/create_teknisi', methods=['POST'])
def create_teknisi():
    """Route to create a teknisi"""
    try:
        # Mengambil data dari request
        data = request.get_json()
        required_fields = ["id_konsultasi", "id_user", "id_request", "judul", "deskripsi"]
        
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            return jsonify({"err_message": f"Missing required field(s): {', '.join(missing_fields)}"}), 400

        id_konsultasi = data["id_konsultasi"]
        id_user = data["id_user"]
        id_request = data["id_request"]
        judul = data["judul"]
        deskripsi = data["deskripsi"]

        connection = get_connection()
        cursor = connection.cursor()
        
        insert_query = """
            INSERT INTO teknisi (id_konsultasi, id_user, id_request, judul, deskripsi)
            VALUES (%s, %s, %s, %s, %s)
        """
        teknisi_insert = (id_konsultasi, id_user, id_request, judul, deskripsi)
        cursor.execute(insert_query, teknisi_insert)
        connection.commit()
        new_id = cursor.lastrowid
        
        cursor.close()
        connection.close()
        
        if new_id:
            return jsonify({"message": "Inserted", "teknisi_id": new_id}), 201
        return jsonify({"message": "Can't Insert Data"}), 500

    except Exception as e:
        return jsonify({"message": str(e)}), 500
    
@teknisi_endpoints.route('/delete_teknisi/<int:id_teknisi>', methods=['DELETE'])
def delete_teknisi(id_teknisi):
    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        query = "DELETE FROM teknisi WHERE id_teknisi = %s"
        values = (id_teknisi,)

        cursor.execute(query, values)
        connection.commit()

        cursor.close()
        connection.close()

        if cursor.rowcount > 0:
            return jsonify({"message": "Data teknisi berhasil dihapus"}), 200
        else:
            return jsonify({"message": "Data teknisi dengan ID tersebut tidak ditemukan"}), 404

    except Exception as e:
        return jsonify({"message": str(e)}), 500
    
@teknisi_endpoints.route('/update_teknisi/<int:id_teknisi>', methods=['PUT'])
def update_teknisi(id_teknisi):
    try:
        id_konsultasi = request.json.get('id_konsultasi')
        id_user = request.json.get('id_user')
        id_request = request.json.get('id_request')
        judul = request.json.get('judul')
        deskripsi = request.json.get('deskripsi')

        if not all([id_konsultasi, id_user, id_request, judul, deskripsi]):
            return jsonify({"message": "Missing required fields"}), 400

        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        query = """
        UPDATE teknisi 
        SET id_konsultasi = %s, id_user = %s, id_request = %s, judul = %s, deskripsi = %s
        WHERE id_teknisi = %s
        """
        values = (id_konsultasi, id_user, id_request, judul, deskripsi, id_teknisi)

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
