from flask import request
from flask.blueprints import Blueprint
from services.purchase_service import PurchaseService
from http import HTTPMethod, HTTPStatus
from utils import check_csrf, check_auth

def make_purchase_router(service: PurchaseService) -> Blueprint:
    router = Blueprint('purchase_router', __name__)

    @router.route('/', methods=[HTTPMethod.POST])
    def create_purchase():
        auth = check_auth(access_level=0)
        if not auth[0]:
            return auth[1], HTTPStatus.UNAUTHORIZED
        
        data = request.get_json()

        bought_products = data
        print(data)

        purchase = service.create_purchase(bought_products)

        return purchase, HTTPStatus.CREATED

    return router

        
        