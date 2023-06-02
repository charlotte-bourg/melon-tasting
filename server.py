"""Server for melon tastings."""

from flask import (Flask, render_template, request,flash,session,redirect)
from model import connect_to_db,db
import crud
from datetime import datetime, timedelta
import math

from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def login_page():
    return render_template('login.html')

@app.route('/login', methods = ['POST'])
def user_login():
    email = request.form.get("email")
    user = crud.get_user_by_email(email)
    print(user)
    if user:
        flash("Logged in!")
    else:
        user = crud.create_user(email)
        db.session.add(user)
        db.session.commit()
        flash("Created user account & logged in!")
    session["user_id"] = user.user_id
    return redirect('/home')

@app.route('/home')
def render_logged_in_homepage():
    return render_template('appt_search.html')

@app.route('/search')
def search_results():
    if "user_id" not in session:
        flash("Please log in to view this page.")
        return redirect('/')
    user = crud.get_user_by_id(session["user_id"])
    date = request.args.get('date')
    start = request.args.get('start')
    end = request.args.get('end')
    appt_times = []
    reservations = user.reservations
    delta = timedelta(minutes = 30)
    if not start: # if start time is not given, begin at midnight 
        start = "00:00"
    start = datetime.strptime(date+start,'%Y-%m-%d%H:%M')
    start = datetime.min + math.ceil((start - datetime.min) / delta) * delta
    if not end: # if end time is not given, last appointment should start at 11:30 pm
        end = datetime.strptime(date, '%Y-%m-%d') + timedelta(days=1) # set end datetime to midnight next day 
    else:
        end = datetime.strptime(date+end,'%Y-%m-%d%H:%M')
        end = datetime.min + math.floor((end - datetime.min) / delta) * delta
    # 
    return render_template('results.html', date=date, start=start, end=end)


@app.route('/reservations')
def get_results():
    if "user_id" not in session:
        flash("Please log in to view this page.")
        return redirect('/')
    user = crud.get_user_by_id(session["user_id"])
    print(user.reservations)
    return render_template('user_details.html', reservations = user.reservations)


if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)
    app.app_context().push()
    