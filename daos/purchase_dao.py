from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

class PurchaseDao:
    def __init__(self, db_connection: SQLAlchemy) -> None:
        self.__db = db_connection
    
    def create_purchase(self, bought_products: list[dict[int, int]]):
        purchase = """
            INSERT INTO purchases (
                customer_id
            )
            VALUES (
                NULL
            )
            RETURNING
                id,
                customer_id
        """

        purchase = self.__db.session.execute(text(purchase)).fetchone()
        purchase_id = purchase[0]

        create_product_sale = """
        INSERT INTO product_sales (
            purchase_id,
            product_version_id,
            amount
        )
        VALUES (
            :purchase_id,
            (SELECT
                id
            FROM
                product_versions
            WHERE 
                version_number = (
                    SELECT 
                        MAX(version_number)
                    FROM
                        product_versions
                    WHERE
                        product_id = :product_id
                    )
            ),
            :amount
        )
        """

        params = [
            {   
                'purchase_id': purchase_id,
                'product_id': sale['product_id'], 
                'amount': sale['amount']
            } 
            for sale in bought_products
        ]

        self.__db.session.execute(text(create_product_sale), params)
        self.__db.session.commit()

        return purchase

