from flask import request, session, render_template, redirect, flash
from flask.blueprints import Blueprint
from services.stock_service import StockService
from services.ingredient_service import IngredientService
from http import HTTPMethod
from utils import check_csrf, check_auth

def make_warehouse_router(stock_service: StockService, ingredient_service: IngredientService):
    router = Blueprint('warehouse_router', __name__)
    
    @router.route('/', methods=[HTTPMethod.GET])
    def get_warehouse_replenishments():
        auth = check_auth(access_level=0)
        if not auth[0]:
            return auth[1]

        replenishments = stock_service.get_warehouse_replenishments()
        ingredients = ingredient_service.get_all()

        return render_template('replenishments.html', replenishments=replenishments, ingredients=ingredients)
    
    @router.route('/', methods=[HTTPMethod.POST])
    def create_warehouse_replenishment() :
        auth = check_auth(access_level=0)
        if not auth[0]:
            return auth[1]
        check_csrf()

        vendor = request.form['vendor']
        ingr_ids = request.form.getlist('ingredient[]')
        ingr_amounts = request.form.getlist('amount[]')
        ingr_prices = request.form.getlist('price[]')

        replenishments = [{
            'ingredient_id': ingr_ids[i],
            'amount': ingr_amounts[i],
            'price_per_unit': ingr_prices[i]
        } for i, _ in enumerate(ingr_ids)]
        
        stock_service.create_warehouse_replenishment(vendor_name=vendor, replenishments=replenishments)

        flash('Toimitus kirjattiin', 'notification')
        return redirect('/replenishments')

    @router.route('/<wh_replenishment_id>', methods=[HTTPMethod.GET])
    def get_replenishment_by_id(wh_replenishment_id: int):
        auth = check_auth(access_level=0)
        if not auth[0]:
            return auth[1]
        
        replenishment = stock_service.get_ingredient_replenishments_by_wh_replenishment_id(wh_replenishment_id)
        
        return render_template('replenishment_by_id.html', replenishment_id=wh_replenishment_id, replenishment=replenishment)

    return router
