import requests
import csv

json_response = requests.get("https://appsumo.com/api/smartcollections/personal/?include_deals=true&page=1&limit=4").json()

file_name = "appsumo_customer_favorites.csv"

file = open(file_name, "w")
products = csv.writer(file)

cols = ["id", "media_url", "public_name", "card_description", "slug", "is_marketplace", "price", "original_price", "deal_review_count", "deal_review_rating", "sub_category", "category", "group"]
products.writerow(cols)

if json_response is not None:
    collections = json_response["collections"]

    for single_collection in collections:
        if "slug" not in single_collection:
            raise ValueError("No target data is available for slug")
        if single_collection["slug"] == "customer-favorites":
            for deal in single_collection["deals"]:
                single_product = [deal["id"], deal["media_url"], deal["public_name"], deal["card_description"],
                                  deal["slug"], deal["is_marketplace"], deal["price"], deal["original_price"],
                                  deal["deal_review"]["review_count"], deal["deal_review"]["average_rating"],
                                  deal["taxonomy"]["subcategory"]["value_enumeration"],
                                  deal["taxonomy"]["category"]["value_enumeration"],
                                  deal["taxonomy"]["group"]["value_enumeration"]]
                products.writerow(single_product)
else:
    print("Cannot extract data from the API")

file.close()