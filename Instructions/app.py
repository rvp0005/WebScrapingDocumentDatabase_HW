from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__, static_url_path='', static_folder="")

# Use flask_pymongo to set up mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/Mars_HW_app")

@app.route("/")
def home():
    
    planet_data = mongo.db.collection.find_one()
    
    return render_template("index.html", data=planet_data)


@app.route("/scrape")
def scrape():
    Mars_data = scrape_mars.scrape()
    mongo.db.collection.update({}, Mars_data, upsert=True)
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)