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
from app.models.booking import Booking
from app.models.space import Pspace 
from app.models.car import Car
from flask import jsonify 



logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@app.route('/available_parking')
@login_required
def available_parking():
    # Fetch all active parking spaces
    parking_spaces = Pspace.find({"status": "active"})
    available_parking_spaces = [] 

    for space in parking_spaces:
        # Assuming each booking reduces the number of available slots by 1
        # You might need to adjust this logic based on how your bookings are structured
        booked_slots_count = Booking.count_documents({"space_id": space['space_id']}) 
        available_slots = space['num_spots'] - booked_slots_count

        # Only add space to list if there are available slots
        if available_slots > 0:
            space['available_slots'] = available_slots  # Add available slots info to space

            available_parking_spaces.append(space)
    return render_template('parking/available_parking.html', parking_spaces=available_parking_spaces)


@app.route('/user_book_parking/<space_id>', methods=['GET', 'POST'])
@login_required
def user_book_parking(space_id):
    if request.method == 'GET':
        parking_space = Pspace.find_one({"space_id": space_id, "status": "active"})
        if not parking_space:
            flash("Parking space not found or is not active.", "error")
            return redirect(url_for('available_parking'))

        user_id = session['user_id']
        user_cars = Car.find({"user_id": user_id})
        if user_cars.count() == 0:
            # Pass a flag to the template indicating no cars are available
            return render_template('parking/user_book_parking.html', parking_space=parking_space, no_cars=True)
        else:  
            return render_template('parking/user_book_parking.html', parking_space=parking_space, cars=user_cars, no_cars=False)
    

@app.route('/user_confirm_booking/<space_id>', methods=['POST'])
@login_required
def user_confirm_booking(space_id):
    print(request.form)
    booking_type = request.form.get('bookingType')
    car_id = request.form.get('car')
    duration_hours_str = request.form.get('durationInHours')
    start_time_str = request.form.get('fromTime')
    end_time_str = request.form.get('toTime')
    user_id = session.get('user_id')
    total_amount_str = request.form.get('totalCost')  # This comes as a string
    space_id = space_id

    car = Car.find_one({"_id": ObjectId(car_id)})
    if not car:
        flash("Car not found.", "error")
        return redirect(url_for('user_book_parking', space_id=space_id))

    booking = {
        "user_id": ObjectId(user_id),
        "car_id": ObjectId(car_id),
        "space_id": space_id,
        "amount": total_amount_str,
        "start_time": start_time_str,
        "end_time": end_time_str,
        "duration_hours": duration_hours_str,
        "booking_type": booking_type,
        "status": "not_paid", # "active" or "inactive"
        "created_at": datetime.now(), 
    }

    try:
        Booking.insert_one(booking)
        flash("Booking successful!", "success")
    except Exception as e:
        flash(f"Failed to save the booking: {e}", "error")

    return redirect(url_for('view_user_bookings', space_id=space_id))


@app.route('/user_book_day_month_parking/<space_id>', methods=['GET', 'POST'])
@login_required
def user_book_day_month_parking(space_id):
    if request.method == 'GET':
        parking_space = Pspace.find_one({"space_id": space_id, "status": "active"})
        if not parking_space:
            flash("Parking space not found or is not active.", "error")
            return redirect(url_for('available_parking'))

        user_id = session['user_id']
        user_cars = Car.find({"user_id": user_id})
        if user_cars.count() == 0:
            return render_template('parking/user_book_day_month_parking.html', parking_space=parking_space, no_cars=True)
        else:  
            return render_template('parking/user_book_day_month_parking.html', parking_space=parking_space, cars=user_cars, no_cars=False)


@app.route('/user_confirm_day_month_booking/<space_id>', methods=['POST'])
@login_required
def user_confirm_day_month_booking(space_id):
    print(request.form)
    booking_type = request.form.get('bookingType')
    car_id = request.form.get('car')
    duration_hours_str = request.form.get('durationInHours')
    start_time_str = request.form.get('fromTime')
    end_time_str = request.form.get('toTime')
    user_id = session.get('user_id')
    total_amount_str = request.form.get('totalCost')  # This comes as a string
    #  from rout get sapcie id
    space_id = space_id
    # Validation omitted for brevity


    car = Car.find_one({"_id": ObjectId(car_id)})
    if not car:
        flash("Car not found.", "error")
        return redirect(url_for('user_book_parking', space_id=space_id))

    booking = {
        "user_id": ObjectId(user_id),
        "car_id": ObjectId(car_id),
        "space_id": space_id,
        "amount": total_amount_str,
        "start_time": start_time_str,
        "end_time": end_time_str,
        "duration_hours": duration_hours_str,
        "booking_type": booking_type,
        "status": "not_paid", # "active" or "inactive"
        "created_at": datetime.now(), 

    }

    try:
        Booking.insert_one(booking)
        flash("Booking successful!", "success")
    except Exception as e:
        flash(f"Failed to save the booking: {e}", "error")

    return redirect(url_for('view_user_bookings', space_id=space_id))






@app.route('/view_user_bookings')
@login_required
def view_user_bookings():
    user_id = session.get('user_id')
    bookings = Booking.find({"user_id": ObjectId(user_id)})
    detailed_bookings = []
    for booking in bookings: 
        car = Car.find_one({"_id": booking['car_id']}) 
        booking['car'] = car
        detailed_bookings.append(booking) 
    return render_template('parking/view_user_bookings.html', bookings=detailed_bookings)




@app.route('/cancel_user_booking/<booking_id>', methods=['POST'])
@login_required
def cancel_user_booking(booking_id):
    # Ensure the user is attempting to cancel their own booking
    print(booking_id)
    user_id = session.get('user_id')
    
    # Optional: Check if the booking belongs to the user, for additional security
    booking = Booking.find_one({"_id": ObjectId(booking_id), "user_id": ObjectId(user_id)})
    if not booking:
        flash("Booking not found or you do not have permission to cancel this booking.", "error")
        return redirect(url_for('view_user_bookings'))

    # Update the booking status to "Cancelled"
    result = Booking.update_one(
        {"_id": ObjectId(booking_id), "user_id": ObjectId(user_id)},
        {"$set": {"status": "Cancelled"}}
    )

    if result.modified_count:
        flash("Booking cancelled successfully.", "success")
    else:
        flash("Failed to cancel booking. already cancelled", "error")

    return redirect(url_for('view_user_bookings'))
    
        