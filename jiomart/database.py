import re
import os
import csv
import json
import requests
import django


from jio_data import JioData

from jiomart_app.models import Product


class Database(JioData):
    def __init__(self) -> None:
        super().__init__()

        # For connecting Django Model
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_project.settings")
        django.setup()

        self.__base_url = "https://www.jiomart.com/catalog/productdetails/get/"

    def get_product_details(self, product_id):
        product_url = self.__base_url + product_id

        res = requests.get(url=product_url, cookies=self.cookies, headers=self.headers)

        try:
            res = res.json()
        except json.JSONDecodeError:
            print(res.text)
            raise

        if res["status"] == "success":
            product_detail = {}
            data = res["data"]

            # Scraping the product details from the response
            product_detail["id"] = data["gtm_details"]["id"]
            product_detail["name"] = data["gtm_details"]["name"]
            product_detail["price"] = float(data["gtm_details"]["price"])
            product_detail["brand"] = data["gtm_details"]["brand"]
            product_detail["generic_name"] = ""

            product_detail["max_qty"] = data["max_qty_in_order"]

            def extract_weight_unit(product_name):
                pattern = r"Approx (\d+)\s*(g|kg|grams|gm|ml|l)?\s*-\s*(\d+)\s*(g|kg|grams|gm|ml|l)?|(\d+)\s*(g|kg|grams|gm|ml|l)"
                matches = re.search(pattern, product_name, re.IGNORECASE)

                if matches:
                    weight = matches.group(1) or matches.group(5)
                    unit = matches.group(2) or matches.group(6)
                    return (
                        float(weight),
                        unit.lower() if unit else None,
                    )
                return None

            weight_unit = extract_weight_unit(product_detail["name"])

            if weight_unit:
                product_detail["weight"] = weight_unit[0]
                product_detail["unit"] = weight_unit[1]
            else:
                product_detail["weight"] = product_detail["unit"] = None

            # Fetching required payload for getting seller_id and availability
            l_idx = data["image_url"].rfind("/")
            s_idx = data["image_url"].rfind("/", 0, l_idx)
            article_id = data["image_url"][s_idx + 1 : l_idx]

            category = data["gtm_details"]["category"]
            vertical = category[0 : category.index("/")].upper()

            tenant_ids = data["tenant_ids"]

            mobile_no = self.get_customer_details()["mobile_no"]

            def get_additional_details(article_id, vertical, tenant_ids, mobile_no):
                json_data = """
                {
                "identifier": "",
                "to_pincode": "",
                "customer_details": {
                    "phone_number": "0",
                    "pincode": "",
                    "coordinates": {
                    "lat": 0,
                    "long": 0
                    }
                },
                "articles": [
                    {
                    "article_id": "",
                    "vertical": "",
                    "lookup_inventory": true,
                    "tenant_ids": "",
                    "merchant_id": null,
                    "exchange_details": null
                    }
                ]
                }"""

                # Load JSON string into a dictionary
                data_dict = json.loads(json_data)

                uuid_value = self.get_UUID()
                location_data = self.get_location_details(self.headers["Pin"])

                # Update values
                data_dict["identifier"] = uuid_value
                data_dict["to_pincode"] = data_dict["customer_details"][
                    "pincode"
                ] = location_data["pin"]
                data_dict["customer_details"]["phone_number"] = mobile_no
                data_dict["customer_details"]["coordinates"]["lat"] = location_data[
                    "lat"
                ]
                data_dict["customer_details"]["coordinates"]["long"] = location_data[
                    "lon"
                ]
                data_dict["articles"][0].update(
                    {
                        "article_id": article_id,
                        "vertical": vertical,
                        "tenant_ids": tenant_ids,
                    }
                )

                url = "https://www.jiomart.com/platform/logistics/api/v1/promise"
                res = requests.post(
                    url=url, cookies=self.cookies, headers=self.headers, json=data_dict
                )

                try:
                    res = res.json()
                except json.JSONDecodeError:
                    print(res.text)
                    raise

                errors = res["articles"][0]["error"]

                if errors["type"] == None:
                    return True, res["articles"][0]["seller_data"][0]["sellerid"]
                else:
                    return False, res

            seller_details = get_additional_details(
                article_id, vertical, tenant_ids, mobile_no
            )

            if seller_details[0]:
                product_detail["availability"] = True
                product_detail["seller_id"] = seller_details[1]

                if product_detail["seller_id"] == "1":
                    product_detail["cart_category"] = "smart"
                else:
                    product_detail["cart_category"] = "normal"

            else:
                print(
                    "Product with id : ",
                    product_id,
                    ", not available at your pincode",
                    self.headers["Pin"],
                )
        else:
            print("Failed to get details for product with id:", product_id)
            return False, None

        return True, product_detail

    def refresh_databse(self):
        with open("product_list.csv", "r") as product_list:
            csv_reader = csv.DictReader(product_list)

        for product in csv_reader:
            product_detail = self.get_product_details(product["id"])
            new_product = Product(
                id=product_detail["id"],
                name=product_detail["name"],
                brand=product_detail["brand"],
                weight_value=product_detail["weight"],
                weight_unit=product_detail["unit"],
                price=product_detail["price"],
                max_qty=product_detail["max_qty"],
                seller_id=product_detail["seller_id"],
                generic_name=product_detail["generic_name"],
                cart_category=product_detail["cart_category"],
                available=product_detail["availability"],
            )
            new_product.save()