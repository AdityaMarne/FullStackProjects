from flask import Flask
from flask_cors import CORS
from routes.notes import notes_db
app = Flask(__name__)
CORS(app)

app.register_blueprint(notes_db)

if __name__ == "__main__":
    app.run(debug=True)

