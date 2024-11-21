from app import mongo
from werkzeug.security import generate_password_hash, check_password_hash
from bson import ObjectId


class Car:
    collection = mongo.db.cars

    @classmethod
    def save_car_details(cls, car_details):
        cls.collection.insert_one(car_details)


    @classmethod
    def delete_car(cls, car_id):
        # Convert car_id to ObjectId and delete the car
        query = {"_id": ObjectId(car_id)}
        return cls.collection.delete_one(query)


    @classmethod
    def update_one(cls, query, update):
        query = {"_id": ObjectId(query["_id"])}
        return cls.collection.update_one(query, update)


        
    @classmethod
    def find(cls, query):
        return cls.collection.find(query)
    

    @classmethod
    def find_one(cls, query): 
        return cls.collection.find_one(query)