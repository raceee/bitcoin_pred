import pymongo
import yaml

with open('keys.yaml', 'r') as file:
    mongo_creds = yaml.safe_load(file)
print(mongo_creds["mongo_username"],mongo_creds["mongo_password"])
myclient = pymongo.MongoClient("mongodb+srv://race:{}@bitcoinpred.mknwdgp.mongodb.net/?retryWrites=true&w=majority".format(mongo_creds["mongo_password"]))

mydb = myclient["bitcoin_data"]
# print(mydb)

# print(mydb.list_collection_names())
# print(mydb["features"])

# my_delete = {"time":213123123}

# mydb["features"].delete_one(my_delete)

for i,data in enumerate(mydb["features"].find()):
    print(i)
    print(len(data["data"]))
    # break
    