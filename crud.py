"""CRUD operations."""

from model import db, User, Reservation, connect_to_db

def create_user(email):
    """Create and return a new user."""
    user = User(email=email)
    return user

def create_reservation(start_datetime, user_id):
    """Create and return a new user."""
    res = Reservation(start_datetime = start_datetime, user_id = user_id)
    return res

def get_user_by_email(email):
    return User.query.filter(User.email == email).first()

def get_user_by_id(id):
    return User.query.filter(User.user_id == id).first()

if __name__ == '__main__':
    from server import app
    connect_to_db(app)
    app.app_context().push()