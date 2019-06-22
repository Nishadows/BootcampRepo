# Dependencies
from bs4 import BeautifulSoup
import requests
import pandas as pd
from splinter import Browser
import time

def scrape():
    # Scrape nasa.gov

    print("****NASA.gov start ***")
    nasa_url = "https://mars.nasa.gov/news/"
    nasa_response = requests.get(nasa_url)
    soup = BeautifulSoup(nasa_response.text, 'html.parser')
    
    print(soup.prettify())

    news_title = soup.find(class_="content_title").text.replace("\n","")
    news_p = soup.find(class_="rollover_description_inner").text.replace("\n","")

    print(news_title)
    print(news_p)
    print("****NASA.gov end ***")

    # Scrape jpl.nasa.gov

    print("****JPL.NASA.gov start ***")
    jpl_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"

    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=True)

    browser.visit(jpl_url)
    time.sleep(1)

    featured_image_url = browser.find_by_tag("article").first['style'].split("\"")
    featured_image_url = "https://www.jpl.nasa.gov"+featured_image_url[1]

    print(featured_image_url)
    print("****JPL.NASA.gov end ***")

    # Scrape twitter.com

    print("****twitter.com start ***")
    twitter_url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(twitter_url)
    time.sleep(1)

    tweets = browser.find_by_id("stream-items-id").find_by_tag("li").first
    mars_weather = tweets.find_by_tag("p").first.text

    print(mars_weather)
    print("****twitter.com end ***")

    # Scrape space-facts.com

    print("****space-facts.com start ***")
    spacefacts_url = "https://space-facts.com/mars/"
    facts_response = requests.get(spacefacts_url)
    facts_soup = BeautifulSoup(facts_response.text, 'lxml')

    print(facts_soup.prettify())

    facts = facts_soup.find("table")
    tables = pd.read_html(str(facts))
    df = tables[0]
    df.columns = ["Facts","Value"]

    # df.head(20)

    html_table = df.to_html()
    html_table=html_table.replace('\n', '')

    print(html_table)
    print("****space-facts.com end ***")

    # Scrape usgs.gov

    print("****usgs.gov start ***")
    usgs_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"

    browser.visit(usgs_url)
    time.sleep(1)

    hemisphere_divs = browser.find_by_tag("div").find_by_css(".description")

    hemisphere_urls = []

    for link in hemisphere_divs:    
        hemisphere_urls.append({"title": link.find_by_tag("a").text, "img_url": link.find_by_tag("a")['href']})

    print(hemisphere_urls)

    hemisphere_image_urls = []

    for i in hemisphere_urls:
        browser.visit(i['img_url'])
        time.sleep(1)
        
        img_url = browser.find_by_tag('li').first 
        hemisphere_image_urls.append({"title": i['title'], "img_url": img_url.find_by_tag("a")['href']})

    print(hemisphere_image_urls)
    print("****usgs.gov start ***")

    #Store scrape results in dictionary

    print("****Store scrape results start ***")

    scrape_dict = {}

    scrape_dict["NASA"] = [news_title, news_p]
    scrape_dict["JPL"] = featured_image_url
    scrape_dict["TWITTER"] = mars_weather
    scrape_dict["SPACE_FACTS"] = html_table
    scrape_dict["USGS"] = hemisphere_image_urls

    print(scrape_dict)

    print("****Store scrape results end ***")

    return scrape_dict



