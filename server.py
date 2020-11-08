"""Server for EatWhere app."""

from flask import (Flask, render_template, request, flash, session,
                   redirect, jsonify)
from model import connect_to_db
import os
# import crud
from jinja2 import StrictUndefined
from yelpapi import YelpAPI
import requests


app = Flask(__name__)
app.secret_key = 'dev'
app.jinja_env.undefined = StrictUndefined

API_KEY = os.environ['YELP_KEY']


@app.route("/")
def homepage():
    """View homepage."""
    # return render_template("index.html")
    return redirect('/search-form')

@app.route('/search-form')
def show_form():
    """Show event search form"""

    return render_template('search-form.html')

@app.route("/restaurants-search")
def get_restaurants_seach():
    location = request.args.get('location', '')
    categories = request.args.get('categories', '')
    price = request.args.get('price', '')
    open_now = request.args.get('open_now', True)
    sort_by = request.args.get('sort_by', 'best_match')

    yelp_res = YelpAPI(API_KEY).search_query(location=location, categories=categories, price=price, open_now=open_now, sort_by=sort_by)

    return jsonify(yelp_res)



if __name__ == '__main__':
    connect_to_db(app)
    app.run(host='0.0.0.0', debug=True)        