"""Models for Eatwhere app."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    """A user."""
    __tablename__ = 'users'
    user_id = db.Column(db.Integer,
                        primary_key=True,
                        autoincrement=True)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String)

    # preferences from user
    price_pref = db.Column(db.String) 
    yelp_rating_pref = db.Column(db.Float)
    review_count_pref = db.Column(db.Integer)
    categories_pref = db.Column(db.String)
    latitude_pref = db.Column(db.Float)
    longitude_pref = db.Column(db.Float)
    is_open_pref = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return f'<User user_id={self.user_id} email={self.email}>'


class Restaurant(db.Model):
    """A restaurant that user likes and saves it."""
    __tablename__ = 'restaurants'

    res_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    yelp_id = db.Column(db.String) # pull from Yelp API
    name = db.Column(db.String) # pull from Yelp API
    like = db.Column(db.Boolean, default=False)
    has_feedback = db.Column(db.Boolean, default=False)

    # timestamp optional

    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))


    def __repr__(self):
        return f"<Restaurant res_id={self.res_id} name={self.name}>"




def connect_to_db(flask_app, db_uri='postgresql:///eatwhere', echo=True):
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    flask_app.config['SQLALCHEMY_ECHO'] = echo
    flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.app = flask_app
    db.init_app(flask_app)

    print('Connected to the db!')


if __name__ == '__main__':
    from server import app

    # Call connect_to_db(app, echo=False) if your program output gets
    # too annoying; this will tell SQLAlchemy not to print out every
    # query it executes.

    connect_to_db(app)
