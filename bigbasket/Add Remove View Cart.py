import requests

cookies_dict = {
    "sessionid": "4hxg8ghwsgqwp8bx8uy3swdplgkrm0b1",
    "BBAUTHTOKEN": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJjaGFmZiI6IlltUzB1LXZFWFhFRjdnIiwidGltZSI6MTY5OTY1MjAyMC4wNjQ1MDg0LCJtaWQiOjQ3MzkwODA1LCJ2aWQiOjg1MDE0OTYyMzEsImRldmljZV9pZCI6IldFQiIsInNvdXJjZV9pZCI6MSwiZWNfbGlzdCI6WzMsNCwxMCwxMiwxMywxNCwxNSwxNiwxNywyMCwxMDBdLCJURExUT0tFTiI6ImUwNTRhOWJhLTA5NzgtNGQ0MC05NzkzLWEzOTQyMGIxZmZkMSIsInJlZnJlc2hfdG9rZW4iOiJkOWIwMDhiMS02NDkwLTQ1NmYtYWFmMS1jYjlhZjY4OWJkY2MiLCJ0ZGxfZXhwaXJ5IjoxNzAwMjU2ODE4LCJleHAiOjE3MTU0MzIwMjAsImlzX3NhZSI6bnVsbH0.WVRDDlMka0jB5accK8PnIIpAogkM3-togXUloblYg6o",
    "access_token": "e054a9ba-0978-4d40-9793-a39420b1ffd1",
    "_bb_vid": "NTM5MzUxNTg0OQ==",
}

header = {
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
}

add_to_cart_url = "https://www.bigbasket.com/mapi/v3.5.2/c-incr-i/"
remove_from_cart_url = "https://www.bigbasket.com/mapi/v3.5.2/c-decr-i/"
fetch_cart_url = "https://www.bigbasket.com/basketService/get/"

data = {"prod_id": 10000434, "qty": 2, "_bb_client_type": "web", "first_atb": 1}

add_to_cart_response = requests.get(
    url=add_to_cart_url, cookies=cookies_dict, headers=header
)

print(add_to_cart_response.text)
