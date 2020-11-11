"""Server for EatWhere app."""

from flask import (Flask, render_template, request, flash, session,
                   redirect, jsonify)
from model import connect_to_db
import os
import crud
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
    if 'user_id' in session:
        return render_template("homepage.html")
    else:
        return render_template("new_user.html")


@app.route('/search')
def show_form():
    """Restaurant search"""

    return render_template('homepage.html')


@app.route("/restaurants-search.json")
def get_restaurants_seach():
    location = request.args.get('location', '')
    categories = request.args.get('categories', '')
    price = request.args.get('price', '')
    open_now = request.args.get('open_now', True)
    sort_by = request.args.get('sort_by', 'best_match')

    yelp_res = YelpAPI(API_KEY).search_query(location=location, categories=categories,
                                             price=price, open_now=open_now, sort_by=sort_by, limit=1)

    return jsonify(yelp_res)


@app.route('/new-user', methods=['POST'])
def register_user():
    """Create a new user."""

    email = request.form.get('email')
    password = request.form.get('password')

    user = crud.get_user_by_email(email)
    if user:
        flash("A user already exists with that email.")
        return redirect('/')

    else:
        crud.create_user(email, password)
        user = crud.get_user_by_email(email)
        session['user_id'] = user.user_id
        flash("Your account is created successfully")
        return redirect('/search')


@app.route('/user-login-page')
def user_login_page():
    """Show log in page """
    return render_template('login.html')


@app.route('/user-login', methods=['POST'])
def user_login():
    """Log a user in."""
    email = request.form.get("login-email")
    password = request.form.get("login-password")

    if crud.password_match(email, password):
        user = crud.get_user_by_email(email)
        session['user_id'] = user.user_id
        return redirect('/search')
    else:
        flash("Your email and password do not match")
        return redirect('/')

@app.route("/logout")
def process_logout():
    del session['user_id']
    flash('Logged out')
    
    return redirect('/')


if __name__ == '__main__':
    connect_to_db(app)
    app.run(host='0.0.0.0', debug=True)
