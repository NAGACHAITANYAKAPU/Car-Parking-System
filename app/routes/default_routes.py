#  hi index route
from flask import render_template
from app import app
from app.models.supervisor import Supervisor
from flask import redirect, url_for, session

@app.route('/')
def index(): 
    # Check if user is already logged in
    if 'user_id' in session:
        # Check the user type and redirect to the appropriate dashboard
        if session["user_type"] == "supervisor":
            return redirect(url_for('supervisor_dashboard'))
        elif session["user_type"] == "user":
            return redirect(url_for('user_dashboard'))

    supervisors = Supervisor.get_all_supervisors()  # Assuming you have this method in your Supervisor model
    return render_template('index.html', supervisors=supervisors)