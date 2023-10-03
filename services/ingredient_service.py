from daos.foodstock_dao import FoodstockDao

class IngredientService:
    def __init__(self, dao: FoodstockDao) -> None:
        self.__dao = dao

    def get_all(self) -> list[dict[int, str, str]]:
        results = self.__dao.get_all_ingredients()
        formatted = [{'id':id, 'name':name, 'storage_category':strg_ctgr} for id, name, strg_ctgr in results]

        return formatted
    
    def get_by_id(self, ingr_id: int) -> dict[int, str, str]:
        id, name, strg_ctgr = self.__dao.get_ingredient_by_id(ingr_id)

        return {'id':id, 'name':name, 'storage_category':strg_ctgr}
    
    def create(self, name: str, category: str) -> dict[int, str, str]:
        id, name, strg_ctgr = self.__dao.create_ingredient(name=name, storage_category=category)

        return {'id':id, 'name':name, 'storage_category':strg_ctgr}
