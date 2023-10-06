from daos.stock_dao import StockDao

class StockService:
    def __init__(self, dao: StockDao) -> None:
        self.__dao = dao

    def create_warehouse_replenishment(self, vendor_name: str, replenishments: list[tuple[int, int, float]]):
        r_id, v_name = self.__dao.create_warehouse_replenishment(vendor_name=vendor_name, replenishments=replenishments)

        return {'id': r_id, 'vendor_name': v_name}
    
    def get_warehouse_replenishments(self):
        results = self.__dao.get_all_warehouse_replenishments()
        for_json = [{'id': replenishment_id, 'vendor_name': vendor_name} for replenishment_id, vendor_name in results]

        return for_json
