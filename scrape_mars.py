
import pymongo
import pandas as pd
import numpy as np
import os
from splinter import Browser
from bs4 import BeautifulSoup as bs
import time

def scrape():

    # get_ipython().system('which chromedriver')

    executable_path={"executable_path":"/usr/local/bin/chromedriver"}
    browser=Browser("chrome",**executable_path,headless=False)

    url="https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"

    browser.visit(url)


    # ## Nasa Mars News

    time.sleep(2)
    html = browser.html
    soup = bs(html, 'lxml')

    mars_news = soup.find(string=True,class_="content_title")
    news_title=mars_news.text
    
    print(news_title)

    mars_para = soup.find(string=True,class_="article_teaser_body")
    news_para=mars_para.text
    
    print(news_para)

    
    # ## JPL Mars Space Images - Featured Image

    url_1="https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    time.sleep(2)

    browser.visit(url_1)
    
    # Allows you to click a link titled FULL IMAGE on the url opened with above url_1
    browser.click_link_by_partial_text('FULL IMAGE')
    time.sleep(5)
    browser.click_link_by_partial_text('more info')

    html = browser.html
    soup = bs(html, 'lxml')

    jpl = soup.find(class_="main_image")

    jpl_url=jpl["src"]

    featured_image_url=f"https://www.jpl.nasa.gov{jpl_url}"

    print(featured_image_url)


    # ## Mars Weather

    url_2="https://twitter.com/marswxreport?lang=en"

    browser.visit(url_2)

    html = browser.html
    soup = bs(html, 'lxml')

    m_weather = soup.find(class_="TweetTextSize")
    print(m_weather.text)

    mars_weather= m_weather.text.split("\n")[0]
    print(mars_weather)
    time.sleep(2)

    # ## Mars Facts

    url_3= "http://space-facts.com/mars/"

    mars_facts=pd.read_html(url_3)
    print(mars_facts)

    facts= mars_facts[0]

    facts_html = facts.to_html()

    facts_html=facts_html.replace('\n', '')

    print(facts_html)


    # # Mars Hemispheres

    # In[24]:


    url_4="https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"

    browser.visit(url_4)

    html = browser.html
    soup = bs(html, 'lxml')

    #goes to the class called "description" and extracts out all the 
    #texts of it and places into a list
    mars_hem = soup.find_all(class_="description")

    empty_list=[]
    for x in range(4):
        y = mars_hem[x].h3.text
        empty_list.append(y)
    #list containing all the names of the hemispheres
    print(empty_list)

    img_url_list=[]
    for c in range(4):
        browser.click_link_by_partial_text(empty_list[c])
        soup_1=bs(browser.html,"lxml")
        for link in soup_1.find_all('a', href=True,text="Sample"):
            img_link=link['href']
            img_url_list.append(img_link)
        # go back to previous page
            browser.visit(url_4)
    #list containing urls for all the full size images 
    print(img_url_list)

    hemisphere_image_url=[]
    for x in range(4):
        z={"title":empty_list[x],"img_url":img_url_list[x]}
        hemisphere_image_url.append(z)
    print(hemisphere_image_url)

    hemisphere_image_url

    return({
        "news_title":news_title,
        "news_para":news_para,
        "featured_image_url":featured_image_url,
        "m_weather.text":m_weather.text,
        "mars_weather":mars_weather, 
        "facts_html":facts_html,
        "hemisphere_image_url":hemisphere_image_url
        })



   