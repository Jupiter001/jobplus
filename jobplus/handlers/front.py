from flask import Blueprint

front = Blueprint('front', __name__, url_prefix='/front')

@front.route('/')
def index():
    return 'Front'
