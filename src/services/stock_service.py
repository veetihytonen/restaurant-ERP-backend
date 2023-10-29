from daos.stock_dao import StockDao

class StockService:
    def __init__(self, dao: StockDao) -> None:
        self.__dao = dao

    def create_warehouse_replenishment(self, vendor_name: str, replenishments: list[dict]):
        r_id, v_name = self.__dao.create_warehouse_replenishment(vendor_name=vendor_name, replenishments=replenishments)
        formatted = {'id': r_id, 'vendor_name': v_name}

        return formatted
    
    def get_warehouse_replenishments(self):
        results = self.__dao.get_all_warehouse_replenishments()
        formatted = [{'id': replenishment_id, 'vendor_name': vendor_name} for replenishment_id, vendor_name in results]

        return formatted
    
    def get_ingredient_replenishments(self):
        results = self.__dao.get_ingredient_replenishments()
        formatted = [
            {
                'id': id, 
                'replenishment_id': replenishment_id, 
                'ingredient_id': ingredient_id, 
                'amount': amount, 
                'price_per_untit': price_per_unit
            } 
            for id, replenishment_id, ingredient_id, amount, price_per_unit in results
        ]

        return formatted
    
    def get_ingredient_replenishment_by_id(self, replenishment_id: int):
        results = self.__dao.get_ingredient_replenishment_by_replenishment_id(replenishment_id)
        id, replenishment_id, ingredient_id, amount, price_per_unit = results

        formatted = {
            'id': id, 
            'replenishment_id': replenishment_id, 
            'ingredient_id': ingredient_id, 
            'amount': amount, 
            'price_per_untit': price_per_unit
        }

        return formatted
    
    def get_ingredient_replenishment_by_wh_replenishment_id(self, wh_replenishment_id):
        results = self.__dao.get_ingredient_replenishments_by_wh_replenishment_id(wh_replenishment_id)
        
        formatted = [
            {
            'id': id, 
            'vendor_name': vendor_name,
            'ingredient_name': ingredient_name,
            'replenishment_id': replenishment_id, 
            'ingredient_id': ingredient_id, 
            'amount': amount, 
            'price_per_unit': price_per_unit
            }
        for id, vendor_name, ingredient_name, replenishment_id, ingredient_id, amount, price_per_unit in results
        ]

        print(formatted)

        return formatted

    def get_all_stock_levels(self):
        results = self.__dao.get_all_stock_levels()
        formatted = [{'id': id, 'name': name, 'amount': amount} for id, name, amount in results]
        
        return formatted

    def get_stock_level_by_id(self, ingredient_id: int):
        i_id, amount = self.__dao.get_stock_level_by_id(ingredient_id)
        formatted = {'id': i_id, 'amount': amount}

        return formatted
