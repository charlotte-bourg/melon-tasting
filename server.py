"""Server for melon tastings."""

from flask import (Flask, render_template, request,flash,session,redirect)
from model import connect_to_db,db
import crud

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
        flash("Created user account & logged in!")
    session["user_id"] = user.user_id
    return render_template('appt_search.html')

@app.route('/search')
def search_results():
    date = request.args.get('date')
    start = request.args.get('start')
    end = request.args.get('end')
    return render_template('results.html', date=date, start=start, end=end)


if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)
    app.app_context().push()
    