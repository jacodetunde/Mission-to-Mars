# Import dependencies
from flask import Flask, render_template
from flask_pymongo import PyMongo
import scraping

# Flask set-up
app = Flask(__name__)
# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

# Create the webpages routes
#Home page
@app.route("/")
def index():
    mars = mongo.db.mars.find_one()
    return render_template("index.html",mars=mars)
# Scrape Button
@app.route("/scrape")
def scrape():
    # mars = mongo.db.mars
    mars_data = scraping.scrape_all()
    # mars.update({}, mars_data, upsert=True)
    return render_template("index.html", image_url=mars_data["image_url"])
    # return "Scraping Successful!"


# App run
if __name__ == "__main__":
    app.run(debug=True)