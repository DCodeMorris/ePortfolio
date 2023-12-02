from pymongo import MongoClient
from bson.objectid import ObjectId
import urllib.parse


class AnimalShelter(object):
    _instance = None  # Class variable to store the instance

    def __new__(cls, _password, _username='aacUser'):
        if cls._instance is None:
            cls._instance = super(AnimalShelter, cls).__new__(cls)
            username = urllib.parse.quote_plus(_username)
            password = urllib.parse.quote_plus(_password)
            cls._instance.client = MongoClient(f'mongodb://{username}:{password}@localhost:27017/?authSource=AAC')
            cls._instance.dataBase = cls._instance.client['AAC']
        return cls._instance

    def __init__(self, _password, _username='aacUser'):
        # Property variables
        self.records_updated = 0
        self.records_matched = 0
        self.records_deleted = 0

    def createRecord(self, data):
        if data:
            _insert_valid = self.dataBase.animals.insert_one(data)
            return _insert_valid.acknowledged
        else:
            return False  # or raise an exception if needed

    def getRecordId(self, post_id):
        _data = self.dataBase.animals.find_one({'_id': ObjectId(post_id)})
        return _data

    def getRecordCriteria(self, criteria):
        if criteria:
            _data = list(self.dataBase.animals.find(criteria, {'_id': 0}))
        else:
            _data = list(self.dataBase.animals.find({}, {'_id': 0}))
        return _data

    def updateRecord(self, query, new_value):
        if not query:
            raise Exception("No search criteria is present.")
        elif not new_value:
            raise Exception("No update value is present.")
        else:
            _update_valid = self.dataBase.animals.update_many(query, {"$set": new_value})
            self.records_updated = _update_valid.modified_count
            self.records_matched = _update_valid.matched_count
            return _update_valid.modified_count > 0

    def deleteRecord(self, query):
        if not query:
            raise Exception("No search criteria is present.")
        else:
            _delete_valid = self.dataBase.animals.delete_many(query)
            self.records_deleted = _delete_valid.deleted_count
            return _delete_valid.deleted_count > 0
