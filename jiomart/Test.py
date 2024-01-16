import json, requests, random, re

url = "https://www.jiomart.com/catalog/productdetails/get/590860406"


headers = {
    "X-Application-Token": "qO2p_wQkq",
    "X-Oms-Application-Id": "5ea6821b3425bb07c82a25c1",
    "User-Agent": "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)",
    "Authtoken": "424ab093285edb504c634af4b4f3aa80fdd838551942891454",
    "Userid": "97715759",
    "Pin": "452010",
}

__base_url = "https://www.jiomart.com/catalog/productdetails/get/"


def get_UUID():
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


def get_location_details(pincode):
    location_url = f"https://www.jiomart.com/mst/rest/v1/5/pin/{pincode}"
    location_res = requests.get(url=location_url, headers=headers)
    try:
        location_res = location_res.json()
    except json.JSONDecodeError:
        print(location_res.text)
        raise

    return location_res["result"]


def get_customer_details():
    url = "https://www.jiomart.com/mst/rest/v1/entity/customer/get_details"
    res = requests.get(url=url, headers=headers)

    try:
        res = res.json()
    except json.JSONDecodeError:
        print(res.text)
        raise

    if res["status"] == "success":
        return True, res["result"]["your_details"]
    else:
        return False, res.text


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


def get_product_details(product_id):
    product_url = __base_url + product_id

    res = requests.get(url=product_url, headers=headers)

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

        product_detail["max_qty"] = data["max_qty_in_order"]

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

        mobile_no = get_customer_details()[1]["mobile_no"]

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

            uuid_value = get_UUID()
            location_data = get_location_details(headers["Pin"])

            # Update values
            data_dict["identifier"] = uuid_value
            data_dict["to_pincode"] = data_dict["customer_details"][
                "pincode"
            ] = location_data["pin"]
            data_dict["customer_details"]["phone_number"] = mobile_no
            data_dict["customer_details"]["coordinates"]["lat"] = location_data["lat"]
            data_dict["customer_details"]["coordinates"]["long"] = location_data["lon"]
            data_dict["articles"][0].update(
                {
                    "article_id": article_id,
                    "vertical": vertical,
                    "tenant_ids": tenant_ids,
                }
            )

            url = "https://www.jiomart.com/platform/logistics/api/v1/promise"
            res = requests.post(url=url, headers=headers, json=data_dict)

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

        if seller_details[0]:
            product_detail["availability"] = True
            product_detail["seller_id"] = seller_details[1]
        else:
            print(
                "Product with id : ",
                product_id,
                ", not available at your pincode",
                headers["Pin"],
            )
    else:
        print("Failed to get details for product with id:", product_id)

    return product_detail


print(get_product_details("604786225"))

# Sample data
product_names = [
    "Tender Coconut 1 pc (Approx 800 g - 1500 g)",
    "Ginger 200 g",
    "Cauliflower 1 pc (Approx 300 g - 500 g)",
    "Good Life Masoor Dal 500 g",
    "Tata Sampann Unpolished Toor / Arhar Dal 500 g",
    "Good Life Chana Dal 1 kg",
    "Some Product 2 kg",
    "Britannia 50-50 Maska Chaska Biscuits 300 g",
    "MidBreak - Cake Rusk | Extra Soft | Cake Rusk | 100% Eggless | Premium Handmade Cake Rusks | 300 Gm | Pack of 1",
    "GRABOLL PREMIUM RUSK 60GM (PACK OF 24)",
    "Paper Boat Coconut Water 200 ml",
    "Maaza Mango Drink 1.2 L",
    "Vim Lemon Dishwash Bar 4x200 g",
    "Vim Lemon Dishwash Liquid 900 ml",
]

# Extract weight and unit for each product name
for product_name in product_names:
    result = extract_weight_unit(product_name)
    print(f"{product_name}: {result}")
