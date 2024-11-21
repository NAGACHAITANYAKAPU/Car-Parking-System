from flask import render_template, request, redirect, url_for, session, flash
from app import app
from .decorators import login_required
import logging
from datetime import datetime, timedelta
from bson.objectid import ObjectId 
from flask import jsonify 
from app.models.user import User 
from app.models.payment import Payment
from app.models.space import Pspace
from app.models.booking import Booking



@app.route('/add_parking_space', methods=['GET', 'POST'])
@login_required
def add_parking_space():
    if session.get("user_type") != "supervisor":
        flash("Unauthorized access.", "error")
        return redirect(url_for('supervisor_dashboard'))

    if request.method == 'POST':
        space_id = request.form['space_id']
        supervisor_id = session.get('user_id')
        num_spots = int(request.form['num_spots'])  # Number of spots input

        # Check if a parking space with the same ID already exists for this supervisor
        existing_space = Pspace.find_one({"space_id": space_id, "supervisor_id": supervisor_id})
        if existing_space:
            new_num_spots = existing_space['num_spots'] + num_spots
            Pspace.update_one({"_id": existing_space['_id']}, {"$set": {"num_spots": new_num_spots}})
            flash("Number of spots updated for the existing parking space.", "success")
            return redirect(url_for('supervisor_dashboard'))

        # Proceed to create a new parking space if it does not exist
        type_of_space = request.form['type_of_space']
        schedule = {day: request.form.getlist(day) for day in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']}
        status = "pending"
        cost_per_hr = request.form['cost_per_hr']
        cost_per_day = request.form['cost_per_day']
        cost_per_month = request.form['cost_per_month']

        parking_space_data = {
            "space_id": space_id,
            "type_of_space": type_of_space,
            "schedule": schedule,
            "status": status,
            "supervisor_id": supervisor_id,
            "num_spots": num_spots,  # Include the number of spots in the document
            "cost": {
                "per_hr": cost_per_hr,
                "per_day": cost_per_day,
                "per_month": cost_per_month,
            }
        }
        Pspace.insert_one(parking_space_data)
        flash("Parking space added successfully!", "success")
        return redirect(url_for('supervisor_dashboard'))

    return render_template('parking/add_parking_space.html')



@app.route('/view_parking_spaces')
@login_required
def view_parking_spaces():
    if session.get("user_type") != "supervisor":
        flash("Unauthorized access.", "error")
        return redirect(url_for('login'))

    supervisor_id = session.get('user_id')
    parking_spaces = Pspace.find({"supervisor_id": supervisor_id})
    return render_template('supervisors/view_parking_spaces.html', parking_spaces=parking_spaces)

@app.route('/view_parking_space_detail/<space_id>')
@login_required
def view_parking_space_detail(space_id):
    if session.get("user_type") != "supervisor":
        flash("Unauthorized access.", "error")
        return redirect(url_for('login'))
     

    parking_space = Pspace.find_one({"space_id": space_id, "supervisor_id": session.get('user_id')})
    if not parking_space:
        flash("Parking space not found.", "error")
        return render_template('supervisors/view_parking_space_detail.html', parking_space=parking_space)


    return render_template('supervisors/view_parking_space_detail.html', parking_space=parking_space)


@app.route('/delete_parking_space/<space_id>', methods=['POST'])
@login_required
def delete_parking_space(space_id):
    if session.get("user_type") != "supervisor":
        flash("Unauthorized access.", "error")
        return redirect(url_for('login'))

    supervisor_id = session.get('user_id')
    result = Pspace.delete_one({"space_id": space_id, "supervisor_id": supervisor_id})
    
    if result.deleted_count:
        flash("Parking space deleted successfully.", "success")
    else:
        flash("Failed to delete parking space or space not found.", "error")
    
    return redirect(url_for('view_parking_spaces'))



@app.route('/edit_parking_space/<space_id>', methods=['GET', 'POST'])
@login_required
def edit_parking_space(space_id):
    if session.get("user_type") != "supervisor":
        flash("Unauthorized access.", "error")
        return redirect(url_for('login'))

    if request.method == 'POST':
        # Process form submission for updating parking space details
        update_data = {
            "type_of_space": request.form['type_of_space'],
            "num_spots": int(request.form['num_spots']),
            "cost": {
                "per_hr": request.form['cost_per_hr'],
                "per_day": request.form['cost_per_day'],
                "per_month": request.form['cost_per_month'],
            }
            # Add other fields as necessary
        }
        result = Pspace.update_one({"space_id": space_id, "supervisor_id": session.get('user_id')}, {"$set": update_data})
        
        if result.modified_count:
            flash("Parking space updated successfully.", "success")
        else:
            flash("Failed to update parking space or space not found.", "error")

        return redirect(url_for('view_parking_spaces'))
    else:
        # Display the form with existing data for the parking space
        parking_space = Pspace.find_one({"space_id": space_id, "supervisor_id": session.get('user_id')})
        if not parking_space:
            flash("Parking space not found.", "error")
            return redirect(url_for('view_parking_spaces'))
        return render_template('supervisors/edit_parking_space.html', parking_space=parking_space)



@app.route('/view_booked_spaces')
@login_required
def view_booked_spaces():
    if session.get("user_type") != "supervisor":
        flash("Unauthorized access.", "error")
        return redirect(url_for('login')) 
    supervisor_id = session.get('user_id') 
    parking_spaces = Pspace.find({"supervisor_id": supervisor_id}) 
    all_bookings = []

    for space in parking_spaces:
        # For each parking space, find related bookings
        space_bookings = Booking.find({"space_id": space['space_id']})
        for booking in space_bookings:
            all_bookings.append(booking) 
    return render_template('supervisors/view_booked_spaces.html', booked_spaces=all_bookings)


@app.route('/view_payments')
@login_required
def view_payments():
    if session.get("user_type") != "supervisor":
        flash("Unauthorized access.", "error")
        return redirect(url_for('login'))

    payments = Payment.find({})
    return render_template('supervisors/view_payments.html', payments=payments)
