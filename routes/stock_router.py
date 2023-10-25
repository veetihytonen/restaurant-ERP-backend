from flask import request, session, render_template, redirect, flash
from flask.blueprints import Blueprint
from services.stock_service import StockService
from http import HTTPMethod
from utils import check_csrf, check_auth

def make_stock_router(service: StockService):
    router = Blueprint('stock_update_router', __name__)
    
    @router.route('/', methods=[HTTPMethod.GET])
    def get_all_stock_levels():
        auth = check_auth(access_level=1)
        if not auth[0]:
            return auth[1]
        
        stock_levels = service.get_all_stock_levels()

        return render_template('stock.html', stock_levels=stock_levels)
    
    @router.route('/<ingredient_id>', methods=[HTTPMethod.GET])
    def get_stock_level_by_id(ingredient_id: int):
        results = service.get_stock_level_by_id(ingredient_id)

    @router.route('/ingredient-replenishments', methods=[HTTPMethod.GET])
    def get_ingredient_replenishments():
        results = service.get_ingredient_replenishments()

    return router
