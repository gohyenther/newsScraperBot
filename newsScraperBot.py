import time
import requests
import pandas as pd
from random import randint
from bs4 import BeautifulSoup

NUM_ARTICLES = 3 # Top n headlines
EXCLUSIONS = ["Simply Wall St", "Simply Wall Street", "www.tradingview.com", "Trade Brains", "MarketWatch"] # Exclude news from these sources
TITLE_EXCLUSIONS = ["Dividend", "Stock"]

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
        source = el.select_one(".NUnG9d span").get_text()
        date = el.select_one(".LfVVr").get_text()
        title = el.select_one("div.MBeuO").get_text()
        snippet = el.select_one(".GI74Re").get_text()
        link = el.find("a")["href"]

        exclude_flag = False

        # news source exclusions:
        if source in EXCLUSIONS: exclude_flag = True

        # news title exclusions:
        for title_exclude in TITLE_EXCLUSIONS:
            if title_exclude in title:
                exclude_flag = True
                break
        
        # only include the past 7 days of latest news
        if not exclude_flag and ("hour" in date or "day" in date or "minute" in date or "week ago" in date):
            if category == 1:
                news_results["Contractor"].append(company)
            elif category == 2:
                news_results["Topic"].append(company)
            news_results["Title"].append(title)
            news_results["Snippet"].append(snippet)
            news_results["Date"].append(date)
            news_results["Source"].append(source)
            news_results["Link"].append(link)


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
