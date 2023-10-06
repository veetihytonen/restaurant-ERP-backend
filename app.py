from flask import Flask

from daos.ingredient_dao import IngredientDao
from daos.stock_dao import StockDao

from services.ingredient_service import IngredientService
from services.stock_service import StockService

app = Flask(__name__)

from db_init import init_db

import routes.public_router as public
from routes.ingredient_router import make_ingredient_router
from routes.stock_router import make_stock_router

init_db()

from db import db

app.register_blueprint(public.router, url_prefix='/')

ingredient_dao = IngredientDao(db_connection=db)
ingrendient_service = IngredientService(dao=ingredient_dao)
ingredient_router = make_ingredient_router(service=ingrendient_service)
app.register_blueprint(ingredient_router, url_prefix='/ingredients')

stock_dao = StockDao(db_connection=db)
stock_service = StockService(dao=stock_dao)
stock_router = make_stock_router(service=stock_service)
app.register_blueprint(stock_router, url_prefix='/stock')
