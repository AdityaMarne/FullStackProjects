from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from config import Config
from db import get_db_connection
from routes.products import products_bp
# from routes.categories import categories_bp
from routes.users import users_bp
# from routes.orders import orders_bp
from db import close_db
app = Flask(__name__)
CORS(app)
app.config['JWT_SECRET_KEY'] = Config.JWT_SECRET
jwt = JWTManager(app)

app.register_blueprint(products_bp)
# app.register_blueprint(categories_bp)
app.register_blueprint(users_bp)
# app.register_blueprint(orders_bp)
app.teardown_appcontext(close_db)

if __name__ == "__main__":
    app.run(debug=True, port=5000)

