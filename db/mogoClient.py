from pymongo import MongoClient
import datetime

client = MongoClient('mongodb://localhost:27017/iBlog2')

iblogDB = client.get_database('iBlog2')


def getCateAll():
    return iblogDB.find()