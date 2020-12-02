"""Models for Eatwhere app."""

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func, desc

db = SQLAlchemy()


class User(db.Model):
    """A user."""
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String)

    def __repr__(self):
        return f'<User user_id={self.user_id} email={self.email}>'


class Restaurant(db.Model):
    """A restaurant that user likes and saves it."""
    __tablename__ = 'restaurants'

    yelp_id = db.Column(db.String, primary_key=True)  # pull from Yelp API

    def __repr__(self):
        return f"<Restaurant yelp_id={self.yelp_id}>"


class Like(db.Model):
    """A like"""

    __tablename__ = 'likes'

    like_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    group_name = db.Column(db.String, default=None)

    yelp_id = db.Column(db.String, db.ForeignKey('restaurants.yelp_id'))
    res = db.relationship('Restaurant', backref='likes')

    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    user = db.relationship('User', backref='likes')

    def __repr__(self):
        return f"<Like like_id={self.like_id} group_name={self.group_name}>"


def connect_to_db(flask_app, db_uri='postgresql:///eatwhere', echo=True):
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    flask_app.config['SQLALCHEMY_ECHO'] = echo
    flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.app = flask_app
    db.init_app(flask_app)

    print('Connected to the db!')


if __name__ == '__main__':
    from server import app

    connect_to_db(app)
