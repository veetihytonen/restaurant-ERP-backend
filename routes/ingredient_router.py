from flask import request
from flask.blueprints import Blueprint
from services.ingredient_service import IngredientService

def make_ingredient_router(service: IngredientService) -> Blueprint:
    router = Blueprint('ingredients_router', __name__)
    service = service

    @router.route('/', methods=['get'])
    def get_ingredients() -> tuple[dict, int]:
        result = service.get_all()
        
        return result, 200
        
    @router.route('/', methods=['post'])
    def create_ingredient() -> tuple[dict[int, str, str], int]:
        data = request.get_json()
        name, category = data['name'], data['storage_category']

        result = service.create(name=name, category=category)

        return result, 201
        
    @router.route('/<ingredient_id>', methods=['get'])
    def get_ingredient_by_id(ingredient_id: int) -> tuple[dict[int, str, str], int]:
        result = service.get_by_id(ingredient_id)

        return result, 200

    return router
