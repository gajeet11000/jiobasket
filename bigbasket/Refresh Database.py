from bs4 import BeautifulSoup
import requests, json

cookies_dict = {
    "sessionid": "4hxg8ghwsgqwp8bx8uy3swdplgkrm0b1",
    "BBAUTHTOKEN": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJjaGFmZiI6IlltUzB1LXZFWFhFRjdnIiwidGltZSI6MTY5OTY1MjAyMC4wNjQ1MDg0LCJtaWQiOjQ3MzkwODA1LCJ2aWQiOjg1MDE0OTYyMzEsImRldmljZV9pZCI6IldFQiIsInNvdXJjZV9pZCI6MSwiZWNfbGlzdCI6WzMsNCwxMCwxMiwxMywxNCwxNSwxNiwxNywyMCwxMDBdLCJURExUT0tFTiI6ImUwNTRhOWJhLTA5NzgtNGQ0MC05NzkzLWEzOTQyMGIxZmZkMSIsInJlZnJlc2hfdG9rZW4iOiJkOWIwMDhiMS02NDkwLTQ1NmYtYWFmMS1jYjlhZjY4OWJkY2MiLCJ0ZGxfZXhwaXJ5IjoxNzAwMjU2ODE4LCJleHAiOjE3MTU0MzIwMjAsImlzX3NhZSI6bnVsbH0.WVRDDlMka0jB5accK8PnIIpAogkM3-togXUloblYg6o",
    "access_token": "e054a9ba-0978-4d40-9793-a39420b1ffd1",
}

header = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
}

product_url = "https://www.bigbasket.com/pd/266157"

product_respond = str(
    requests.get(url=product_url, cookies=cookies_dict, headers=header).text
)

soup = BeautifulSoup(product_respond, "html.parser")

data = soup.find("script", {"id": "__NEXT_DATA__", "type": "application/json"})

json_data = None

if data:
    json_data = data.string
    try:
        json_data = json.loads(json_data)
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
else:
    print("Script tab with ID = '__NEXT_DATA__' not found")

json_data = json_data["props"]["pageProps"]["productDetails"]["children"][0]

product_list = list(json_data.pop("children"))

product_list.append(json_data)

for product in product_list:
    product.pop("tabs")
    product.pop("breadcrumb")
    product.pop("images")

print(product_list)
