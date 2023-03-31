import pymongo
import yaml

with open('config.yaml', 'r') as file:
    mongo_creds = yaml.safe_load(file)

myclient = pymongo.MongoClient()

mydb = myclient["bitcoin_data"]
print(mydb)

print(mydb.list_collection_names())