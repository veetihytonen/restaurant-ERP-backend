from flask import request
from flask.blueprints import Blueprint
from services.product_service import ProductService
from http import HTTPMethod, HTTPStatus
from utils import check_csrf, check_auth

def make_product_router(service: ProductService) -> Blueprint:
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
    
    @router.route('/<product_id>', methods=[HTTPMethod.GET])
    def get_product_by_id(product_id: int):
        auth = check_auth(access_level=1)
        if not auth[0]:
            return auth[1], HTTPStatus.UNAUTHORIZED

        product = service.get_product_by_id(product_id)

        return product, HTTPStatus.OK
    
    @router.route('/<product_id>/versions', methods=[HTTPMethod.GET])
    def get_versions_for_product(product_id: int):
        auth = check_auth(access_level=1)
        if not auth[0]:
            return auth[1], HTTPStatus.UNAUTHORIZED

        versions = service.get_versions_for_product(product_id)

        return versions, HTTPStatus.OK

    @router.route('<product_id>/versions', methods=[HTTPMethod.POST])
    def create_product_version(product_id: int):
        auth = check_auth(access_level=1)
        if not auth[0]:
            return auth[1], HTTPStatus.UNAUTHORIZED
        check_csrf()
        
        data = request.get_json()

        sale_price = data['sale_price']
        ingredients_and_amounts = data['ingredients_and_amounts']

        product_version = service.create_product_version(
            sale_price=sale_price,
            product_id=product_id, 
            ingredients_and_amounts=ingredients_and_amounts
        )

        return product_version, HTTPStatus.CREATED
    
    @router.route('/<product_id>/versions/<version_number>', methods=[HTTPMethod.GET])
    def get_version_by_number(product_id: int, version_number: int):
        auth = check_auth(access_level=1)
        if not auth[0]:
            return auth[1], HTTPStatus.UNAUTHORIZED

        product = service.get_version_by_number(version_number=version_number, product_id=product_id)

        return product, HTTPStatus.OK

    return router