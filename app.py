from flask import Flask
from flask_jwt_extended import JWTManager
from endpoints.service_request import service_requests_endpoints
from endpoints.consultation import consultation_endpoints
from endpoints.auth import auth_endpoints
from endpoints.teknisi import teknisi_endpoints
from endpoints.data_protected import protected_endpoints

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'your-secret-key'  # Gantilah "your-secret-key" dengan kunci rahasia Anda

# Inisialisasi JWTManager
jwt = JWTManager(app)

# Daftarkan blueprint
app.register_blueprint(service_requests_endpoints)
app.register_blueprint(consultation_endpoints)
app.register_blueprint(auth_endpoints, name='auth')
app.register_blueprint(teknisi_endpoints)
app.register_blueprint(protected_endpoints)

if __name__ == '__main__':
    app.run(debug=True)