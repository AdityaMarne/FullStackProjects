from flask import Flask
from flask_jwt_extended import JWTManager
from db import app
from routes.auth import auth_bp
from routes.blog import blog_bp
from routes.comments import comments_bp
from routes.tags import tags_bp
from flask_cors import CORS

jwt = JWTManager(app)

CORS(app)  

app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(blog_bp, url_prefix='/blog')
app.register_blueprint(comments_bp, url_prefix='/comments')
app.register_blueprint(tags_bp, url_prefix='/tags')

if __name__ == '__main__':
    app.run(debug=True)

    