"""CRUD operations."""

from model import db, User, connect_to_db


def create_user(email, password):
    """Create and return a new user."""

    user = User(email=email, password=password)

    db.session.add(user)
    db.session.commit()

    return user


def get_all_users():
    """Return all users."""
    return User.query.all()


def get_user_by_id(user_id):
    """Return user by id."""
    return User.query.get(user_id)


def get_user_by_email(email):
    """ Return user by email """

    return User.query.filter(User.email == email).first()


def password_match(email, password):
    """Check if password matches email."""
    return User.query.filter(User.email == email,
                             User.password == password).first()


if __name__ == '__main__':
    from server import app
    connect_to_db(app)
