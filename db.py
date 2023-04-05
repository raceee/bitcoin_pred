import pymongo
import yaml

with open('config.yaml', 'r') as file:
    mongo_creds = yaml.safe_load(file)

myclient = pymongo.MongoClient("mongodb+srv://{}:{}@bitcoinpred.mknwdgp.mongodb.net/?retryWrites=true&w=majority".format(mongo_creds["mongo_username"],mongo_creds["mongo_password"]))

mydb = myclient["bitcoin_data"]
print(mydb)

print(mydb.list_collection_names())