from daos.product_dao import ProductDao

class ProductService:
    def __init__(self, dao: ProductDao) -> None:
        self.__dao = dao

    def get_products(self):
        results = self.__dao.get_products()

        formatted = [
            {
                'id': id,
                'name': name
            }
            for id, name in results
        ]

        return formatted

    def create_product(self, name: str):
        id, name = self.__dao.create_product(name)

        formatted = {'id': id, 'name': name}

        return formatted