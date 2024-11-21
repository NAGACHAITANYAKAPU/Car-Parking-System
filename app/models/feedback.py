from app import mongo
from werkzeug.security import generate_password_hash, check_password_hash

class Feedback:
    collection = mongo.db.feedback