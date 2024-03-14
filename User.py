import datetime
import uuid
from flask import session, flash
from flask_login import UserMixin
from dotenv import load_dotenv
import pymongo
import os
import bcrypt
import json
from bson.objectid import ObjectId

# Connect to the MongoDB server using environment variables 
load_dotenv()
connection = pymongo.MongoClient("mongodb+srv://admin:iheartswe@project2cluster.w6vn0bs.mongodb.net/?retryWrites=true&w=majority")
db = connection['modelpyDB']
users = db.users

class User(UserMixin):

    def __init__(self, email, name, password, _id, strategies=None):

        self.email = email
        self.name = name
        self.password = password
        self._id = str(_id)

    def is_authenticated(self):
        return True
    def is_active(self):
        return True
    def is_anonymous(self):
        return False
    def get_id(self):
        return self._id


    @classmethod
    def get_by_email(cls, email):
        data = users.find_one({"email": email})
        if data is not None:
            return cls(**data)

    @classmethod
    def get_by_id(cls, _id):
        data = users.find_one({"_id": ObjectId(_id)})
        if data is not None:
            return cls(**data)

    @staticmethod
    def login_valid(email, password):
        verify_user = User.get_by_email(email)
        if verify_user is not None:
            return bcrypt.checkpw(password.encode('utf-8'),verify_user.password)
        return False

    @classmethod
    def register(cls, email, name, password):
        user = cls.get_by_email(email)
        if user is None:
            new_user = {"email": email, "name": name, "password": password}
            new_user_id = str(users.insert_one(new_user).inserted_id)
            print(new_user_id)
            #new_user.save_to_mongo()
            user_obj = cls(name, email, password, new_user_id)
            session['email'] = email
            return True
        else:
            return False

    def json(self):
        return {
            "email": self.email,
            "name": self.name,
            "_id": self._id,
            "password": self.password
        }

    def save_to_mongo(self):
        users.insert_one(self.json)