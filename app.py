from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars


app = Flask(__name__)
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars")

@app.route('/')
def index():
    query_mongo = mongo.db.mars.find_one()

    if query_mongo:
        news = query_mongo['news_title']
        news_para = query_mongo['news_para'] 
        featured_image = query_mongo['featured_image_url']
        mars_weather = query_mongo['m_weather.text']
        table = query_mongo['facts_html']
        hemisphere = query_mongo['hemisphere_image_url']

    return render_template('index.html',
    news=news,
    news_para=news_para,
    featured_image=featured_image,
    mars_weather=mars_weather,
    table=table,
    hemisphere=hemisphere)

@app.route('/scrape')
def scrape():
    mars = mongo.db.mars
    data = scrape_mars.scrape()
    mars.update(
        {},
        data,
        upsert=True
    )
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)
 

