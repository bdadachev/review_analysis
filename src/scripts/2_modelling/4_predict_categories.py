import collections
import cPickle
import itertools
import logging
import os
import pandas as pd

import gensim.corpora
import gensim.models

from config import data_config
from scripts import utils

logging.basicConfig(level=logging.INFO)

pickleDataFolder = data_config.YELP_PICKLE_DATA_FOLDER
modelFolder = data_config.MODELS_FOLDER

logging.info("Loading restaurant file...")
restaurantDF = utils.load_dataframe_from_pickle("restaurant_original.df", pickleDataFolder)

logging.info("Loading -preprocessed- review file...")
reviewDF = utils.load_dataframe_from_pickle("review_preprocessed.df", pickleDataFolder)

logging.info("Loading category prediction model...")
categoryPredictorsFile = os.path.join(modelFolder, "categorypredictor_linreg.pickle")
with open(categoryPredictorsFile, 'r') as fp:
    categoryPredictors = cPickle.load(fp)

logging.info("Preparing data for category prediction...")
byRestReviews = pd.DataFrame()
byRestReviews["reviews"] = reviewDF.groupby("business_id").preproc_text.apply(list)
# note: size of byRestReviews < nbRestaurants since some restaurants have no reviews

logging.info("Predicting categories...")
toDictFn = lambda restReviews: collections.Counter(itertools.chain(*restReviews))
dictX = categoryPredictors["dictVectorizer"].transform(byRestReviews.reviews.apply(toDictFn))
tfidfX = categoryPredictors["tfidfTransformer"].transform(dictX)
byRestReviews["predicted_categories"] = categoryPredictors["categoryPredictor"].predict(tfidfX)
# merge back with restaurantDF because we will need true categories
restaurantDF = restaurantDF.join(byRestReviews.predicted_categories)

logging.info("Filtering true categories from predictions...")
def catFilterFn(row):
    # predicted_categories: list of categories
    # if no reviews for restaurant, prediction impossible, so get nan when joining
    # if all predictions are negative, get empty list
    if isinstance(row["predicted_categories"], list):
        return [ cat for cat in row["predicted_categories"] if cat not in row["categories"] ]
    else:
         return []
restaurantDF["predicted_categories"] = restaurantDF.apply(catFilterFn, axis=1)
categoriesDF = restaurantDF[ ["predicted_categories"] ]
categoriesDF.reset_index(level=0, inplace=True)

utils.save_dataframe_to_pickle(categoriesDF, "restaurant_categories.df", pickleDataFolder)
