"""Server for EatWhere app."""

from flask import (Flask, render_template, request, flash, session,
                   redirect, jsonify, url_for)
from model import connect_to_db
import os
import crud
from jinja2 import StrictUndefined
from yelpapi import YelpAPI
import requests
from authlib.integrations.flask_client import OAuth
from datetime import timedelta


app = Flask(__name__)
app.secret_key = os.environ['APP_SECRET_KEY']

app.jinja_env.undefined = StrictUndefined
app.config['SESSION_COOKIE_NAME'] = 'google-login-session'
# app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=5)

API_KEY = os.environ['YELP_KEY']


# oAuth Setup
oauth = OAuth(app)
google = oauth.register(
    name='google',
    client_id=os.getenv("GOOGLE_CLIENT_ID"),
    client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
    access_token_url='https://accounts.google.com/o/oauth2/token',
    access_token_params=None,
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    authorize_params=None,
    api_base_url='https://www.googleapis.com/oauth2/v1/',
    # This is only needed if using openId to fetch user info
    userinfo_endpoint='https://openidconnect.googleapis.com/v1/userinfo',
    client_kwargs={'scope': 'openid email profile'},
)

@app.route("/")
def homepage():
    """View homepage."""

    if 'user_id' in session:

        return render_template("homepage.html")
    else:
        return render_template("new_user.html")


@app.route("/restaurants-search.json")
def get_restaurants_seach():
    location = request.args.get('location')
    longitude = request.args.get('longitude')
    latitude = request.args.get('latitude')
    categories = request.args.get('categories')
    price = request.args.get('price')
    sort_by = request.args.get('sort_by')
    

    yelp_res = YelpAPI(API_KEY).search_query(location=location, longitude=longitude, latitude=latitude, categories=categories,
                                             price=price, sort_by=sort_by, limit=5)

    return jsonify(yelp_res)

    # create new objects and pass in fields we need from yelp. Add liked field from database to the new object




# @app.route("/restaurant-details.json")
# def restaurant_details():

#     yelp_res = YelpAPI(API_KEY).business_query(id='amys-ice-creams-austin-3')

#     return jsonify(yelp_res)


@app.route('/new-user', methods=['POST'])
def register_user():
    """Create a new user."""

    email = request.form.get('email')
    password = request.form.get('password')

    user = crud.get_user_by_email(email)
    if user:
        flash("A user already exists with that email.")

    else:
        crud.create_user(email, password)
        user = crud.get_user_by_email(email)
        session['user_id'] = user.user_id
        flash("Your account is created successfully")

    return redirect('/')


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
    else:
        flash("Your email and password do not match")

    return redirect('/')


@app.route('/google-login')
def login():
    google = oauth.create_client('google')  # create the google oauth client
    redirect_uri = url_for('authorize', _external=True)
    return google.authorize_redirect(redirect_uri)


@app.route('/authorize')
def authorize():
    google = oauth.create_client('google')  # create the google oauth client
    # Access token from google (needed to get user info)
    token = google.authorize_access_token()
    # userinfo contains stuff u specificed in the scope
    resp = google.get('userinfo')
    user_info = resp.json()
    user = oauth.google.userinfo()  # uses openid endpoint to fetch user info
    email = user_info['email']

    if not crud.email_exist(email):
        crud.create_user(email)

    user = crud.get_user_by_email(email)
    session['user_id'] = user.user_id

    return redirect('/')


@app.route("/logout")
def process_logout():
    for key in list(session.keys()):
        session.pop(key)
    return redirect('/')



@app.route('/like/<yelp_id>')
def is_liked(yelp_id):
    user_id = session['user_id']
    user = crud.get_user_by_id(user_id)
    res = crud.get_restaurant_by_id(yelp_id)
    if not res:
        crud.create_restaurant(yelp_id)
        res = crud.get_restaurant_by_id(yelp_id)

    like = crud.get_like(user, res)

    if like:
        crud.delete_like(like)
    else:
        crud.create_like(user, res)

    return jsonify({'liked' : like == None})


if __name__ == '__main__':
    connect_to_db(app)
    app.run(host='0.0.0.0', debug=True)
