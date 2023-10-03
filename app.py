from flask import Flask
from services.ingredient_service import IngredientService 
from daos.foodstock_dao import FoodstockDao

app = Flask(__name__)

from db_init import init_db

import routes.public_router as public
from routes.ingredient_router import make_ingredient_router
import routes.stock_update_router as stock_updates

init_db()

from db import db



app.register_blueprint(public.router, url_prefix='/')

foodstock_dao = FoodstockDao(db_connection=db)
ingredients_service = IngredientService(dao=foodstock_dao)
ingredient_router = make_ingredient_router(service=ingredients_service)
app.register_blueprint(ingredient_router, url_prefix='/ingredients')

app.register_blueprint(stock_updates.router, url_prefix='/stock_updates')

