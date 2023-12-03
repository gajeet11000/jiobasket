import requests, time, json

class JioMart:
    def __init__(self) -> None:
        self.cookies = None
        self.request_headers = {
            "User-Agent": "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)",
        }
        self.cart_id = None

    def load_cookies(self):
        try:
            with open("cookies.txt", "r") as file:
                data_dict = json.load(file)
            cookies = {}
            for cookie in data_dict:
                cookies[cookie["name"]] = cookie["value"]
            self.cookies = cookies
        except FileNotFoundError:
            print("File cookies.txt doesn't exist to load cookies")

    def load_headers(self):
        try:
            with open("local_storage.txt", "r") as file:
                data_dict = json.load(file)
            headers = {}
            headers["Authtoken"] = data_dict["authtoken"]
            headers["Userid"] = data_dict["userid"]
            self.__add_request_headers(headers)
        except FileNotFoundError:
            print("File load_storage.txt doesn't exist to load headers")

    def __get_timestamp(self):
        return str(int(time.time()) * 1000)

    def __set_cart_id(self, cart_id):
        self.cart_id = cart_id

    def __add_request_headers(self, headers):
        self.request_headers.update(headers)

    def create_smart_cart(self):
        timestamp = self.__get_timestamp()
        url = f"https://www.jiomart.com/mst/rest/v1/5/cart/create/smart?n={timestamp}&universal=true"
        response = requests.get(
            url=url, cookies=self.cookies, headers=self.request_headers
        ).json()

        if response["status"] == "success":
            self.__set_cart_id(response["result"]["cart_id"])
            return True
        else:
            return False, response.text

    def add_to_cart(self, product_id):
        timestamp = self.__get_timestamp()
        url = f"https://www.jiomart.com/mst/rest/v1/5/cart/add_item?product_code={product_id}&qty=1&seller_id=1&n={timestamp}&cart_id={self.cart_id}"

        response = requests.get(
            url=url, cookies=self.cookies, headers=self.request_headers
        ).json()

        if response["status"] == "success":
            return True
        else:
            return False, response.text

    def get_cart_items(self):
        timestamp = self.__get_timestamp()
        url = f"https://www.jiomart.com/mst/rest/v1/5/cart/get?n={timestamp}&cart_id={self.cart_id}"

        response = requests.get(
            url=url, cookies=self.cookies, headers=self.request_headers
        ).json()
        if response["status"] == "success":
            return True, response["result"]["cart"]["lines"]
        else:
            return False, response.text