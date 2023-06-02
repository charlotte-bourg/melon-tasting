"""CRUD operations."""

from model import db, User, connect_to_db

def create_user(email):
    """Create and return a new user."""
    user = User(email=email)
    return user

def get_user_by_email(email):
    return User.query.filter(User.email == email).first()

if __name__ == '__main__':
    from server import app
    connect_to_db(app)
    app.app_context().push()