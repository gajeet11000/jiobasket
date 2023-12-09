import os, time, requests, django

# Set up Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_project.settings")
django.setup()

from shopping_aio.models import Product

jiomart_product_url = "https://www.jiomart.com/catalog/productdetails/get/"

products = []

with open("jiomart_product_id.txt") as file:
    for line in file:
        products.append(line.strip().replace("\n", ""))
        
for product_id in products:
    
    product_url = jiomart_product_url + product_id

    response = requests.get(
        url=product_url, headers=request_header_jiomart, cookies=jiomart_cookies
    ).json()
    
    if response["status"] == "success":
        product_data = response["data"]["gtm_details"]
        new_product = Product(
            name=product_data["name"],
            price=float(product_data["price"]),
            brand=product_data["brand"],
        )
        try:
            new_product.save()
            print(new_product.name + " successfully saved")
        except Exception as e:
            print(f"Failed to save data:-\n{e}")
    else:    
        print(f"Product with the url below is not available at your pincode\n{product_url}")
    time.sleep(5)