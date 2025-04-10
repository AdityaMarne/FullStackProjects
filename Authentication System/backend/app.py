from flask import Flask
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from auth.routes import auth_bp
import os
from dotenv import load_dotenv

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
CORS(app)
JWTManager(app)

app.register_blueprint(auth_bp, url_prefix = "/auth")

if __name__ == "__main__":
    app.run(debug=True)
