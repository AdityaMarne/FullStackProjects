from flask import Flask
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from auth.routes import auth_bp
import os
from dotenv import load_dotenv
from auth.routes import google_bp, github_bp

load_dotenv()

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
CORS(app)
JWTManager(app)

app.register_blueprint(auth_bp, url_prefix="/auth")
app.register_blueprint(google_bp, url_prefix="/login")
app.register_blueprint(github_bp, url_prefix="/login")

if __name__ == "__main__":
    app.run(debug=True)
