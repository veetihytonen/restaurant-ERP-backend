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
    
    def get_product_by_id(self, product_id: int):
        id, name = self.__dao.get_prodcut_by_id(product_id)

        formatted = {'id': id, 'name': name}

        return formatted

    def create_product(self, name: str):
        id, name = self.__dao.create_product(name)

        formatted = {'id': id, 'name': name}

        return formatted
    
    def get_versions_for_product(self, product_id: int):
        versions = self.__dao.get_versions_for_product(product_id)

        formatted = [
            {
                'id': id,
                'sale_price': sale_price,
                'product_id': product_id
            }
            for id, sale_price, product_id in versions
        ]

        return formatted
    
    def get_version_by_number(self, product_id: int, version_number: int):
        id, version_number, sale_price, product_id = self.__dao.get_version_by_number(product_id=product_id, version_number=version_number)

        formatted = {'id': id, 'version_number': version_number, 'sale_price': sale_price, 'product_id': product_id}

        return formatted
    
    def create_product_version(
        self,
        sale_price: int, 
        product_id: int, 
        ingredients_and_amounts: list[dict[int, float]]
    ):
        product_version = self.__dao.create_product_version(
            sale_price=sale_price,
            product_id=product_id,
            ingredients_and_amounts=ingredients_and_amounts
        )

        formatted = {
            'product_version_id': product_version[0],
            'sale_price': product_version[1],
            'product_id': product_version[2]
            }
        
        return formatted