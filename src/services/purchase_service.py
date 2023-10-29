from daos.purchase_dao import PurchaseDao

class PurchaseService:
    def __init__(self, dao: PurchaseDao) -> None:
        self.__dao = dao

    def get_purchases(self):
        purchases = self.__dao.get_purchases()

        formatted = [
            {'purchase_id': purchase_id}
            for purchase_id, in purchases
        ]

        return formatted

    def create_purchase(self, bought_products: list[dict[int, int]]):
        purchase_id = self.__dao.create_purchase(bought_products)

        formatted = {'purchase_id': purchase_id}

        return formatted
    
    def get_sales_by_purchase_id(self, purchase_id: int):
        sales = self.__dao.get_sales_by_purchase_id(purchase_id)

        formatted = [
            {
                'sale_id': sale_id,
                'purchase_id': purchase_id,
                'product_version_id': product_version_id,
                'amount': amount
            }
            for sale_id, purchase_id, product_version_id, amount
            in sales
        ]
        
        return formatted