from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

class StockDao:
    def __init__(self, db_connection: SQLAlchemy) -> None:
        self.__db = db_connection

    def get_all_stock_levels(self):
        sql = """
        SELECT ingredient_id, SUM (amount)
        FROM ingredient_stock_updates
        GROUP BY ingredient_id
        ORDER BY ingredient_id ASC
        """

        results = self.__db.session.execute(text(sql))

        return results.fetchall()
    
    def get_stock_level_by_id(self, ingredient_id: int):
        sql = """
        SELECT ingredient_id, SUM (amount)
        FROM ingredient_stock_updates
        WHERE ingredient_id = :id
        GROUP BY ingredient_id
        """

        params = {'id': ingredient_id}

        results = self.__db.session.execute(text(sql), params)
        
        return results.fetchone()

    def get_all_warehouse_replenishments(self) -> list[tuple[int, str]]:
        sql = """
        SELECT id, vendor_name
        FROM warehouse_replenishments
        """

        results = self.__db.session.execute(text(sql))

        return results.fetchall()
    
    def get_ingredient_replenishments(self):
        sql = """
        SELECT 
            id,
            replenishment_id, 
            ingredient_id,
            amount,
            price_per_unit
        FROM ingredient_replenishments
        """

        results = self.__db.session.execute(text(sql))

        return results.fetchall()
    
    def get_ingredient_replenishment_by_replenishment_id(self, replenishment_id: int):
        sql = """
        SELECT
            id,
            replenishment_id, 
            ingredient_id,
            amount,
            price_per_unit
        FROM ingredient_replenishments
        WHERE id = :id
        """

        params = {'id': replenishment_id}

        results = self.__db.session.execute(text(sql), params)

        return results.fetchone()
    
    def get_ingredient_replenishments_by_wh_replenishment_id(self, wh_replenishment_id: int):
        sql = """
        SELECT 
            id,
            replenishment_id, 
            ingredient_id,
            amount,
            price_per_unit
        FROM ingredient_replenishments
        WHERE replenishment_id = :id
        """

        params = {'id': wh_replenishment_id}

        results = self.__db.session.execute(text(sql), params)

        return results.fetchall()

    def create_warehouse_replenishment(self, vendor_name: str, replenishments: list[dict]):
        session = self.__db.session

        sql = """
        INSERT INTO warehouse_replenishments (
            vendor_name
        )
        VALUES (
            :name
        )
        RETURNING id, vendor_name
        """

        params = {'name': vendor_name}

        wh_replenishment_id, vendor_name = session.execute(text(sql), params).fetchone()
        
        sql = """
        INSERT INTO ingredient_stock_updates (
            replenishment_id, 
            purchase_id, 
            ingredient_id, 
            amount
        ) 
        VALUES (
            :repl_id, 
            NULL, 
            :ingr_id, 
            :amount
        );

        INSERT INTO ingredient_replenishments (
            replenishment_id,
            ingredient_id,
            amount,
            price_per_unit
        )
        VALUES (
            :repl_id,
            :ingr_id,
            :amount,
            :ppu
        )
        """

        params = [
            {
                'repl_id': wh_replenishment_id, 
                'ingr_id': repl['ingredient_id'], 
                'amount': repl['amount'],
                'ppu': repl['price_per_unit']
            } 
            for repl in replenishments
        ]

        session.execute(text(sql), params)
        session.commit()

        return (wh_replenishment_id, vendor_name)
