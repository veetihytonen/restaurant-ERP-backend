from daos.purchase_dao import PurchaseDao

class PurchaseService:
    def __init__(self, dao: PurchaseDao) -> None:
        self.__dao = dao

    def create_purchase(self, bought_products: list[dict[int, int]]):
        purchase_id, customer_id = self.__dao.create_purchase(bought_products)

        formatted = {'purchase_id': purchase_id, 'customer_id': customer_id}

        return formatted