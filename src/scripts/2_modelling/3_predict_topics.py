import collections
import itertools
import logging
import os
import pandas as pd

import gensim.corpora
import gensim.models

from config import data_config
from scripts import utils

# Create handler because gensim writes a lot on INFO...
logger = logging.getLogger(__name__)
sh = logging.StreamHandler()
sh.setLevel(logging.INFO)
logger.setLevel(logging.INFO)
logger.addHandler(sh)

pickleDataFolder = data_config.YELP_PICKLE_DATA_FOLDER
modelFolder = data_config.MODELS_FOLDER
ldaTopicsCount = data_config.LDA_TOPICS_COUNT

# Load data and models
logging.info("Loading restaurant file...")
restaurantDF = utils.load_dataframe_from_pickle("restaurant_original.df", pickleDataFolder)

logging.info("Loading -preprocessed- review file...")
reviewDF = utils.load_dataframe_from_pickle("review_preprocessed.df", pickleDataFolder)

logging.info("Loading topic prediction model...")
dictFile = os.path.join(modelFolder, "reviews_all.dict")
mmFile = os.path.join(modelFolder, "reviews_all.mm")
ldaFile = os.path.join(modelFolder, "reviews_all.lda{}".format(ldaTopicsCount))

dictionary = gensim.corpora.Dictionary.load(dictFile)
ldaModel = gensim.models.ldamodel.LdaModel.load(ldaFile)
#ldaModel = gensim.models.ldamulticore.LdaMulticore.load(ldaFile)

# Concatenate reviews for each restaurant
logging.info("Preparing data for topic prediction...")
byRestReviews = pd.DataFrame()
byRestReviews["reviews"] = reviewDF.groupby("business_id").preproc_text.apply(list)  

# Predict topics for each restaurant
logging.info("Predicting topics...")
def topicPredictionFn(restReviews):
    words = itertools.chain(*restReviews)
    restaurantBOW = dictionary.doc2bow(words)
    predictedTopics = ldaModel[restaurantBOW]
    return { topicIdx: topicProb for topicIdx, topicProb in predictedTopics }
topicsDF = pd.DataFrame()
topicsDF["predicted_topics"] = byRestReviews.reviews.apply(topicPredictionFn)
topicsDF.reset_index(level=0, inplace=True)

# Store results to disk
utils.save_dataframe_to_pickle(topicsDF, "restaurant_topics.df", pickleDataFolder)
