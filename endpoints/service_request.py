import os
from flask import Blueprint, jsonify, request
from form_validation import get_form_data
from db_helper import get_connection

service_requests_endpoints =Blueprint('service', __name__)

@service_requests_endpoints.route('/read_service_request',methods=['GET'])
def read():
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    select_query = "SELECT * FROM service_request"
    cursor.execute(select_query)
    results = cursor.fetchall()
    cursor.close()  # Close the cursor after query execution
    return jsonify({"message": "OK", "datas": results}), 200


@service_requests_endpoints.route('/create_service_request', methods=['POST'])
def create_service_request():
    """Route to create a service request"""
    try:
        # Mengambil data dari request
        data = request.get_json()
        required_fields = ["id_user", "tanggal_service", "judul", "deskripsi", "serial_number", "brand", "model"]
        
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            return jsonify({"err_message": f"Missing required field(s): {', '.join(missing_fields)}"}), 400

        id_user = data["id_user"]
        tanggal_service = data["tanggal_service"]
        judul = data["judul"]
        deskripsi = data["deskripsi"]
        serial_number = data["serial_number"]
        brand = data["brand"]
        model = data["model"]

        connection = get_connection()
        cursor = connection.cursor()
        
        insert_query = """
            INSERT INTO service_request (id_user, tanggal_service, judul, deskripsi, serial_number, brand, model)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        request_insert = (id_user, tanggal_service, judul, deskripsi, serial_number, brand, model)
        cursor.execute(insert_query, request_insert)
        connection.commit()
        new_id = cursor.lastrowid
        
        cursor.close()
        connection.close()
        
        if new_id:
            return jsonify({"message": "Inserted", "service_request_id": new_id}), 201
        return jsonify({"message": "Can't Insert Data"}), 500

    except Exception as e:
        return jsonify({"message": str(e)}), 500
    
@service_requests_endpoints.route('/delete_service_request/<int:id_request>', methods=['DELETE'])
def delete_service_request(id_request):
    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        query = "DELETE FROM service_request WHERE id_request = %s"
        values = (id_request,)

        cursor.execute(query, values)
        connection.commit()

        cursor.close()
        connection.close()

        if cursor.rowcount > 0:
            return jsonify({"message": "Data service request berhasil dihapus"}), 200
        else:
            return jsonify({"message": "Data service request dengan ID tersebut tidak ditemukan"}), 404

    except Exception as e:
        return jsonify({"message": str(e)}), 500
    
@service_requests_endpoints.route('/update_service_request/<int:id_request>', methods=['PUT'])
def update_service_request(id_request):
    try:
        judul = request.json.get('judul')
        deskripsi = request.json.get('deskripsi')
        serial_number = request.json.get('serial_number')
        brand = request.json.get('brand')
        model = request.json.get('model')
        tanggal_service = request.json.get('tanggal_service')
        status = request.json.get('status')

        # Check if all required fields are present
        if not all([judul, deskripsi, serial_number, brand, model, tanggal_service, status]):
            return jsonify({"message": "Missing required fields"}), 400

        # Validate status
        if status not in ['belum diservice', 'diproses', 'selesai']:
            return jsonify({"message": "Invalid status value"}), 400

        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        query = """
        UPDATE service_request 
        SET judul = %s, deskripsi = %s, serial_number = %s, brand = %s, model = %s, tanggal_service = %s, status = %s
        WHERE id_request = %s
        """
        values = (judul, deskripsi, serial_number, brand, model, tanggal_service, status, id_request)

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