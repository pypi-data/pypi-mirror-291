from typing import Any
import json
import pymongo
import pandas as pd
class mogodb_operation:
    def __init__(self, client_url: str, database_name: str, collection_name: str):
        self.client_url = client_url
        self.database_name = database_name
        self.collection_name = collection_name

    def create_client(self):
        client = pymongo.MongoClient(self.client_url)
        return client

    def create_database(self):
        client = self.create_client()
        database = client[self.database_name]
        return database

    def create_collection(self, collection_name: str = None):
        database = self.create_database()
        collection = database[collection_name]
        return collection

    def insert_record(self, record: dict, collection_name: str):
        if type(record) == list:
            for data in record:
                if type(data) != dict:
                    raise TypeError(" record must be of type dict")
            collection = self.create_collection(collection_name)
            collection.insert_many(record)
        elif type(record) == dict:
            collection = self.create_collection(collection_name)
            collection.insert_one(record)

    def bulk_insert(self, datafile: str, collection_name: str = None):
        self.path = datafile
        if self.path.endswith('.csv'):
            data = pd.read_csv(self.path, encoding='utf-8')
        elif self.path.endswith('.xlsx'):
            data = pd.read_excel(self.path, encoding='utf-8')

        datajson = json.load(data.to_json(orient='records'))
        collection = self.create_collection(collection_name)
        collection.insert_many(datajson)