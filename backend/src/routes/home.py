from flask import Blueprint

home_bp = Blueprint('home',__name__)

@home_bp.route('/',methods=['GET'])
def home():
    return '<h1>Welcome to our Home Page [Flask]</h1>'