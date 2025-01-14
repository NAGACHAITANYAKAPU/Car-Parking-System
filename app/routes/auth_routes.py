from flask import render_template, request, redirect, url_for, session
from app import app
from app.models.supervisor import Supervisor
from app.models.user import User
from app.models.admin import Admin
from werkzeug.security import generate_password_hash, check_password_hash 
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


#     return render_template('users/login.html')
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_type = request.form.get("user_type")
        email = request.form.get("email").strip()
        password = request.form.get("password").strip()
        user = None
        if user_type == "supervisor": 
            user = Supervisor.get_by_email(email)
        elif user_type == "user": 
            user = User.get_by_email(email)
        elif user_type == "admin": 
            user = Admin.get_by_email(email)
        if not user:
            return "Email not found", 404

        is_valid_password = False
        if user_type == "supervisor":
            is_valid_password = Supervisor.check_password(user, password)
        elif user_type == "user":
            is_valid_password = User.check_password(user, password)
        elif user_type == "admin":
            is_valid_password = Admin.check_password(user, password)
        if not is_valid_password: 
            return render_template('users/login.html')

        session["user_id"] = str(user["_id"])
        session["user_type"] = user_type

        # Redirect to the appropriate dashboard after successful login
        if user_type == "supervisor":
            return redirect(url_for('supervisor_dashboard'))
        elif user_type == "user":
            return redirect(url_for('user_dashboard'))
        elif user_type == "admin":
            return redirect(url_for('admin_dashboard'))

    return render_template('users/login.html')



@app.route('/register_supervisor', methods=['GET', 'POST'])
def register_supervisor():
    try:
        if request.method == 'POST':
            email = request.form.get("email").strip()
            if Supervisor.exists_by_email(email):
                return "Email already registered", 400

            password = request.form.get("password").strip()
            confirm_password = request.form.get("confirm_password").strip()

            if password != confirm_password:
                return "Passwords do not match", 400

            data = {
                "user_name": request.form.get("user_name").strip(), 
                "email": email,
                "phone": request.form.get("phone").strip(), 
                "address": request.form.get("address").strip(),
                "password": generate_password_hash(password),
            }
            Supervisor.create(data)
            return redirect(url_for('login'))

        return render_template('supervisors/register_supervisor.html')
    except Exception as e:
        logger.error(f"Error during supervisor registration: {e}", exc_info=True)
        return "Internal Server Error", 500


@app.route('/register_user', methods=['GET', 'POST'])
def register_user():
    try:
        if request.method == 'POST':
            email = request.form.get("email").strip()
            if User.exists_by_email(email):
                return "Email already registered", 400

            password = request.form.get("password").strip()
            confirm_password = request.form.get("confirm_password").strip()

            if password != confirm_password:
                return "Passwords do not match", 400

            data = {
                "user_name": request.form.get("user_name").strip(),
                "dob": request.form.get("dob").strip(),
                "sex": request.form.get("sex"), 
                "email": email,
                "phone": request.form.get("phone").strip(),
                "address": request.form.get("address").strip(),
                "password": generate_password_hash(password)
            }
            User.create(data)
            return redirect(url_for('login'))

        return render_template('users/register_user.html')
    except Exception as e:
        logger.error(f"Error during user registration: {str(e)}")
        return "Internal Server Error", 500

@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    try:
        if request.method == 'POST':
            user_type = request.form.get("user_type")
            email = request.form.get("email")

            if user_type == "supervisor" and Supervisor.exists_by_email(email):
                session["reset_email"] = email
                session["user_type"] = user_type
                return redirect(url_for('enter_otp'))
            elif user_type == "user" and User.exists_by_email(email):
                session["reset_email"] = email
                session["user_type"] = user_type
                return redirect(url_for('enter_otp'))
            else:
                return "Email not found", 404

        return render_template('users/forgot_password.html')
    except Exception as e:
        logger.error(f"Error during forgot password process: {str(e)}")
        return "Internal Server Error", 500

@app.route('/enter_otp', methods=['GET', 'POST'])
def enter_otp():
    try:
        if request.method == 'POST':
            otp = request.form.get("otp")
            if otp == "11111":
                return redirect(url_for('reset_password'))
            else:
                return "Invalid OTP", 400

        return render_template('users/enter_otp.html')
    except Exception as e:
        logger.error(f"Error during OTP verification: {str(e)}")
        return "Internal Server Error", 500

@app.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
    try:
        if "reset_email" not in session:
            return redirect(url_for('login'))

        if request.method == 'POST':
            new_password = request.form.get("new_password")
            hashed_password = generate_password_hash(new_password)

            if session["user_type"] == "supervisor":
                Supervisor.collection.update_one(
                    {"email": session["reset_email"]},
                    {"$set": {"password": hashed_password}}
                )
            elif session["user_type"] == "user":
                User.collection.update_one(
                    {"email": session["reset_email"]},
                    {"$set": {"password": hashed_password}}
                )

            session.pop("reset_email", None)
            session.pop("user_type", None)
            return redirect(url_for('login'))

        return render_template('users/reset_password.html')
    except Exception as e:
        logger.error(f"Error during password reset: {str(e)}")
        return "Internal Server Error", 500

@app.route('/logout')
def logout():
    try:
        session.pop('user_id', None)
        session.pop('user_type', None)
        return redirect(url_for('login'))
    except Exception as e:
        logger.error(f"Error during logout: {str(e)}")
        return "Internal Server Error", 500




# register admin secret url
@app.route('/admin_secret', methods=['GET', 'POST'])
def register_admin():
    try:
        if request.method == 'POST':
            email = request.form.get("email").strip()
            if Admin.exists_by_email(email):
                return "Email already registered", 400

            password = request.form.get("password").strip()
            confirm_password = request.form.get("confirm_password").strip()

            if password != confirm_password:
                return "Passwords do not match", 400

            data = {
                "user_name": request.form.get("user_name").strip(), 
                "dob": request.form.get("dob").strip(),
                "sex": request.form.get("sex"), 
                    "email": email,
                    "phone": request.form.get("phone").strip(),
                    "address": request.form.get("address").strip(),
                "password": generate_password_hash(password)
            }
            Admin.create(data)
            return redirect(url_for('login'))

        return render_template('admin/register_admin.html')
    except Exception as e:
        logger.error(f"Error during admin registration: {str(e)}")
        return "Internal Server Error", 500