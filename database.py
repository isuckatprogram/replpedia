import pymongo
import os

client = pymongo.MongoClient(os.getenv('mongourl'))
db = client['replpedia']

def add_wiki(info):
  db['wikis'].insert_one(info)

def get_wiki(info):
  return db['wikis'].find_one(info)

def delete(info):
  db['wikis'].delete_one(info)

def update(old,new):
  newquery = { "$set": new}
  db['wikis'].update_one(old,newquery)

def get_wikis(info):
  return db['wikis'].find(info)