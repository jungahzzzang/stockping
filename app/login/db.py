import os
import json
from pymongo import MongoClient

abs_path = os.getcwd()

with open(abs_path+'/app/settings/config.json', 'r') as f:
    config = json.load(f)
    client = MongoClient(config['DB']['MONGO_URI'])
    db = client[config['DB']['DATABASE']]
    collection = db[config['DB']['COLLECTION']]

def get_db():
    return db
