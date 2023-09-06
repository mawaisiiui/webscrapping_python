import requests as req
from bs4 import BeautifulSoup
import json
import csv


file_name = "appsumo_customer_favorites_json.csv"
headers = (
    { 'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
      'Accept-Language': 'en-US, en;q=0.5'
    }
)
file = open(file_name, "w")
products = csv.writer(file)
response = req.get("https://appsumo.com/", headers=headers)

cols = ["id", "media_url", "public_name", "card_description", "slug", "is_marketplace", "price", "original_price", "deal_review_count", "deal_review_rating", "sub_category", "category", "group"]
products.writerow(cols)

if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')

    response_scripts = soup.find("script", {"id": "__NEXT_DATA__"}).text.strip()

    data = json.loads(response_scripts)

    if data is not None:
        if "props" not in data:
            raise ValueError("No {props} target is available in JSON data")
        if "pageProps" not in data["props"]:
            raise ValueError("No {pageProps} target is available in JSON data")
        if "fallbackData" not in data["props"]["pageProps"]:
            raise ValueError("No {props} target is available in JSON data")
        if "collections" not in data["props"]["pageProps"]["fallbackData"]:
            raise ValueError("No {pageProps} target is available in JSON data")

        for single_section in data["props"]["pageProps"]["fallbackData"]["collections"]:
            if single_section["slug"] == "customer-favorites":
                if "deals" not in single_section:
                    raise ValueError("No deals are available in JSON data")

                for deal in single_section["deals"]:
                    single_product = [deal["id"], deal["media_url"], deal["public_name"], deal["card_description"],
                                      deal["slug"], deal["is_marketplace"], deal["price"], deal["original_price"],
                                      deal["deal_review"]["review_count"], deal["deal_review"]["average_rating"],
                                      deal["taxonomy"]["subcategory"]["value_enumeration"],
                                      deal["taxonomy"]["category"]["value_enumeration"],
                                      deal["taxonomy"]["group"]["value_enumeration"]]
                    products.writerow(single_product)

else:
    print("No Response")



file.close()