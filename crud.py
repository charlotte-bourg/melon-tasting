"""CRUD operations."""

from model import db, User, Reservation, connect_to_db

def create_user(email):
    """Create and return a new user."""
    user = User(email=email)
    return user

def create_reservation(date, start_time, user_id):
    """Create and return a new user."""
    res = Reservation(date = date, start_time = start_time, user_id = user_id)
    return res

def get_reservations_for_day(date):
    """Create and return a new user."""
    return Reservation.query.filter(Reservation.date == date).all()

def user_has_res_on_date(user_id, date):
    if Reservation.query.filter(Reservation.date == date, Reservation.user_id == user_id).first():
        return True
    else:
        return False

def get_user_by_email(email):
    return User.query.filter(User.email == email).first()

def get_user_by_id(id):
    return User.query.filter(User.user_id == id).first()

if __name__ == '__main__':
    from server import app
    connect_to_db(app)
    app.app_context().push()