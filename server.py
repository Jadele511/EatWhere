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
    userinfo_endpoint='https://openidconnect.googleapis.com/v1/userinfo',  # This is only needed if using openId to fetch user info
    client_kwargs={'scope': 'openid email profile'},
)



@app.route("/")
def homepage():
    """View homepage."""
    
    if 'email' in session:
        return render_template("homepage.html")
    else:
        return render_template("new_user.html")


@app.route("/restaurants-search.json")
def get_restaurants_seach():
    location = request.args.get('location', '')
    categories = request.args.get('categories', '')
    price = request.args.get('price', '')
    open_now = request.args.get('open_now', True)
    sort_by = request.args.get('sort_by')

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

    else:
        crud.create_user(email, password)
        user = crud.get_user_by_email(email)
        session['email'] = user.email
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
        session['email'] = user.email
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
    token = google.authorize_access_token()  # Access token from google (needed to get user info)
    resp = google.get('userinfo')  # userinfo contains stuff u specificed in the scope
    user_info = resp.json()
    user = oauth.google.userinfo()  # uses openid endpoint to fetch user info
    
    session['profile'] = user_info
    return render_template("homepage.html")


@app.route("/logout")
def process_logout():
    for key in list(session.keys()):
        session.pop(key)   
    return redirect('/')


if __name__ == '__main__':
    connect_to_db(app)
    app.run(host='0.0.0.0', debug=True)
