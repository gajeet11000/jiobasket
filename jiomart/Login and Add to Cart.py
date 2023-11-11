import requests, time, sys

jiomart_cookies = {
    "AKA_A2": "A",
    "nms_mgo_pincode": "452010",
    "_ALGOLIA": "anonymous-80ed58be-6617-4a75-b7b4-b563e3878e39",
    "nms_mgo_city": "Indore",
    "nms_mgo_state_code": "MP",
    "new_customer": "true",
}
request_header_jiomart = {
    "Pin": "452010",
    "User-Agent": "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)",
}

mobile_no = "9516062018"

login_url = f"https://www.jiomart.com/mst/rest/v1/session/initiate/using_mobileno_n_otp?mobile_no={mobile_no}"

login_response = requests.get(
    url=login_url, headers=request_header_jiomart, cookies=jiomart_cookies
).json()

if login_response["status"] == "success":
    print("Login request sent successfully")
else:
    print("Failed to send login request")
    print(login_response)
    sys.exit()

rk = login_response["result"]["otp_details"]["random_key"]

otp = input("Otp: ")

submit_url = f"https://www.jiomart.com/mst/rest/v1/session/complete/using_mobileno_n_otp?mobile_no={mobile_no}&rk={rk}&otp={otp}&channel=web"
submit_response = requests.get(
    url=submit_url, headers=request_header_jiomart, cookies=jiomart_cookies
).json()

if submit_response["status"] == "success":
    print("Logged in successfully.")
else:
    print("Failed to login.")
    print(submit_response)
    sys.exit()

request_header_jiomart["Authtoken"] = str(submit_response["result"]["session"]["id"])
request_header_jiomart["Userid"] = str(
    submit_response["result"]["session"]["customer_id"]
)

unix_timestamp_milliseconds = str(int(time.time()) * 1000)

create_smart_cart_url = f"https://www.jiomart.com/mst/rest/v1/5/cart/create/smart?n={unix_timestamp_milliseconds}&universal=true"

create_smart_cart_response = requests.get(
    url=create_smart_cart_url, cookies=jiomart_cookies, headers=request_header_jiomart
).json()

if create_smart_cart_response["status"] == "success":
    print("Create smart cart successfully.")
else:
    print("Failed to create smart cart.")
    print(create_smart_cart_response)
    sys.exit()

cart_id = create_smart_cart_response["result"]["cart_id"]

unix_timestamp_milliseconds = str(int(time.time()) * 1000)

add_item_to_cart_url = f"https://www.jiomart.com/mst/rest/v1/5/cart/add_item?product_code=491185152&qty=1&seller_id=1&n={unix_timestamp_milliseconds}&cart_id={cart_id}"
add_item_to_cart_response = requests.get(
    url=add_item_to_cart_url, cookies=jiomart_cookies, headers=request_header_jiomart
).json()

if add_item_to_cart_response["status"] == "success":
    print("Item added to cart successfully.")
else:
    print("Failed to add item to cart.")
    print(add_item_to_cart_response)
    sys.exit()

unix_timestamp_milliseconds = str(int(time.time()) * 1000)

view_cart_url = f"https://www.jiomart.com/mst/rest/v1/5/cart/get?n={unix_timestamp_milliseconds}&cart_id={cart_id}"
view_cart_response = requests.get(
    url=view_cart_url, cookies=jiomart_cookies, headers=request_header_jiomart
).json()

if view_cart_response["status"] == "success":
    for product in view_cart_response["result"]["cart"]["lines"]:
        print(product["display_name"])
else:
    print("Failed to view cart items.")
    print(view_cart_response)


# for id in products:
# id = "491299542"
# try:
#     response = requests.get(
#         "https://www.jiomart.com/catalog/productdetails/get/" + id,
#         headers=request_header_jiomart,
#         cookies=jiomart_cookies,
#     ).json()

#     gtm_details = response["data"]["gtm_details"]
#     print(gtm_details["name"])
# except TypeError:
#     print(id)
# finally:
#     time.sleep(3)

# max_qty_in_order
# gtm_details
#     id
#     price
#     name
#     brand


# request_header_jiomart_test = {
#     "authority": "www.jiomart.com",
#     "method": "GET",
#     "scheme": "https",
#     "Accept": "text/html, */*; q=0.01",
#     "Accept-Encoding": "gzip, deflate, br",
#     "Accept-Language": "en-US,en;q=0.9,hi;q=0.8",
#     "Pin": "452010",
#     "Sec-Ch-Ua-Mobile": "?0",
#     "Sec-Fetch-Dest": "empty",
#     "Sec-Fetch-Mode": "cors",
#     "Sec-Fetch-Site": "same-origin",
#     "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
#     "X-Requested-With": "XMLHttpRequest",
# }
