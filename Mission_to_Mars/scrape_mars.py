# import dependencies
import pymongo
import requests
from bs4 import BeautifulSoup
from splinter import Browser
import pandas as pd
import time

def scrape():

    # # connections to mongo db saving
    #  !!! need to run mongo in terminal  !!!!!
    conn = 'mongodb://localhost:27017'
    client = pymongo.MongoClient(conn)   # Define the 'classDB' database in Mongo

    # Here, db.students refers to the collection 'classroom '
    db = client.mars_db   # create mars database assign to db if doesn't exist, make connection
    collection = db.mars_coll  # assign collection to collection called articles,  called articles

    ### 1. NASA Mars News
    # Windows Chrome Browser for use with Splinter/ webpage does not load properly without
    executable_path = {'executable_path': './chromedriver.exe'}  # will see a new chrome browser
    browser = Browser('chrome', **executable_path, headless=False)
    url='https://mars.nasa.gov/news/'

    # try-except for when browser does not load fast enough, usually first scrape attempt.
    try:
        # Retrieve page with the requests module
        browser.visit(url)
        response = browser.html

        # loup through boutiful soup results, parse articles, make dictionary and enter into database
        soup = BeautifulSoup(response, 'html.parser')
        mars_news = soup.find('div', class_= "list_text")  #  class_="content_title")
        mars_news = mars_news.a.text
        news_p = soup.find('div', class_="article_teaser_body")
    except:
        time.sleep(5)
        browser.visit(url)
        response = browser.html

        # loup through boutiful soup results, parse articles, make dictionary and enter into database
        soup = BeautifulSoup(response, 'html.parser')
        mars_news = soup.find('div', class_= "list_text")  #  class_="content_title")
        mars_news = mars_news.a.text
        news_p = soup.find('div', class_="article_teaser_body")
        
    news_p = news_p.text
    mars_dict = {'title':mars_news,
                'paragraph':news_p}

    ### 2. JPL Mars Space Images - Featured Image
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'

    # use Splinter go to website and copy html text
    browser.visit(url)

    # Click thru the websites to get to large Size image
    browser.links.find_by_partial_text('FULL IMAGE').click()
    browser.links.find_by_partial_text('more info').click()

    response = browser.html
    soup = BeautifulSoup(response, 'html.parser')
    results = soup.find('figure')
    feature_link = results.a['href']
    featured_image_url = f'https://www.jpl.nasa.gov{feature_link}'
    print(featured_image_url)
    mars_dict.update({"featured_image_url" : featured_image_url})

    ### 3. Mars Facts
    # use Pandas to scrape the table containing facts about the planet including Diameter, Mass, etc.
    url = 'https://space-facts.com/mars/'
    tables = pd.read_html(url, index_col=0)
    tables
    specs = tables[0]
    specs = specs.rename(columns={1:'Mars'})
    specs.index.names = ['Description']

    # Use Pandas to convert the data to a HTML table string.
    mars_spec_table = specs.to_html()
    mars_dict.update({"Mars_Table" : mars_spec_table})
    specs

    ### 4. Mars Hemispheres
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    response = browser.html
    soup = BeautifulSoup(response, 'html.parser')

    # find the titles on the 4 mars hemispheres that will be used

    titles = soup.find_all('h3')
    title_list = []

    for title in titles:
        title_list.append(title.text)
    #     print(title.text)
    print(title_list)

    # Go to usgs and find the 4 hemispheres of mars, using Splinger's Browser
    # by clicking thru the pages. Store the titles and the image in the dictionary.
    hemisphere_image_urls = {}
    list_hem = []

    # loop thru the titles, click on the link to go to page, and scrape the image
    for title in title_list:
        browser.links.find_by_partial_text(title).click()
        response = browser.html
        soup = BeautifulSoup(response, 'html.parser')
        results = soup.find('li')  
        imag_url = results.a['href']
        
        # go back to orginal page
        url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
        browser.visit(url)
        response = browser.html
        
        # add title and image to dictionary then add it to the list
        hemisphere_image_urls.update({"title":title,"img_url":imag_url})
        list_hem.append(dict(hemisphere_image_urls))

    browser.quit()  # close the browser, we are done scraping

    # mars_dict.update({"hemisphere_image_urls" : list})
    mars_dict.update({"hemisphere_image_urls" : list_hem})

    # # Update Data Base with new data in dictionary
    collection.update({}, mars_dict, upsert=True)  # update database

    return mars_dict