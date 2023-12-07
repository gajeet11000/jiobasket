import requests
import json

from jio_data import JioData


class JioMart(JioData):
    def __init__(self) -> None:
        super().__init__()

    def get_cart_items(self, cart_id):
        timestamp = self.__get_timestamp()
        url = f"https://www.jiomart.com/mst/rest/v1/5/cart/get?n={timestamp}&cart_id={cart_id}"

        res = requests.get(url=url, cookies=self.cookies, headers=self.request_headers)

        try:
            res = res.json()
        except json.JSONDecodeError:
            print(res.text)
            raise

        if res["status"] == "success":
            return True, res["result"]["cart"]["lines"]
        else:
            return False, res

    def add_to_cart(self, cart_type, product_id, qty, seller_id=1):
        timestamp = self.__get_timestamp()

        url = f"https://www.jiomart.com/mst/rest/v1/5/cart/add_item?product_code={product_id}&qty={qty}&seller_id={seller_id}&n={timestamp}"

        if cart_type == "regular":
            url += f"&cart_id={self.cart_id}"
        else:
            url += f"&cart_id={self.smart_cart_id}"

        res = requests.get(url=url, cookies=self.cookies, headers=self.request_headers)

        try:
            res = res.json()
        except json.JSONDecodeError:
            print(res.text)
            raise

        if res["status"] == "success":
            return True
        else:
            return False, res
