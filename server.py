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


def restaurant_from_yelp(biz, like):
    biz_res = {
        "categories": biz["categories"][0]["title"],
        "name": biz["name"],
        "image_url": biz["image_url"],
        "rating": biz["rating"],
        "review_count": biz["review_count"],
        "price": biz["price"],
        "address": biz["location"]["display_address"],
        "url": biz["url"],
        "id": biz["id"],
        "liked": like != None,
        "lat": biz["coordinates"]["latitude"],
        "long": biz["coordinates"]["longitude"]
    }
    return biz_res


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

    yelp_list = yelp_res["businesses"]
    biz_list = []

    user_id = session['user_id']
    user = crud.get_user_by_id(user_id)

    for idx in range(len(yelp_list)):
        biz = yelp_list[idx]
        yelp_id = biz["id"]
        res = crud.get_restaurant_by_id(yelp_id)
        like = crud.get_like(user, res)
        biz_res = restaurant_from_yelp(biz, like)
        biz_list.append(biz_res)

    return jsonify({"businesses": biz_list})


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


@app.route('/google-authorize')
def authorize():
    google = oauth.create_client('google')  # create the google oauth client
    token = google.authorize_access_token()
    resp = google.get('userinfo')
    user_info = resp.json()
    user = oauth.google.userinfo()  # uses openid endpoint to fetch user info
    email = user_info['email']

    if not crud.email_exist(email):
        crud.create_user(email)

    user = crud.get_user_by_email(email)
    session['user_id'] = user.user_id

    return redirect('/')


@app.route('/facebook-authorize')
def fb_auth():
    pass


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

    return jsonify({'liked': like == None})


@app.route('/vote-result.json')
def vote_result():
    res = crud.get_restaurant_with_most_likes()
    yelp_id = res.yelp_id

    yelp_res = YelpAPI(API_KEY).business_query(id=yelp_id)

    res_detail = restaurant_from_yelp(yelp_res, like=None)

    return jsonify(res_detail)


if __name__ == '__main__':
    connect_to_db(app)
    app.run(host='0.0.0.0', debug=True)
