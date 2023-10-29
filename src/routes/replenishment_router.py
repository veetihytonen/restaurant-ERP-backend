from flask import request
from flask.blueprints import Blueprint
from services.stock_service import StockService
from services.ingredient_service import IngredientService
from http import HTTPMethod, HTTPStatus
from utils import check_csrf, check_auth

def make_replenishment_router(stock_service: StockService, ingredient_service: IngredientService):
    router = Blueprint('warehouse_router', __name__)
    
    @router.route('/', methods=[HTTPMethod.GET])
    def get_warehouse_replenishments():
        auth = check_auth(access_level=1)
        if not auth[0]:
            return auth[1], HTTPStatus.UNAUTHORIZED
        
        results = stock_service.get_warehouse_replenishments()

        return results, HTTPStatus.OK
    
    @router.route('/', methods=[HTTPMethod.POST])
    def create_warehouse_replenishment():
        auth = check_auth(access_level=0)
        if not auth[0]:
            return auth[1], HTTPStatus.UNAUTHORIZED
        check_csrf()

        data = request.get_json()
        vendor_name, replenishments = data['vendor_name'], data['replenishments']

        result = stock_service.create_warehouse_replenishment(vendor_name=vendor_name, replenishments=replenishments)

        return result, HTTPStatus.CREATED

    @router.route('/<wh_replenishment_id>', methods=[HTTPMethod.GET])
    def get_wh_replenishment_by_id(wh_replenishment_id: int):
        auth = check_auth(access_level=1)
        if not auth[0]:
            return auth[1], HTTPStatus.UNAUTHORIZED
        
        replenishment = stock_service.get_ingredient_replenishment_by_wh_replenishment_id(wh_replenishment_id)
        
        return replenishment, HTTPStatus.OK

    return router
