# Import Dependencies
from flask import Flask, jsonify, render_template, redirect
from pymongo import MongoClient
import scrape_mars


# Create App
app = Flask(__name__)

# Create Mongo connection
client = MongoClient("mongodb://localhost:27017")
db = client.scrape_db


# Create routes
# Root route
@app.route("/")
def index():
    try: 
        scrapedata = db.scrapemars.find_one()
        if scrapedata is None:
            return render_template('index_landing.html', message="Data not yet scraped")
        else:
            return render_template('index.html', listings=scrapedata)
    except:
        return "Unknow error occurred, check the Database connection and try again"


# Scrape route
@app.route("/scrape")
def scrapemars():
    # Scrape data
    scraperesults = scrape_mars.scrape() 

    scrapecoll = db.scrapemars
    
    scrapecoll.update({}, scraperesults, upsert=True)
    return redirect("/", code=302)


if __name__ == '__main__':
    app.run(debug=True)

