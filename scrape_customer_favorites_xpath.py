import requests as req
from bs4 import BeautifulSoup
import csv

headers = (
    { 'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
      'Accept-Language': 'en-US, en;q=0.5'
    }
)

response = req.get('https://appsumo.com/', headers=headers)

filename = "appsumo_customer_favorites_xpath.csv"
f = open(filename, "w")
products_csv = csv.writer(f)

cols = ["title", "product_img", "product_link", "category", "reviews", "description", "rating", "price", "old_price"]


products_csv.writerow(cols)

if response.status_code == 200:
    # html_contents = response.content
    soup = BeautifulSoup(response.text, 'html.parser')

    for extractDiv in soup.find_all("section", {"class": "my-4"}):
        if extractDiv.find("h3").text == 'Customer favorites':

            products = extractDiv.find("div", {"class": "flicking-camera"})
            for single in products:
                anchor_tag = single.select("div a")
                title = anchor_tag[0].string

                # title = single.find_all("div")[1].find_all("div")[3].find_all("span")[0].string

                product_img = single.find("img")["src"]
                product_link = anchor_tag[0]["href"]

                category = anchor_tag[1].string
                reviews = str(anchor_tag[2].find_all("span")[0]).replace("<!-- --> reviews</span>", "").replace("<span>", "")
                description = single.find_all("div")[1].find_all("div")[3].find_all("div")[1].string
                rating = single.find_all("div")[1].find_all("div")[3].find_all("div")[3].find("img")["alt"]

                # if title == "Reoon Email Verifier":
                # price = str(single.find_all("div")[1].find_all("div")[3].find_all("div")[3].find_all("span")[1]).replace('<span class="text-sm font-normal">/<!-- -->lifetime</span></span>', '').replace("<span>", "")
                # old_price = single.find_all("div")[1].find_all("div")[3].find_all("div")[3].find_all("span")[3].string

                price = str(single.find_all("div")[1].find_all("div")[3].find_all("span")[3]).replace('<span class="text-sm font-normal">/<!-- -->lifetime</span></span>', "").replace("<span>", "")
                old_price = single.find_all("div")[1].find_all("div")[3].find_all("span")[5].string

                # print(single.find_all("div")[1].find_all("div")[3].find_all("span")[5])

                single_item = [
                    title,
                    product_img,
                    product_link,
                    category,
                    reviews,
                    description,
                    rating,
                    price,
                    old_price
                ]

                products_csv.writerow(list(single_item))
else:
    print("Cannot extract data from the source")

f.close()