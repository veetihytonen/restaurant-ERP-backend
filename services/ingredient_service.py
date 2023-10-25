from daos.ingredient_dao import IngredientDao

class IngredientService:
    def __init__(self, dao: IngredientDao) -> None:
        self.__dao = dao

    def get_all(self) -> list[dict[int, str, str]]:
        results = self.__dao.get_all_ingredients()
        formatted = [{'id':id, 'name':name, 'storage_category':strg_ctgr} for id, name, strg_ctgr in results]

        return formatted
    
    def get_by_id(self, ingr_id: int) -> dict[int, str, str]:
        id, name, strg_ctgr = self.__dao.get_ingredient_by_id(ingr_id)
        formatted = {'id':id, 'name':name, 'storage_category':strg_ctgr}

        return formatted
    
    def create(self, name: str, category: str) -> dict[int, str, str]:
        id, name, strg_ctgr = self.__dao.create_ingredient(name=name, storage_category=category)
        formatted = {'id':id, 'name':name, 'storage_category':strg_ctgr}

        return formatted
