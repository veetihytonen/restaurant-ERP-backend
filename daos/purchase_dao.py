from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

class PurchaseDao:
    def __init__(self, db_connection: SQLAlchemy) -> None:
        self.__db = db_connection

        
