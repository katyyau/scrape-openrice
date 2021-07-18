import requests
import pandas

# to scrap the restaurants on the first page
headers = {
    # "GET /zh/hongkong/restaurants/type/%E5%B0%91%E9%B9%BD%E5%B0%91%E7%B3%96%E9%A3%9F%E5%BA%97?dedicatedPromotionId=13 HTTP/1.1"
    # "Host":"www.openrice.com",
    # "Connection":"keep-alive",
    # "Cache-Control":"max-age=0",
    # "Upgrade-Insecure-Requests":"1",
    "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.106 Safari/537.36",
    # "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    # "Accept-Encoding":"gzip, deflate",
    # "Accept-Language":"en-GB,en-US;q=0.9,en;q=0.8,zh-CN;q=0.7,zh;q=0.6",
}

url = "https://www.openrice.com/zh/hongkong/restaurants/type/%E5%B0%91%E9%B9%BD%E5%B0%91%E7%B3%96%E9%A3%9F%E5%BA%97?dedicatedPromotionId=13"

response = requests.get(url, headers=headers)
#print(response)
from bs4 import BeautifulSoup
soup = BeautifulSoup(response.text, "html.parser")

ul = soup.find_all('ul', class_='sr1-listing-content-cells')[0]
restaurants = ul.select("li.sr1-listing-content-cell")


rest_infos = []

# to scrap the link of each restaurant
rest_comments = []

for restaurant in restaurants:
    shop_title_name = restaurant.select("h2.title-name")[0].text.strip()
    shop_id = restaurant.select("section.js-openrice-bookmark.openrice-bookmark")[0]["data-poi-id"]
    shop_address = restaurant.select("div.icon-info.address")[0].text.strip()
    shop_price_range = restaurant.select("div.icon-info.icon-info-food-price")[0].text.strip()
    shop_comment_count = restaurant.select("div.counters-container")[0].text.strip()
    shop_bookmark_count = restaurant.select("div.text.bookmarkedUserCount.js-bookmark-count")[0]["data-count"]
    shop_like_count = restaurant.select(".smile-face .score")[0].text.strip()
    shop_dislike_count = restaurant.select(".sad-face .score")[0].text.strip()

    rest_infos.append([shop_title_name, shop_id, shop_address, shop_price_range, shop_comment_count, shop_bookmark_count, shop_like_count, shop_dislike_count])
    #print(rest_infos)
    shop_url = restaurant.select_one(".title-name>a")["href"]
    print(shop_url)
    full_link = "https://www.openrice.com" + shop_url + "/reviews"
    response2 = requests.get(full_link, headers=headers)
    soup2 = BeautifulSoup(response2.text, "html.parser")
    comments = soup2.select("section.sr2-review-list2-main-content-section")
    #print(comments)
    for comment in comments:
        comment_publish_date = comment.select("[itemprop=datepublished]")[0].text.strip()
        comment_title = comment.select(".review-title")[0].text.strip()
        comment_content_tag = comment.select(".content-full .review-container")[0]#.text.strip()
        comment_photos = comment_content_tag.select("a.photo")
        for comment_photo in comment_photos:
            comment_photo.extract()
        comment_content = comment_content_tag.text.strip().replace("\n","")
        comment_view_count = comment.select(".view-count")[0].text.strip()

        rest_comments.append([comment_publish_date, comment_title, comment_content, comment_view_count])


pandas.DataFrame(rest_infos).to_csv("rest_infos.csv")
pandas.DataFrame(rest_comments).to_csv("rest_comments.csv")