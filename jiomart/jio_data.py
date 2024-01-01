import os
import time
import json
import random
import requests


class JioData:
    headers = {
        "X-Application-Token": "qO2p_wQkq",
        "X-Oms-Application-Id": "5ea6821b3425bb07c82a25c1",
        "User-Agent": "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)",
    }
    cookies = {}
    cart_id = None
    smart_cart_id = None

    def __init__(self) -> None:
        if self.is_super_not_instantiated():
            self.__load_cookies()
            self.__load_headers()

            self.__check_cart_ids()
            self.change_location()

    def is_super_not_instantiated(self):
        return (
            self.headers
            == {
                "X-Application-Token": "qO2p_wQkq",
                "X-Oms-Application-Id": "5ea6821b3425bb07c82a25c1",
                "User-Agent": "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)",
            }
            and self.cookies == {}
            and not self.cart_id
            and not self.smart_cart_id
        )

    def get_cart_id_by_type(self, cart_type):
        if cart_type == "regular":
            return self.cart_id
        elif cart_type == "smart":
            return self.smart_cart_id
        else:
            raise Exception("Invalid cart type exception!")

    def get_timestamp(self):
        return str(int(time.time()) * 1000)

    def __set_cookie(self, key, value):
        self.cookies[key] = value

    def __set_header(self, key, value):
        self.headers[key] = value

    def __set_smart_cart_id(self, new_cart_id):
        self.smart_cart_id = new_cart_id

    def __check_cart_ids(self):
        if not self.cart_id:
            self.__get_cart_id()
        if not self.smart_cart_id:
            self.__get_smart_cart_id()

    def get_UUID(self):
        uuid_pattern = "xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx"

        def generate_char(c):
            if c == "x":
                return format(int(random.random() * 16), "x")
            elif c == "y":
                return format((3 & int(random.random() * 16)) | 8, "x")
            else:
                return c

        uuid_result = "".join(generate_char(c) for c in uuid_pattern)
        return uuid_result

    def save_cookies_headers(self):
        with open("cookies.json", "w") as json_file:
            json.dump(self.cookies, json_file)

        with open("headers.json", "w") as json_file:
            json.dump(self.headers, json_file)

    def __get_location_details(self, pincode):
        location_url = f"https://www.jiomart.com/mst/rest/v1/5/pin/{pincode}"
        location_res = requests.get(url=location_url, headers=self.headers)
        try:
            location_res = location_res.json()
        except json.JSONDecodeError:
            print(location_res.text)
            raise

        return location_res["result"]

    def delete_session(self):
        try:
            os.remove("cookies.json")
            print("Saved cookies.json is deleted.")
        except FileNotFoundError:
            print("cookies.json not found to delete")
            raise
        try:
            os.remove("headers.json")
            print("Saved headers.json is deleted.")
        except FileNotFoundError:
            print("headers.json not found to delete")
            raise

    def __get_cart_id(self):
        timestamp = self.get_timestamp()
        url = f"https://www.jiomart.com/mst/rest/v1/5/cart/get?n={timestamp}"
        res = requests.get(url=url, headers=self.headers, cookies=self.cookies)
        try:
            res = res.json()
        except json.JSONDecodeError:
            print(res.text)
            raise

        if res["status"] == "success":
            self.cart_id = res["result"]["cart"]["id"]
        else:
            print("Failed to get regular cart id")

    def __get_smart_cart_id(self):
        url = "https://www.jiomart.com/mst/rest/v1/5/cart/get/smart_cart_id"
        res = requests.get(url=url, headers=self.headers, cookies=self.cookies)
        try:
            res = res.json()
        except json.JSONDecodeError:
            print(res.text)
            raise

        if res["status"] == "success":
            self.smart_cart_id = res["result"]["cart_id"]
        else:
            print("Failed to get smart cart id")

    def change_location(self):
        pincode = input("Enter your area pincode: ")
        location_data = self.__get_location_details(pincode)

        self.__set_header("Pin", location_data["pin"])

        self.__set_cookie("nms_mgo_pincode", location_data["pin"])
        self.__set_cookie("nms_mgo_state_code", location_data["state_code"])
        self.__set_cookie("nms_mgo_city", location_data["pin"])

        self.save_cookies_headers()

    def create_new_smart_cart(self):
        timestamp = self.get_timestamp()
        url = f"https://www.jiomart.com/mst/rest/v1/5/cart/create/smart?n={timestamp}&universal=true"
        res = requests.get(url=url, cookies=self.cookies, headers=self.request_headers)
        try:
            res = res.json()
        except json.JSONDecodeError:
            print(res.text)
            raise

        if res["status"] == "success":
            self.__set_smart_cart_id(res["result"]["cart_id"])
            return True
        else:
            return False, res

    def __load_cookies(self):
        if os.path.exists("cookies.json") and os.path.getsize("cookies.json") != 0:
            with open("cookies.json") as json_file:
                self.cookies.update(json.load(json_file))
        else:
            try:
                with open("cookies.txt", "r") as file:
                    data_dict = json.load(file)
                cookies = {}
                for cookie in data_dict:
                    cookies[cookie["name"]] = cookie["value"]
                self.cookies.update(cookies)
            except FileNotFoundError:
                print("File cookies.txt doesn't exist to load cookies")
                raise

    def __load_headers(self):
        if os.path.exists("headers.json") and os.path.getsize("headers.json") != 0:
            with open("headers.json") as json_file:
                self.headers.update(json.load(json_file))
        else:
            try:
                with open("local_storage.txt", "r") as file:
                    data_dict = json.load(file)
                headers = {}
                headers["Authtoken"] = data_dict["authtoken"]
                headers["Userid"] = data_dict["userid"]
                headers["Pin"] = data_dict["nms_mgo_pincode"]
                self.headers.update(headers)

                cart_info = data_dict.get("cart_info")
                if cart_info:
                    self.cart_id = cart_info["cart"]["id"]

                smart_cart_info = data_dict.get("smart_cart_info")
                if smart_cart_info:
                    self.smart_cart_id = smart_cart_info["cart"]["id"]

            except FileNotFoundError:
                print("File load_storage.txt doesn't exist to load headers")
                raise
