"""CRUD operations."""

from model import db, User, Restaurant, Like, connect_to_db


def create_user(email, password=None):
    """Create and return a new user."""

    user = User(email=email, password=password)

    db.session.add(user)
    db.session.commit()

    return user

def create_restaurant(yelp_id):
    """Create and return a new restaurant."""

    res = Restaurant(yelp_id=yelp_id)

    db.session.add(res)
    db.session.commit()

    return res


def create_like(user, res, is_liked=False):
    """ Change like attribute to true """

    like = Like(user=user, res=res, is_liked=is_liked)

    db.session.add(like)
    db.session.commit()

    return like
    

def get_all_users():
    """Return all users."""
    return User.query.all()

def get_all_restaurants():
    """ Return all restaurants"""
    return Restaurant.query.all()


def get_user_by_id(user_id):
    """Return user by id."""
    return User.query.get(user_id)

def get_restaurant_by_id(yelp_id):
    """Return restaurant by id."""
    return Restaurant.query.get(yelp_id)

def get_user_by_email(email):
    """ Return user by email """

    return User.query.filter(User.email == email).first()


def password_match(email, password):
    """Check if password matches email."""
    return User.query.filter(User.email == email,
                             User.password == password).first() != None

def email_exist(email):
    """ Check if email matches"""
    return User.query.filter(User.email == email).first() != None


if __name__ == '__main__':
    from server import app
    connect_to_db(app)
