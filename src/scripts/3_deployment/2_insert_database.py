import json
import logging
import pandas as pd
import pymongo

from scripts import utils
from config import data_config, mongo_config

logging.basicConfig(level=logging.INFO)

pickleDataFolder = data_config.YELP_PICKLE_DATA_FOLDER
modelFolder = data_config.MODELS_FOLDER

logging.info("Creating database collections...")
client = pymongo.MongoClient(mongo_config.URI)
client.drop_database(mongo_config.DB)

restaurantCollection = client[mongo_config.DB]["restaurants"]
restaurantCollection.create_index([("longlat_location", pymongo.GEO2D)])
trendCollection = client[mongo_config.DB]["trends"]
topicCollection = client[mongo_config.DB]["topics"]

def dataframe_to_dicts(df):
	"""
	Helper function turning a dataframe into a list of rows/data points
	for easier insertion of the data into MongoDB collections.
	The dataframe is converted into a list of rows,
	where each row is a dictionary {"column_name":"value", ...}.
	"""
	rowToDict = lambda row: { colName: row[colIdx] for colIdx, colName in enumerate(df.columns.values) }
	return [ rowToDict(row) for row in df.values ]

logging.info("Storing restaurants into the database...")
restaurantDF = utils.load_dataframe_from_pickle("restaurant_database.df", pickleDataFolder)
restaurants = dataframe_to_dicts(restaurantDF)
restaurantCollection.insert(restaurants)

logging.info("Storing trends into the database...")
trendDF = utils.load_dataframe_from_pickle("trend_database.df", pickleDataFolder)
trends = dataframe_to_dicts(trendDF)
trendCollection.insert(trends)

logging.info("Storing topics into the database...")
labelFile = "topic_labels.lda{}".format(data_config.LDA_TOPICS_COUNT)
with open(os.path.join(modelFolder, labelFile), 'r') as fp:
	topics = json.load(fp)
topics = { unicode(topicIdx): topicLabel for topicIdx, topicLabel in enumerate(topics) }
topicCollection.insert([topics])
