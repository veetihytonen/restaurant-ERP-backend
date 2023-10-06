from flask import request
from flask.blueprints import Blueprint
from services.stock_service import StockService
from http import HTTPMethod, HTTPStatus


def make_stock_router(service: StockService):
    router = Blueprint('stock_update_router', __name__)

    @router.route('/replenishments', methods=[HTTPMethod.GET])
    def get_warehouse_replenishments() -> tuple[list[dict[int, str]], HTTPStatus]:
        results = service.get_warehouse_replenishments()

        return results, HTTPStatus.OK

    @router.route('/replenishments', methods=[HTTPMethod.POST])
    def create_warehouse_replenishment() -> tuple[dict[int, str], HTTPStatus]:
        data = request.get_json()
        vendor_name, replenishments = data['vendor_name'], data['replenishments']

        result = service.create_warehouse_replenishment(vendor_name=vendor_name, replenishments=replenishments)

        return result, HTTPStatus.CREATED
    
    return router
    