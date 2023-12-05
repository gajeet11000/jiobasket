import requests, time, json


class JioMart:
    def __init__(self) -> None:
        self.cookies = None
        self.request_headers = {
            "X-Application-Token": "qO2p_wQkq",
            "X-Oms-Application-Id": "5ea6821b3425bb07c82a25c1",
            "User-Agent": "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)",
        }
        self.cart_id = None
        self.__load_cookies()
        self.__load_headers()
        self.change_location()

    def set_header(self, key, value):
        self.cookies[key] = value

    def set_cookie(self, key, value):
        self.request_headers[key] = value

    def __get_location_details(self, pincode):
        location_url = f"https://www.jiomart.com/mst/rest/v1/5/pin/{pincode}"
        location_res = requests.get(
            url=location_url, headers=self.request_headers
        ).json()
        return location_res["result"]

    def change_location(self):
        pincode = input("Enter your area pincode: ")
        location_data = self.__get_location_details(pincode)

        self.set_header("Pin", location_data["pin"])

        self.set_cookie("nms_mgo_pincode", location_data["pin"])
        self.set_cookie("nms_mgo_state_code", location_data["state_code"])
        self.set_cookie("nms_mgo_city", location_data["pin"])

    def __load_cookies(self):
        try:
            with open("cookies.txt", "r") as file:
                data_dict = json.load(file)
            cookies = {}
            for cookie in data_dict:
                cookies[cookie["name"]] = cookie["value"]
            self.cookies = cookies
        except FileNotFoundError:
            print("File cookies.txt doesn't exist to load cookies")

    def __load_headers(self):
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
            return False, response

    def add_to_cart(self, product_id, seller_id=1):
        timestamp = self.__get_timestamp()

        cart_url = f"https://www.jiomart.com/mst/rest/v1/5/cart/add_item?product_code={product_id}&qty=1&seller_id={seller_id}&n={timestamp}"

        smart_cart_url = f"https://www.jiomart.com/mst/rest/v1/5/cart/add_item?product_code={product_id}&qty=1&seller_id=1&n={timestamp}&cart_id={self.cart_id}"

        response = requests.get(
            url=smart_cart_url, cookies=self.cookies, headers=self.request_headers
        ).json()

        if response["status"] == "success":
            return True
        else:
            return False, response

    def get_cart_items(self):
        timestamp = self.__get_timestamp()
        url = f"https://www.jiomart.com/mst/rest/v1/5/cart/get?n={timestamp}"

        response = requests.get(
            url=url, cookies=self.cookies, headers=self.request_headers
        ).json()
        if response["status"] == "success":
            return True, response["result"]["cart"]["lines"]
        else:
            return False, response
