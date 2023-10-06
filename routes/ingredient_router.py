from flask import request
from flask.blueprints import Blueprint
from services.ingredient_service import IngredientService
from http import HTTPMethod, HTTPStatus

def make_ingredient_router(service: IngredientService) -> Blueprint:
    router = Blueprint('ingredients_router', __name__)

    @router.route('/', methods=[HTTPMethod.GET])
    def get_ingredients() -> tuple[dict, HTTPStatus]:
        result = service.get_all()
        
        return result, HTTPStatus.OK

    @router.route('/', methods=[HTTPMethod.POST])
    def create_ingredient() -> tuple[dict[int, str, str], HTTPStatus]:
        data = request.get_json()
        name, category = data['name'], data['storage_category']

        result = service.create(name=name, category=category)

        return result, HTTPStatus.CREATED
        
    @router.route('/<ingredient_id>', methods=[HTTPMethod.GET])
    def get_ingredient_by_id(ingredient_id: int) -> tuple[dict[int, str, str], HTTPStatus]:
        result = service.get_by_id(ingredient_id)

        return result, HTTPStatus.OK

    return router
