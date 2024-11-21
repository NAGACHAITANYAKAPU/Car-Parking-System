from app import mongo
from werkzeug.security import generate_password_hash, check_password_hash
from bson import ObjectId, errors

class User:
    collection = mongo.db.users

    @classmethod
    def create(cls, data):
        return cls.collection.insert_one(data)

    @classmethod
    def get_by_email(cls, email):
        return cls.collection.find_one({"email": email})

    @classmethod
    def check_password(cls, user, password):
        return check_password_hash(user["password"], password)

    @classmethod
    def exists_by_email(cls, email):
        return cls.collection.find_one({"email": email}) is not None

    @classmethod
    def get_user_name_by_id(cls, user_id):
        try:
            user = cls.collection.find_one({"_id": ObjectId(user_id)}) 
            # print(f"Found user: {user}")
            return user['name'] if user else None
        except errors.PyMongoError as e:
            print(f"An error occurred while fetching user name: {e}")
            return None

