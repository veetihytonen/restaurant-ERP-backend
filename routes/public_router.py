from flask import request
from flask.blueprints import Blueprint

router = Blueprint("public_router", __name__)

@router.route('/')
def index():
    return '<p>brr</p>'
