# import dependencies
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo  # incorporate flask into pymongo
import scrape_mars
import pymongo

app = Flask(__name__)

# app.config['MONGO_URI'] = 'mongodb://localhost:27017/mars_db'
# mongo = PyMongo(app)
# mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_db")

conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)   # Define the 'classDB' database in Mongo

db = client.mars_db   # create mars database assign to db if doesn't exist, make connection
collection = db.mars_coll  # assign collection to collection called articles,  called articles

@app.route('/')
def index():
    mars_dict = collection.find_one()   # pass in collection mars_coll
    return render_template('index.html', mars_dict = mars_dict) # listing=listing, html_string=html_table)


@app.route('/scrape')
def scrape():
    mars_dict = scrape_mars.scrape()  # run the scrape function
    collection.update({}, mars_dict, upsert=True)
    # mongo.db.collection.update({}, mars_dict, upsert=True)  # update Mongo database
    # print("test1: ", mars_dict)
    return redirect('/')  # redirect to homepage index.html

if __name__ == "__main__":
    app.run(debug=True)
