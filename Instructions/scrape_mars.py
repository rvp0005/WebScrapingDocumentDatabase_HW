import pandas as pd
from bs4 import BeautifulSoup
import requests
import os
from splinter import Browser
import time


def init_broswer():
    executable_path = {'executable_path': 'chromedriver.exe'}
    return Browser('chrome', **executable_path, headless=False)

def scrape():
    browser = init_broswer()

    url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    browser.visit(url)
    
    time.sleep(1)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    news_headline = soup.find_all(class_= 'content_title')[0].text
    news_text= soup.find_all(class_ = "article_teaser_body")[0].text

# ## JPL Mars Space Images- Featured Image

    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    results = soup.find_all(class_="carousel_item")

    for result in results:
        try:
            url_result = result.a['data-fancybox-href']

        except AttributeError as e:
            print(e)

    JPL_img = (f"https://www.jpl.nasa.gov/{url_result}")

# ## Mars Weather

    url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    current_weather= soup.find_all("p", class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text")[0].text

# ## Mars Facts
    url = 'https://space-facts.com/mars/'
    tables = pd.read_html(url)
    df = tables[0]
    df.columns= ["Characteristics", "Values"]
    df.head()
    html_table = df.to_html()
    mars_table = html_table
    html_table.replace('\n', " ")
    df.to_html("mars_facts.html")

# ## Mars Hemispheres
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    results = soup.find_all(class_= "description")

    url_list = []
    hemi_names = []
    img_url = []

    for result in results:
        try:
            url = result.a['href']
            hemi_names.append(result.h3.get_text())
            url_list.append(f"https://astrogeology.usgs.gov{url}")

        except AttributeError as e:
            print(e)

    browser.visit(url_list[0])
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    downloads= soup.find_all(class_= "downloads")

    for download in downloads:
        img_url.append(download.a['href'])

    browser.visit(url_list[1])
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    downloads= soup.find_all(class_= "downloads")

    for download in downloads:
        img_url.append(download.a['href'])

    browser.visit(url_list[2])
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    downloads= soup.find_all(class_= "downloads")

    for download in downloads:
        img_url.append(download.a['href'])
        
    browser.visit(url_list[3])
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    downloads= soup.find_all(class_= "downloads")

    for download in downloads:
        img_url.append(download.a['href'])

    Mars_hemispheres= dict(zip(hemi_names, img_url))

    links_to_use= []
    for key, val in Mars_hemispheres.items():
        links_to_use.append(val)


    Mars_data = {
        "news_headline": news_headline,
        "news_text": news_text,
        "featured_img": JPL_img,
        "weather" : current_weather,
        "Hemisphere_dict": Mars_hemispheres,
        "Mars_hemispheres": links_to_use
            }

    browser.quit()

    return Mars_data