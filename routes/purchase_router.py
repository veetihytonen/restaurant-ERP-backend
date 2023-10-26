from flask import request
from flask.blueprints import Blueprint
from services.purchase_service import PurchaseService
from http import HTTPMethod, HTTPStatus
from utils import check_csrf, check_auth

def make_purchase_router(service: PurchaseService) -> Blueprint:
    router = Blueprint('purchase_router', __name__)

    @router.route('/', methods=[HTTPMethod.GET])
    def get_purchases():
        auth = check_auth(access_level=1)
        if not auth[0]:
            return auth[1], HTTPStatus.UNAUTHORIZED
        
        purchases = service.get_purchases()

        return purchases, HTTPStatus.OK
    
    @router.route('/<purchase_id>', methods=[HTTPMethod.GET])
    def get_sales_by_purchase_id(purchase_id: int):
        auth = check_auth(access_level=1)
        if not auth[0]:
            return auth[1], HTTPStatus.UNAUTHORIZED

        sales = service.get_sales_by_purchase_id(purchase_id)

        return sales, HTTPStatus.OK

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
