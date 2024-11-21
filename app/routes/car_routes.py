from flask import render_template, request, redirect, url_for, session, flash
from app import app
from app.models.supervisor import Supervisor
from app.models.user import User 
from .decorators import login_required
import logging
from datetime import datetime, timedelta
from bson.objectid import ObjectId
from app.models.feedback import Feedback
from app.models.payment import Payment
from app.models.booking import Booking
from app.models.car import Car
from app.models.space import Pspace
from flask import jsonify


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)



@app.route('/add_car', methods=['GET', 'POST'])
@login_required
def add_car():
    # get current user details id
    user_id = session['user_id']
    if request.method == 'POST':
        car_type = request.form['carType']
        car_make = request.form['carMake']
        car_model = request.form['carModel']
        car_color = request.form['carColor']
        car_number_plate = request.form['carNumberPlate']

        # Assuming you have a function to save car details
        # This is a placeholder, implement saving logic based on your database
        Car.save_car_details({
            'user_id': user_id,  # Assuming you have access to the logged-in user's ID
            'type': car_type,
            'make': car_make,
            'model': car_model,
            'color': car_color,
            'number_plate': car_number_plate
        })

        flash('Car added successfully!', 'success')
        return redirect(url_for('user_dashboard'))  # Redirect to a relevant page after adding

    # Render add car form on GET request
    return render_template('car/add_car.html')


# view cars
@app.route('/view_cars')
@login_required
def view_cars():
    user_id = session['user_id']
    cars = Car.find({"user_id": user_id})
    return render_template('car/view_cars.html', cars=cars)


@app.route('/edit_user_car/<car_id>', methods=['GET', 'POST'])
@login_required
def edit_user_car(car_id):
    if session.get("user_type") != "user":
        flash("Unauthorized access.", "error")
        return redirect(url_for('login'))

    if request.method == 'POST':
        # Process form submission for updating car details
        print(request.form)
        update_data = {
            "make": request.form['make'],
            "model": request.form['model'], 
            "color": request.form['color'],
            "number_plate": request.form['number_plate'] 
        }
        result = Car.update_one({"_id": car_id, "user_id": session.get('user_id')}, {"$set": update_data})

        if result.modified_count:
            flash("Car updated successfully.", "success")
        else:
            flash("Failed to update car or car not found.", "error")

        return redirect(url_for('view_cars'))
    else:
        # Display the form with existing data for the car
        print(car_id)
        print(session.get('user_id'))
        car = Car.find_one({"_id": ObjectId(car_id), "user_id": session.get('user_id')})
        print(car)
        if not car:
            flash("Car not found.", "error")
            return redirect(url_for('view_cars'))
        return render_template('car/edit_user_car.html', car=car)



@app.route('/delete_user_car/<car_id>')
@login_required
def delete_user_car(car_id): 
    user_id = session['user_id']
    car = Car.find_one({"_id": ObjectId(car_id), "user_id": user_id})
    if not car:
        flash("Car not found.", "error")
        return redirect(url_for('view_cars'))

    # Call delete_car with car_id directly
    Car.delete_car(car_id)
    flash('Car deleted successfully!', 'success')
    return redirect(url_for('view_cars'))
