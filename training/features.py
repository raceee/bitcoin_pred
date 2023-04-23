import requests
import pymongo
import yaml
import time
import torch
WEEK = 604800

with open('config.yaml', 'r') as file:
    mongo_creds = yaml.safe_load(file)

def create_features(begin_time:int):
    '''
    parameters
    ----------
    begin_time: Unix time of the last entry in the database

    this is a funciton that grabs all of the prices and such and creates the feature sequences from begin_time to present
    '''
    begin_time = begin_time / 1000 # coingecko works on unix milisecond time
    market_array = requests.get("https://api.coingecko.com/api/v3/coins/bitcoin/market_chart/range?vs_currency=usd&from={}&to={}".format(begin_time, time.time()), headers=None).json()
    zoinker_man = [{"time":i[0], "price": i[1] , "market_cap": j[1], "volume": k[1]} for i, j, k in zip(market_array["prices"], market_array["market_caps"], market_array["total_volumes"])]
    zoinker_man = sorted(zoinker_man, key=lambda d: d['time']) 
    zoinkers_dataset = []
    for z in range(len(zoinker_man)-14):
        zoinkers_dataset.append({"data":zoinker_man[z:z+15]})
    return zoinkers_dataset

def get_collection(database_name:str, collection_name:str):
    '''
    parameters
    -----------
    database_name: string that is the name of the database trying to access
    collection_name: string that is the name of the collection you are trying to acess data from
    '''
    myclient = pymongo.MongoClient(mongo_creds["mongo_url"].format(mongo_creds["mongo_username"],mongo_creds["mongo_password"]))
    mydb = myclient[database_name]
    if collection_name in mydb.list_collections():
        return mydb[collection_name]
    else:
        print("Collection didn't exsist in the database so one was created")
        return mydb[collection_name]

def get_features_from_collection(collection, return_all_channels=True):
    '''
    parameters
    -----------
    collection: this is the acutal pymongo class that represents a collection from the database

    this function creates pytorch dataset 14 elements of the sequence are used to predict and the 15th is the element being predicted
    '''
    dataset_X = []
    dataset_Y = []
    for record in collection.find():
        record_feature_X = []
        record_feature_Y = []
        for i, data in enumerate(record["data"]):
            if i == len(record["data"]) - 1:
                record_feature_Y.append(torch.FloatTensor([data["price"], data["market_cap"], data["volume"]]))
            else:
                record_feature_X.append(torch.FloatTensor([data["price"], data["market_cap"], data["volume"]]))
        dataset_X.append(torch.vstack(record_feature_X).unsqueeze(dim=0))
        dataset_Y.append(torch.vstack(record_feature_Y))

    return torch.vstack(dataset_X), torch.vstack(dataset_Y)

def expand_db(collection):
    '''
    parameters
    ----------
    collection: this is a pymongo class that is the actual collection from the dataset 

    this function updates the database with new feature sequences sense the last unix time update
    '''
    # get last time stamp in the mongo db
    _, last_time = get_last(collection)
    time_diff = time.time() - (last_time/1000)
    if time_diff >= WEEK:
        new_data = create_features(last_time)
        myclient = pymongo.MongoClient(mongo_creds["mongo_url"].format(mongo_creds["mongo_username"], mongo_creds["mongo_password"]))
        mydb = myclient["bitcoin_data"]
        feature_collection = mydb["features"]
        feature_collection.insert_many(new_data)
    
def get_last(collection):
    """
    helper function for expand_db, this gets the last time stamp 
    """
    time__ = 0
    for record in collection.find():
        if record["data"][len(record["data"]) - 1]['time'] >= time__:
            newest_record = record
            time__ = record["data"][len(record["data"]) - 1]['time']
    return newest_record, time__