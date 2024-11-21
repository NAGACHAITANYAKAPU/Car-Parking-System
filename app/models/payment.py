from app import mongo
from werkzeug.security import generate_password_hash, check_password_hash

class Payment:
    collection = mongo.db.payments



    @classmethod
    def insert_one(cls, payment):
        cls.collection.insert_one(payment)


    @classmethod
    def find(cls, query):
        return cls.collection.find(query)