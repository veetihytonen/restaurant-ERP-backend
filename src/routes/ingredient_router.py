from flask import request
from flask.blueprints import Blueprint
from services.ingredient_service import IngredientService
from http import HTTPMethod, HTTPStatus
from utils import check_csrf, check_auth

def make_ingredient_router(service: IngredientService) -> Blueprint:
    router = Blueprint('ingredients_router', __name__)

    @router.route('/', methods=[HTTPMethod.GET])
    def get_ingredients():
        auth = check_auth(access_level=1)
        if not auth[0]:
            return auth[1], HTTPStatus.UNAUTHORIZED
        
        result = service.get_all()
        
        return result, HTTPStatus.OK

    @router.route('/', methods=[HTTPMethod.POST])
    def create_ingredient():
        auth = check_auth(access_level=1)
        if not auth[0]:
            return auth[1], HTTPStatus.UNAUTHORIZED
        check_csrf()

        data = request.get_json()
        name, category = data['name'], data['storage_category']
        
        try:
            result = service.create(name=name, category=category)
        except ValueError as ve:
            return ve.args[0], HTTPStatus.CONFLICT

        return result, HTTPStatus.CREATED
        
    @router.route('/<ingredient_id>', methods=[HTTPMethod.GET])
    def get_ingredient_by_id(ingredient_id: int):
        auth = check_auth(access_level=1)
        if not auth[0]:
            return auth[1], HTTPStatus.UNAUTHORIZED

        result = service.get_by_id(ingredient_id)

        return result, HTTPStatus.OK

    return router
