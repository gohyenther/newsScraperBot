import time
import requests
import pandas as pd
from random import randint
from bs4 import BeautifulSoup

NUM_ARTICLES = 3 # Top n headlines


def scrape_news(company, category):
    time.sleep(randint(0,5)) # relax and don't spam google
    headers = {
        "User-Agent":
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36"
    }
    response = requests.get(
        "https://www.google.com/search?q=" + company + "&tbm=nws&num=" + str(NUM_ARTICLES), headers=headers
    )
    soup = BeautifulSoup(response.content, "html.parser")

    print(company + " - " + str(response.status_code))

    for el in soup.select("div.SoaBEf"):
        date = el.select_one(".LfVVr").get_text()
        if "hour" in date or "day" in date or "minute" in date or "week ago" in date:
            if category == 1:
                news_results["Contractor"].append(company)
            elif category == 2:
                news_results["Topic"].append(company)
            news_results["Title"].append(el.select_one("div.MBeuO").get_text())
            news_results["Snippet"].append(el.select_one(".GI74Re").get_text())
            news_results["Date"].append(date)
            news_results["Source"].append(el.select_one(".NUnG9d span").get_text())
            news_results["Link"].append(el.find("a")["href"])

# Scrape Contractors News
news_results = {"Contractor":[], "Title":[], "Snippet":[], "Date":[], "Source":[], "Link":[]}

watchlist = pd.read_csv("watchlist.csv")['Companies']
for company in watchlist:
    scrape_news(company, 1) # category: 1
news_results = pd.DataFrame(news_results)
news_results.to_csv("news_contractors.csv", index=False)


# Scrape Topics News
news_results = {"Topic":[], "Title":[], "Snippet":[], "Date":[], "Source":[], "Link":[]}

topics = pd.read_csv("topics.csv")['Topics']
for topic in topics:
    scrape_news(topic, 2) # category: 2
news_results = pd.DataFrame(news_results)
news_results.to_csv("news_topics.csv", index=False)
