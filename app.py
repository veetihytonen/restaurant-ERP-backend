from flask import Flask
from config import SECRET_KEY

from daos.user_dao import UserDao
from daos.ingredient_dao import IngredientDao
from daos.stock_dao import StockDao

from services.user_service import UserService
from services.ingredient_service import IngredientService
from services.stock_service import StockService

app = Flask(__name__)
app.secret_key = SECRET_KEY
from init_db import init_db

from routes.puclic_router import make_public_router
from routes.ingredient_router import make_ingredient_router
from routes.stock_router import make_stock_router
from routes.replenishment_router import make_replenishment_router

init_db()

from db import db

user_dao = UserDao(db_connection=db)
user_service = UserService(dao=user_dao)
public_router = make_public_router(service=user_service)

app.register_blueprint(public_router, url_prefix='/')

ingredient_dao = IngredientDao(db_connection=db)
ingrendient_service = IngredientService(dao=ingredient_dao)
ingredient_router = make_ingredient_router(service=ingrendient_service)

app.register_blueprint(ingredient_router, url_prefix='/ingredients')

stock_dao = StockDao(db_connection=db)
stock_service = StockService(dao=stock_dao)
stock_router = make_stock_router(service=stock_service)
replenishment_router = make_replenishment_router(stock_service=stock_service, ingredient_service=ingrendient_service)

app.register_blueprint(stock_router, url_prefix='/stock')
app.register_blueprint(replenishment_router, url_prefix='/replenishments')
