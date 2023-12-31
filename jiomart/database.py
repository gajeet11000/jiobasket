import os
import csv
import time
import requests
import django

from jio_data import JioData

# from shopping_aio.models import Product


class Database(JioData):
    def __init__(self) -> None:
        super().__init__()

        # For connecting Django Model
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_project.settings")
        django.setup()

        self.__product_url = "https://www.jiomart.com/catalog/productdetails/get/"
        self.__products = {}

    def __initialize_from_csv(self):
        with open("product_list.csv", "r") as product_list:
            csv_reader = csv.DictReader(product_list)
            for product_row in csv_reader:
                self.__products[product_row["id"]] = product_row["name"]


# for product_id in products:
#     product_url = jiomart_product_url + product_id

#     response = requests.get(
#         url=product_url, headers=request_header_jiomart, cookies=jiomart_cookies
#     ).json()

#     if response["status"] == "success":
#         product_data = response["data"]["gtm_details"]
#         new_product = Product(
#             name=product_data["name"],
#             price=float(product_data["price"]),
#             brand=product_data["brand"],
#         )
#         try:
#             new_product.save()
#             print(new_product.name + " successfully saved")
#         except Exception as e:
#             print(f"Failed to save data:-\n{e}")
#     else:
#         print(
#             f"Product with the url below is not available at your pincode\n{product_url}"
#         )
#     time.sleep(5)
