from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

class StockDao:
    def __init__(self, db_connection: SQLAlchemy) -> None:
        self.__db = db_connection
    
    def get_all_warehouse_replenishments(self) -> list[tuple[int, str]]:
        sql = """
        SELECT id, vendor_name
        FROM warehouse_replenishments
        """

        results = self.__db.session.execute(text(sql))

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

        replenishment_id, vendor_name = session.execute(text(sql), params).fetchone()

        sql = """
        INSERT INTO ingredient_replenishments (
            warehouse_replenishment_id,
            ingredient_id,
            amount,
            price_per_unit
        )
        VALUES (
            :repl_id,
            :ingr_id,
            :amount,
            :ppu
        );
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
        """

        params = [
            {
                'repl_id': replenishment_id, 
                'ingr_id': repl['ingredient_id'], 
                'amount': repl['amount'],
                'ppu': repl['price_per_unit']
            } 
            for repl in replenishments
        ]

        session.execute(text(sql), params)
        session.commit()

        return (replenishment_id, vendor_name)
