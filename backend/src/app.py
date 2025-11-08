from flask import Flask
from flask_cors import CORS
from routes.home import home_bp
from routes.api import api_bp

app = Flask(__name__)
CORS(app)

app.register_blueprint(home_bp)
app.register_blueprint(api_bp)


app.run(port=5000,debug=True)