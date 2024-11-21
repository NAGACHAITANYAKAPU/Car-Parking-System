from app import mongo
from werkzeug.security import generate_password_hash, check_password_hash




class Booking:
    collection = mongo.db.booking


    @classmethod
    def count_documents(cls, query):
        return cls.collection.count_documents(query)
    
    @classmethod
    def update_one(cls, query, new_values):
        return cls.collection.update_one(query, new_values)


    @classmethod
    def find_one(cls, query):
        return cls.collection.find_one(query)
    
    @classmethod
    def find(cls, query):
        return cls.collection.find(query)
    
    
    @classmethod
    def insert_one(cls, booking):
        return cls.collection.insert_one(booking)
