import requests
import json

from jio_data import JioData


class JioMart(JioData):
    def __init__(self) -> None:
        super().__init__()

    def get_cart_items(self, cart_type):
        timestamp = self.get_timestamp()
        url = f"https://www.jiomart.com/mst/rest/v1/5/cart/get?n={timestamp}&cart_id="

        try:
            url += str(self.get_cart_id_by_type(cart_type))
        except Exception:
            print("Invalid cart type. Please check for your input cart type")

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

    def add_to_cart(self, cart_type, product_id, seller_id=1, qty=1):
        timestamp = self.get_timestamp()

        url = f"https://www.jiomart.com/mst/rest/v1/5/cart/add_item?product_code={product_id}&qty={qty}&seller_id={seller_id}&n={timestamp}&cart_id="

        try:
            url += str(self.get_cart_id_by_type(cart_type))
        except Exception:
            print("Invalid cart type. Please check for your input cart type")

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

    def remove_from_cart(self, cart_type, product_id, qty=1):
        timestamp = self.get_timestamp()
        url = f"https://www.jiomart.com/mst/rest/v1/5/cart/remove_item?product_code={product_id}&qty={qty}&n={timestamp}&cart_id="

        try:
            url += str(self.get_cart_id_by_type(cart_type))
        except Exception:
            print("Invalid cart type. Please check for your input cart type")

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
