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
    date_str = request.args.get('date')
    date_obj = datetime.strptime(date_str, '%Y-%m-%d')
    if crud.user_has_res_on_date(session["user_id"], date_obj):
        flash(f"You already have a tasting reservation on that day. Please select another day as we do not allow multiple reservations per day!")
        return redirect('/home')
    start = request.args.get('start')
    end = request.args.get('end')
    reservations = crud.get_reservations_for_day(date_obj)
    booked = set()
    for res in reservations:
        booked.add(datetime.combine(res.date, res.start_time)) 
    appt_times = []
    delta = timedelta(minutes = 30)
    null_start = False
    if not start: # if start time is not given, begin at midnight 
        null_start = True
        start = "00:00"
    start = datetime.strptime(date_str+start,'%Y-%m-%d%H:%M')
    start = datetime.min + math.ceil((start - datetime.min) / delta) * delta
    null_end= False
    if not end: # if end time is not given, last appointment should start at 11:30 pm
        end = datetime.strptime(date_str, '%Y-%m-%d') + timedelta(days=1) # set end datetime to midnight next day 
        null_end = True
    else:
        end = datetime.strptime(date_str+end,'%Y-%m-%d%H:%M')
        end = datetime.min + math.floor((end - datetime.min) / delta) * delta
    appt = start
    while appt < end:
        if appt not in booked: 
            appt_times.append(appt.time())
        appt = appt + timedelta(minutes = 30)
    return render_template('results.html', date = date_obj.date(), start=start.time(), end=end.time(), appt_times = appt_times, null_start=null_start, null_end = null_end)

@app.route('/book', methods = ['POST'])
def book():
    #check conflicting res
    if "user_id" not in session:
        flash("Please log in to view this page.")
        return redirect('/')
    user_id = session["user_id"]
    date_str = request.form.get("date")
    start_time_str = request.form.get("start_time")
    date = datetime.strptime(date_str,'%Y-%m-%d')
    start_time = datetime.strptime(start_time_str, '%H:%M:%S').time()
    if crud.res_booked_in_slot(date, start_time): 
         flash(f'Oh no! Someone has booked that time since you searched for available appointments. Please select another time.')
    else:
        res = crud.create_reservation(date, start_time, user_id)
        db.session.add(res)
        db.session.commit()
        flash(f"Booked! See you on {date_str} at {start_time_str} for your 30 minute reservation!")
    return redirect('/home')

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
    