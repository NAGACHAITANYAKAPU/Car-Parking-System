from app import app
from app.routes import auth_routes,  admin_routes, profile_routes, default_routes, parking_routes, booking_routes, car_routes, feedback_routes, payment_routes, user_routes, pspace_routes
if __name__ == "__main__":
     app.run(host='0.0.0.0', port=5000, debug=True)