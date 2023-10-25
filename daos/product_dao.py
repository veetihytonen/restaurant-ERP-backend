from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

from sqlalchemy.exc import IntegrityError

class ProductDao:
    def __init__(self, db_connection: SQLAlchemy) -> None:
        self.__db = db_connection

    def get_products(self):
        sql =  """
        SELECT (
            id,
            name
        )
        FROM 
            products
        """
        
        results = self.__db.session.execute(text(sql))

        return results.fetchall()

    def create_product(self, name: str):
        sql = """
        INSERT INTO products (
            name
        )
        VALUES (
            :name
        )
        RETURNING
            id,
            name
        """

        params = {'name': name}

        try:
            result = self.__db.session.execute(text(sql), params)
            self.__db.session.commit()
        except IntegrityError:
            raise ValueError('Tuote on jo olemassa')
        
        return result.fetchone()
    



