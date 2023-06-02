"""Models for reservations app."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    """A user."""
    __tablename__ = "users"
    user_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    email = db.Column(db.String, unique=True)
    reservations = db.relationship("Reservation", back_populates = "user")

    def __repr__(self):
        return f'<User user_id={self.user_id} email={self.email}>'
    
class Reservation(db.Model):
    """A reservation."""
    __tablename__ = "reservations"
    reservation_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    date = db.Column(db.Date)
    start_time = db.Column(db.Time)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))

    user = db.relationship("User", back_populates = "reservations")

    def __repr__(self):
        return f'<Reservation reservation_id={self.reservation_id} user={self.user_id} date = {self.date} start_time = {self.start_time}>'

def connect_to_db(flask_app, db_uri="postgresql:///reservations", echo=True):
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    flask_app.config["SQLALCHEMY_ECHO"] = echo
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = flask_app
    db.init_app(flask_app)
    print("Connected to the db!")


if __name__ == "__main__":
    from server import app
    connect_to_db(app)
    app.app_context().push()