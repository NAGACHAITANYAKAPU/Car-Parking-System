from app import mongo
from werkzeug.security import generate_password_hash, check_password_hash
from bson import ObjectId, errors
# app/models/supervisor.py

class Supervisor:
    collection = mongo.db.supervisors

    @classmethod
    def create(cls, data):  
        return cls.collection.insert_one(data)

    @classmethod
    def get_all_supervisors(cls):
        return cls.collection.find()

    @classmethod
    def check_password(cls, supervisor, password):  
        return check_password_hash(supervisor["password"], password)

    @classmethod
    def get_by_email(cls, email):
        return cls.collection.find_one({"email": email})
    @classmethod
    def get_supervisor_name_by_id(cls, supervisor_id):
        try:
            # print(f"Querying for supervisor_id: {supervisor_id}")
            supervisor = cls.collection.find_one({"_id": ObjectId(supervisor_id)}) 
            return supervisor['name'] if supervisor else None
        except errors.PyMongoError as e:
            print(f"An error occurred while fetching the supervisor's name: {e}")
            return None

    @classmethod
    def exists_by_email(cls, email):
        return cls.collection.find_one({"email": email}) is not None

    @classmethod
    def get_supervisor_by_id(cls, supervisor_id):
        try:
            # print(f"Querying for supervisor_id: {supervisor_id}")
            return cls.collection.find_one({"_id": ObjectId(supervisor_id)}) 
        except errors.PyMongoError as e:
            print(f"An error occurred while fetching the supervisor: {e}")
            return None