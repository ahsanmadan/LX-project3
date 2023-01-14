import os
from os.path import join, dirname
from dotenv import load_dotenv
from flask import (
    Flask,
    render_template,
    request,
    jsonify,
    redirect,
    url_for
)
import certifi
from pymongo import MongoClient

dotenv_path = join(dirname(__file__), "env")
load_dotenv(dotenv_path)

uri = os.environ.get("MONGODB_URI")
db_name = os.environ.get("DB_NAME")

client = MongoClient("uri", tlsCAFile=certifi.where())
db = client[db_name]

app = Flask(__name__)



@app.route("/")
def main():
    return render_template("index.html")


@app.route("/restaurants", methods=["GET"])
def get_restaurants():
    # This api endpoint should fetch a list of restaurants
    restaurants = list(db.restaurants.find({}, {"_id": False}))
    return jsonify({"result": "success", "restaurants": restaurants})


@app.route("/restaurant/create", methods=["POST"])
def create_restaurant():
    name = request.form.get('name')
    categories = request.form.get('categories')
    location = request.form.get('location')
    longitude = request.form.get('longitude')
    latitude = request.form.get('latitude')
    link = request.form.get("link")
    doc = {
        'name': name,
        'categories': categories,
        'location': location,
        'center': [longitude, latitude],
        "link": link
    }
    db.restaurants.insert_one(doc)
    return jsonify(
        {"result": "success", "msg": "Restaurant successfully added"}
    )


@app.route("/restaurant/delete", methods=["POST"])
def delete_restaurant():
    name = request.form.get('name')
    db.restaurants.delete_one({'name': name})
    return jsonify(
        {"result": "success", "msg": "Restaurant successfully deleted"}
    )


if __name__ == "__main__":
    app.run("0.0.0.0", port=5000, debug=True)