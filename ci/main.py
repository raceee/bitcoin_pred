import torch
from model import SequenceModel
import features
from pymongo import DESCENDING
import io
import requests
import time
import yaml
TIME_GAP = 604800 * 2
import os 
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
with open('keys.yaml', 'r') as file:
    mongo_creds = yaml.safe_load(file)

# connect to the database
model_collection = features.get_collection("bitcoin_data", "model_weights")

# set the state_dict
most_recent_document = model_collection.find_one(sort=[('_id', DESCENDING)], limit=1)
state_dict_bytes = io.BytesIO(most_recent_document["params"])

model = SequenceModel()
model.load_state_dict(torch.load(state_dict_bytes))

# call the coingeecko api
begin_time = time.time() - TIME_GAP # coingecko works on unix milisecond time
market_array = requests.get("https://api.coingecko.com/api/v3/coins/bitcoin/market_chart/range?vs_currency=usd&from={}&to={}".format(begin_time, time.time()), headers=None).json()
zoinker_man = [{"time":i[0], "price": i[1] , "market_cap": j[1], "volume": k[1]} for i, j, k in zip(market_array["prices"], market_array["market_caps"], market_array["total_volumes"])]
zoinker_man = sorted(zoinker_man, key=lambda d: d['time'])

# feed the model the coingecko data
input_array = zoinker_man[-14:]
last_time = int(zoinker_man[len(zoinker_man)-1]["time"])
input_array = torch.vstack([torch.FloatTensor([data["price"], data["market_cap"], data["volume"]]) for data in input_array]).unsqueeze(dim=0)
print(model(input_array).item())
pred = model(input_array).item()

# tweet
import tweepy
client = tweepy.Client(bearer_token=mongo_creds["twitter_api_bearer_tok"], consumer_key=mongo_creds["twitter_api_key"], consumer_secret=mongo_creds["twitter_api_secret"], access_token=mongo_creds["twitter_api_access_tok"], access_token_secret=mongo_creds["twitter_api_access_tok_secret"])

tweet_text = """One hour from {} the price of $BTC will be ${} \n \n \n #neuralnetwork #crypto #ml""".format(last_time, pred)

client.create_tweet(text=tweet_text)

# TODO: #3 #2 do I have to do min max scaling for the input for the model in the field?