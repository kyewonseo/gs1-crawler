import os
from pymongo import MongoClient
from gs1_crawler import config

# DB_HOST = os.environ['DB_DATASET_HOST']
# DB_PORT = os.environ['DB_DATASET_PORT']
# DB_NAME = os.environ['DB_DATASET_NAME']
# DB_USER = os.environ['DB_DATASET_USER']
# DB_PASSWORD = os.environ['DB_DATASET_PASSWORD']


DB_HOST = config.DATABASE_CONFIG['DB_DATASET_HOST']
DB_PORT = config.DATABASE_CONFIG['DB_DATASET_PORT']
DB_NAME = config.DATABASE_CONFIG['DB_DATASET_NAME']
DB_USER = config.DATABASE_CONFIG['DB_DATASET_USER']
DB_PASSWORD = config.DATABASE_CONFIG['DB_DATASET_PASSWORD']

class DataBase(object):
  def __init__(self):
    self.client = MongoClient('mongodb://' + DB_USER + ':' + DB_PASSWORD + '@' + DB_HOST + ':' + DB_PORT)
    # self.client = MongoClient('mongodb://' + DB_HOST + ':' + DB_PORT)
    self.db = self.client[DB_NAME]
