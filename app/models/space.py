from app import mongo
from werkzeug.security import generate_password_hash, check_password_hash 

class Pspace:
    collection = mongo.db.parking_spaces


    @classmethod
    def insert_one(cls, data):
        return cls.collection.insert_one(data)
    
    @classmethod
    def find_one(cls, query):
        return cls.collection.find_one(query)
    

    @classmethod
    def update_one(cls, query, data):
        return cls.collection.update_one(query, data)
    
    @classmethod
    def find(cls, query):
        return cls.collection.find(query)

    

    @classmethod
    def delete_one(cls, query):
        return cls.collection.delete_one(query)