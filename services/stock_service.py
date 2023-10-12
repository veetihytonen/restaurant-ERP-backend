from daos.stock_dao import StockDao

class StockService:
    def __init__(self, dao: StockDao) -> None:
        self.__dao = dao

    def create_warehouse_replenishment(self, vendor_name: str, replenishments: list[tuple[int, int, float]]):
        r_id, v_name = self.__dao.create_warehouse_replenishment(vendor_name=vendor_name, replenishments=replenishments)
        for_json = {'id': r_id, 'vendor_name': v_name}

        return for_json
    
    def get_warehouse_replenishments(self):
        results = self.__dao.get_all_warehouse_replenishments()
        for_json = [{'id': replenishment_id, 'vendor_name': vendor_name} for replenishment_id, vendor_name in results]

        return for_json
    
    def get_ingredient_replenishments(self):
        results = self.__dao.get_ingredient_replenishments()
        for_json = [
            {
            'id': id, 
            'replenishment_id': replenishment_id, 
            'ingredient_id': ingredient_id, 
            'amount': amount, 
            'price_per_untit': price_per_unit
            } 
            for id, replenishment_id, ingredient_id, amount, price_per_unit in results
        ]

        return for_json
    
    def get_ingredient_replenishment_by_id(self, replenishment_id: int):
        results = self.__dao.get_ingredient_replenishment_by_replenishment_id(replenishment_id)
        id, replenishment_id, ingredient_id, amount, price_per_unit = results

        for_json = {
            'id': id, 
            'replenishment_id': replenishment_id, 
            'ingredient_id': ingredient_id, 
            'amount': amount, 
            'price_per_untit': price_per_unit
        }

        return for_json
    
    def get_ingredient_replenishments_by_wh_replenishment_id(self, wh_replenishment_id):
        results = self.__dao.get_ingredient_replenishments_by_wh_replenishment_id(wh_replenishment_id)
        
        for_json = [
            {
            'id': id, 
            'replenishment_id': replenishment_id, 
            'ingredient_id': ingredient_id, 
            'amount': amount, 
            'price_per_untit': price_per_unit
            }
        for id, replenishment_id, ingredient_id, amount, price_per_unit in results
        ]

        return for_json

    def get_all_stock_levels(self):
        results = self.__dao.get_all_stock_levels()
        for_json = [{'id': ingredient_id, 'amount': amount} for ingredient_id, amount in results]
        
        return for_json

    def get_stock_level_by_id(self, ingredient_id: int):
        i_id, amount = self.__dao.get_stock_level_by_id(ingredient_id)
        for_json = {'id': i_id, 'amount': amount}

        return for_json
