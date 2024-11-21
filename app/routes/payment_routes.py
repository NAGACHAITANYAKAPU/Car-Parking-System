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


@app.route('/show_payment_form/<booking_id>', methods=['GET'])
@login_required
def show_payment_form(booking_id):
    booking = Booking.find_one({"_id": ObjectId(booking_id)})
    if booking and booking['status'] == 'not_paid':
        amount = booking['amount']  # Assuming 'amount' field exists in your booking document
        return render_template('payments/user_pay_form.html', amount=amount, booking_id=booking_id)
    else:
        flash("Invalid booking or payment already processed.")
        return redirect(url_for('view_user_bookings'))
    


@app.route('/process_payment/<booking_id>', methods=['POST'])
@login_required
def process_payment(booking_id):
    payment_mode = request.form['paymentMode']
    amount = request.form['amount']
    payment_details = {}

    # Collect payment details based on payment mode
    if payment_mode == "Credit Card":
        payment_details = {
            "cardNumber": request.form.get('cardNumber'),
            "expiryDate": request.form.get('expiryDate'),
            "cvv": request.form.get('cvv')
        }
    elif payment_mode == "Checking Account":
        payment_details = {
            "accountNumber": request.form.get('accountNumber'),
            "routingNumber": request.form.get('routingNumber')
        }

    # Here you would integrate with a payment gateway to process the payment
    # For simplicity, we'll assume the payment is always successful

    # Insert payment record into 'payments' collection with payment details
    payment_record = {
        "bookingID": ObjectId(booking_id),
        "Amount": amount,
        "PaymentMode": payment_mode,
        "Details": payment_details,
        "Status": "Paid",
        "Date": datetime.now().strftime("%Y-%m-%d"),
        "Time": datetime.now().strftime("%H:%M:%S")
    }
    Payment.insert_one(payment_record)

    # Update booking status to 'paid'
    Booking.update_one({"_id": ObjectId(booking_id)}, {"$set": {"status": "paid"}})

    flash("Payment processed successfully.")
    return redirect(url_for('view_user_bookings'))

    
    
    
