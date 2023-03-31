import requests
import pymongo
import yaml

with open('config.yaml', 'r') as file:
    mongo_creds = yaml.safe_load(file)

# dataset creation
market_array = requests.get("https://api.coingecko.com/api/v3/coins/bitcoin/market_chart/range?vs_currency=usd&from=1672531200&to=1680020825", headers=None).json()
zoinker_man = [{"time":i[0], "price": i[1] , "market_cap": j[1], "volume": k[1]} for i, j, k in zip(market_array["prices"], market_array["market_caps"], market_array["total_volumes"])]
zoinker_man = sorted(zoinker_man, key=lambda d: d['time']) 
zoinkers_dataset = []
for z in range(len(zoinker_man)-14):
    zoinkers_dataset.append({"data":zoinker_man[z:z+15]})

# upload to db
myclient = pymongo.MongoClient()
mydb = myclient["bitcoin_data"]
feature_collection = mydb["features"]
x = feature_collection.insert_many(zoinkers_dataset)
print(x.inserted_ids)