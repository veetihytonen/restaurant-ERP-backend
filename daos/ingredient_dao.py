from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

from sqlalchemy.exc import IntegrityError

class IngredientDao:
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
        sql = """
        INSERT INTO ingredients (
            name, 
            storage_category
        )
        VALUES (
            :name,
            :strg_ctgr
        ) 
        RETURNING 
            id, name, storage_category
        """

        params = {'name':name, 'strg_ctgr':storage_category}
        
        try:
            result = self.__db.session.execute(text(sql), params)
            self.__db.session.commit()
        except IntegrityError:
            raise ValueError('Raaka-aine on jo olemassa')

        return result.fetchone()