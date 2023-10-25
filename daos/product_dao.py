from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

from sqlalchemy.exc import IntegrityError

class ProductDao:
    def __init__(self, db_connection: SQLAlchemy) -> None:
        self.__db = db_connection

    def get_products(self):
        sql =  """
        SELECT
            id,
            name
        FROM 
            products
        """
        
        results = self.__db.session.execute(text(sql))

        return results.fetchall()
    
    def get_prodcut_by_id(self, product_id: int):
        sql =  """
        SELECT
            id,
            name
        FROM 
            products
        WHERE
            id = :id
        """

        params = {'id': product_id}

        results = self.__db.session.execute(text(sql), params)

        return results.fetchone()

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
    
    def get_versions_for_product(self, product_id: int):
        sql = """
        SELECT 
            id,
            sale_price,
            product_id
        FROM
            product_versions
        WHERE
            product_id = :product_id
        """

        params = {'product_id': product_id}

        versions = self.__db.session.execute(text(sql), params)
        
        return versions.fetchall()
    
    def get_version_by_number(self, product_id: int, version_number: int):
        sql =  """
        SELECT
            id,
            version_number,
            sale_price,
            product_id
        FROM 
            product_versions
        WHERE
            product_id = :product_id
        AND 
            version_number = :version_number
        """

        params = {'product_id': product_id, 'version_number': version_number}

        version = self.__db.session.execute(text(sql), params)

        return version.fetchone()
    
    def create_product_version(
        self, 
        sale_price: int, 
        product_id: int, 
        ingredients_and_amounts: list[dict[int, float]]
    ):
        sql = """
        SELECT
            COUNT(id)+1
        FROM
            product_versions
        WHERE
            product_id = :product_id
        """

        params = {'product_id': product_id}

        result = self.__db.session.execute(text(sql), params).fetchone()
        version_number = result[0]

        sql = """
        INSERT INTO product_versions (
            version_number,
            sale_price,
            product_id
        )
        VALUES (
            :version_number,
            :sale_price,
            :product_id
        )
        RETURNING 
            id,
            version_number,
            sale_price,
            product_id
        """
        params = {'version_number': version_number, 'sale_price': sale_price, 'product_id': product_id}

        product_version = self.__db.session.execute(text(sql), params).fetchone()
        version_id = product_version[0]

        sql = """
        INSERT INTO product_ingredient_mapping (
            product_version_id,
            ingredient_id,
            amount
        )
        VALUES (
            :version_id,
            :ingredient_id,
            :amount
        )
        """
        
        params = [
            {
                'version_id': version_id,
                'ingredient_id': entry['ingredient_id'],
                'amount': entry['amount']
            }
            for entry in ingredients_and_amounts
        ]

        self.__db.session.execute(text(sql), params)
        self.__db.session.commit()

        return product_version
