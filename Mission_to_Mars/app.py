from flask import Flask, render_template, redirect
# from pymongo import PyMongo
from flask_pymongo import PyMongo  # incorporate flask into pymongo
from splinter import Browser
from bs4 import BeautifulSoup
import scrape_mars
import pymongo

app = Flask(__name__)

# conn= 'mongodb://localhost:27017'
# client = pymongo.MongoClient(conn)
# db = client.mars_db
# mars_coll = db.collection

app.config['MONGO_URI'] = 'mongodb://localhost:27017/mars_db'
mongo = PyMongo(app)

@app.route('/')
def index():
    mars_dict = mongo.db.mars_coll.find_one()
    # diction = mars_coll.find()  #  = mongo.db.listing.find_one()
    # html_table = diction.Mars_table
    return render_template('index.html', mars_dict = mars_dict) # listing=listing, html_string=html_table)


@app.route('/scrape')
def scrape():
    
    
    #route to open browser, useing chrome driver, to
    executable_path = { 'executable_path': './chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)  # object, 
    
    
    # mars_dict = scrape_mars.scrape()
    # mongo.db.listings.update({}, listing, upsert=True)
# upsert- if doesn't exist create, if exist update record
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)

    return redirect('/')  # redirect to index.html

# To pull data use data=mars_coll.find({})  everything  {name: 'title'}

if __name__ == "__main__":
    app.run(debug=True)
