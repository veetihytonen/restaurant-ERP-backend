from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

class FoodstockDao:
    """
    DB Interface for doing any business related to ingredients:
        - Adding ingredients
        - Stock updates
        - Replenishments (orders)
    """

    def __init__(self, db_connection: SQLAlchemy) -> None:
        self.__db = db_connection

    def get_ingredient_by_id(self, id: int) -> tuple[int, str, str]:
        sql = "SELECT id, name, storage_category FROM ingredients WHERE id = :id"
        params = {'id':id}
        result = self.__db.session.execute(text(sql), params)
        
        return result.fetchone()
    
    def get_ingredient_by_name(self, name: str) -> tuple[int, str, str]:
        sql = "SELECT id, name, storage_category FROM ingredients WHERE name = :name"
        params = {'name':name}
        result = self.__db.session.execute(text(sql), params)

        return result.fetchone()

    def get_all_ingredients(self) -> list[tuple[int, str,str]]:
        sql = "SELECT id, name, storage_category FROM ingredients"
        result = self.__db.session.execute(text(sql))
        
        return result.fetchall()

    def create_ingredient(self, name: str, storage_category: str) -> tuple[int, str, str]:
        """Returns created row"""
        sql = """
        INSERT INTO ingredients (
            name, 
            storage_category)
        VALUES (
            :name,
            :strg_ctgr) 
        RETURNING id, name, storage_category
        """
        params = {"name":name, "strg_ctgr":storage_category}

        result = self.__db.session.execute(text(sql), params)
        self.__db.session.commit()

        return result.fetchone()
    
    def create_stock_update(self,
                            replesnishment_id: int | None, 
                            purchase_id: int | None, 
                            ingredient_id: int,
                            amount: float) -> tuple[int | None, int | None, int, float]:
        """Takes in either replenishment_id or purchase_id depending on event that creates update"""

        sql = """
            INSERT INTO ingredient_stock_updates (
                replenishment_id, 
                purchase_id, 
                ingredient_id, 
                amount) 
            VALUES (
                :repl_id, 
                :purch_id, 
                :ingr_id, 
                :amount)
            RETURNING (
                replenishment_id,
                purchase_id,
                ingredient_id,
                amount)
        """
        params = {"repl_id":replesnishment_id, 
                  "purch_id":purchase_id, 
                  "ingr_id":ingredient_id, 
                  "amount":amount}
        
        result = self.__db.session.execute(text(sql), params)

        return result.fetchone()
