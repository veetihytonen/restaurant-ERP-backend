from flask import request
from flask.blueprints import Blueprint
from services.product_service import ProductService
from http import HTTPMethod, HTTPStatus
from utils import check_csrf, check_auth

def make_purchase_router(service: ProductService) -> Blueprint:
    router = Blueprint('product_router', __name__)

    @router.route('/', methods=[HTTPMethod.POST])
    def create_purchase():
        auth = check_auth(access_level=0)
        if not auth[0]:
            return auth[1], HTTPStatus.UNAUTHORIZED
        
        