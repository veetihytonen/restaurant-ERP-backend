from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

class PurchaseDao:
    def __init__(self, db_connection: SQLAlchemy) -> None:
        self.__db = db_connection

    def get_purchases(self):
        sql = """
        SELECT
            id
        FROM
            purchases
        """

        purchases = self.__db.session.execute(text(sql))

        return purchases.fetchall()
    
    def create_purchase(self, bought_products: list[dict[int, int]]):
        purchase = """
            INSERT INTO purchases 
            VALUES(DEFAULT)
            RETURNING id
        """

        purchase = self.__db.session.execute(text(purchase)).fetchone()
        purchase_id = purchase[0]

        create_product_sale = """
        INSERT INTO product_sales (
            purchase_id,
            product_version_id,
            amount
        )
        SELECT
            :purchase_id,
            (SELECT
                id
            FROM
                product_versions
            WHERE 
                version_number = 
                    (SELECT 
                        MAX(version_number)
                    FROM
                        product_versions
                    WHERE
                        product_id = :product_id
                    )
            ),
            :amount
        RETURNING
            id
        """

        sale_params = [
            {   
                'purchase_id': purchase_id,
                'product_id': sale['product_id'], 
                'amount': sale['amount']
            } 
            for sale in bought_products
        ]

        sales = self.__db.session.execute(text(create_product_sale), sale_params).fetchall()

        create_stock_update = """
        INSERT INTO ingredient_stock_updates (
            product_sale_id,
            ingredient_id,
            amount
        )
        SELECT
            sales.id,
            ingredients.id,
            mapping.amount * sales.amount * (-1)
        FROM
            product_sales AS sales
        INNER JOIN
            product_versions as versions
        ON
            sales.product_version_id = versions.id
        INNER JOIN 
            product_ingredient_mapping AS mapping
        ON
            versions.id = mapping.product_version_id
        INNER JOIN 
            ingredients
        ON
            mapping.ingredient_id = ingredients.id
        WHERE 
            sales.id = :sale_id
        """
        print(sales)
        stock_update_params = [
            {'sale_id': sale_id}
            for sale_id, in sales
        ]

        self.__db.session.execute(text(create_stock_update), stock_update_params)

        self.__db.session.commit()

        return purchase_id
    
    def get_sales_by_purchase_id(self, purchase_id: int):
        sql = """
        SELECT
            s.id,
            s.purchase_id,
            s.product_version_id,
            s.amount
        FROM
            purchases AS p
        INNER JOIN
            product_sales AS s
        ON 
            p.id = s.purchase_id
        WHERE
            p.id = :purchase_id
        """

        params = {'purchase_id': purchase_id}

        sales = self.__db.session.execute(text(sql), params)

        return sales.fetchall()
