from flask import Flask
from config import SECRET_KEY

from daos.user_dao import UserDao
from daos.ingredient_dao import IngredientDao
from daos.stock_dao import StockDao
from daos.product_dao import ProductDao
from daos.purchase_dao import PurchaseDao

from services.user_service import UserService
from services.ingredient_service import IngredientService
from services.stock_service import StockService
from services.product_service import ProductService
from services.purchase_service import PurchaseService

app = Flask(__name__)
app.secret_key = SECRET_KEY

from routes.public_router import make_public_router
from routes.ingredient_router import make_ingredient_router
from routes.stock_router import make_stock_router
from routes.replenishment_router import make_replenishment_router
from routes.product_router import make_product_router
from routes.purchase_router import make_purchase_router

from db import db

user_dao = UserDao(db_connection=db)
user_service = UserService(dao=user_dao)
public_router = make_public_router(service=user_service)

app.register_blueprint(public_router, url_prefix='/')

ingredient_dao = IngredientDao(db_connection=db)
ingredient_service = IngredientService(dao=ingredient_dao)
ingredient_router = make_ingredient_router(service=ingredient_service)

app.register_blueprint(ingredient_router, url_prefix='/ingredients')

stock_dao = StockDao(db_connection=db)
stock_service = StockService(dao=stock_dao)
stock_router = make_stock_router(service=stock_service)
replenishment_router = make_replenishment_router(stock_service=stock_service, ingredient_service=ingredient_service)

app.register_blueprint(stock_router, url_prefix='/stock')
app.register_blueprint(replenishment_router, url_prefix='/replenishments')

prodcut_dao = ProductDao(db_connection=db)
product_service = ProductService(dao=prodcut_dao)
product_router = make_product_router(service=product_service)

app.register_blueprint(product_router, url_prefix='/products')

purchase_dao = PurchaseDao(db_connection=db)
purchase_service = PurchaseService(dao=purchase_dao)
purchase_router = make_purchase_router(service=purchase_service)

app.register_blueprint(purchase_router, url_prefix='/purchases')
