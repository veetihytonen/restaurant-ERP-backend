from flask import request
from flask.blueprints import Blueprint
from services.stock_service import StockService
from http import HTTPMethod, HTTPStatus


def make_stock_router(service: StockService):
    router = Blueprint('stock_update_router', __name__)
    
    @router.route('/', methods=[HTTPMethod.GET])
    def get_all_stock_levels() -> tuple[list[dict], HTTPStatus]:
        results = service.get_all_stock_levels()

        return results, HTTPStatus.OK
    
    @router.route('/<ingredient_id>', methods=[HTTPMethod.GET])
    def get_stock_level_by_id(ingredient_id: int) -> tuple[dict, HTTPStatus]:
        results = service.get_stock_level_by_id(ingredient_id)

        return results, HTTPStatus.OK

    @router.route('/warehouse-replenishments', methods=[HTTPMethod.GET])
    def get_warehouse_replenishments() -> tuple[list[dict[int, str]], HTTPStatus]:
        results = service.get_warehouse_replenishments()

        return results, HTTPStatus.OK

    @router.route('/warehouse-replenishments', methods=[HTTPMethod.POST])
    def create_warehouse_replenishment() -> tuple[dict[int, str], HTTPStatus]:
        data = request.get_json()
        vendor_name, replenishments = data['vendor_name'], data['replenishments']

        result = service.create_warehouse_replenishment(vendor_name=vendor_name, replenishments=replenishments)

        return result, HTTPStatus.CREATED
    
    @router.route('/ingredient-replenishments', methods=[HTTPMethod.GET])
    def get_ingredient_replenishments() -> tuple[list[dict[int, str]], HTTPStatus]:
        results = service.get_ingredient_replenishments()

        return results, HTTPStatus.OK
    
    @router.route('/ingredient-replenishments/<replenishment_id>', methods=[HTTPMethod.GET])
    def get_ingredient_replenishment_by_id(replenishment_id: int) -> tuple[dict, HTTPStatus]:
        result = service.get_ingredient_replenishment_by_id(replenishment_id)

        return result, HTTPStatus.OK
    
    @router.route('/ingredient-replenishments/replenishment/<wh_replenishment_id>', methods=[HTTPMethod.GET])
    def get_ingredient_replenishments_by_wh_replenishment_id(wh_replenishment_id: int) -> tuple[list[dict], HTTPStatus]:
        results = service.get_ingredient_replenishments_by_wh_replenishment_id(wh_replenishment_id)

        return results, HTTPStatus.OK

    return router
