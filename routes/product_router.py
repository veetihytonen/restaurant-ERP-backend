from flask import request
from flask.blueprints import Blueprint
from services.product_service import ProductService
from http import HTTPMethod, HTTPStatus
from utils import check_csrf, check_auth

def make_ingredient_router(service: ProductService) -> Blueprint:
    router = Blueprint('product_router', __name__)

    @router.route('/', methods=[HTTPMethod.GET])
    def get_products():
        auth = check_auth(access_level=1)
        if not auth[0]:
            return auth[1], HTTPStatus.UNAUTHORIZED

        products = service.get_products()

        return products, HTTPStatus.OK
    
    @router.route('/', methods=[HTTPMethod.POST])
    def create_product():
        auth = check_auth(access_level=1)
        if not auth[0]:
            return auth[1], HTTPStatus.UNAUTHORIZED
        check_csrf()

        data = request.get_json()
        name = data['name']

        try:
            product = service.create_product(name)
        except ValueError as error:
            return error.args[0], HTTPStatus.CONFLICT
        
        return product, HTTPStatus.CREATED



