from flask import request, session
from flask.blueprints import Blueprint
from services.stock_service import StockService
from http import HTTPMethod, HTTPStatus
from utils import check_csrf, check_auth

def make_stock_router(service: StockService):
    router = Blueprint('stock_update_router', __name__)
    
    @router.route('/', methods=[HTTPMethod.GET])
    def get_all_stock_levels() -> tuple[str | dict, HTTPStatus]:
        auth = check_auth(access_level=1)
        if not auth[0]:
            return auth[1], HTTPStatus.UNAUTHORIZED
        
        results = service.get_all_stock_levels()

        return results, HTTPStatus.OK
    
    @router.route('/<ingredient_id>', methods=[HTTPMethod.GET])
    def get_stock_level_by_id(ingredient_id: int) -> tuple[str | dict, HTTPStatus]:
        auth = check_auth(access_level=1)
        if not auth[0]:
            return auth[1], HTTPStatus.UNAUTHORIZED
        
        results = service.get_stock_level_by_id(ingredient_id)

        return results, HTTPStatus.OK
    