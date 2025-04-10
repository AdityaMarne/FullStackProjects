from flask import Flask
from config import Config
from models import db
from routes import api
from flask_cors import CORS
from flask_migrate import Migrate

app = Flask(__name__)
CORS(app)
migrate = Migrate(app, db)
app.config.from_object(Config)
db.init_app(app)

app.register_blueprint(api)

if __name__ == "__main__":
    app.run(debug=True)


