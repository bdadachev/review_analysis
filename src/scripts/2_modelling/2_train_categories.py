from collections import Counter
import itertools
import logging
import os
import pandas as pd
import pickle
from sklearn.feature_extraction import DictVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.linear_model import LogisticRegression

from analysis import category_prediction
from config import data_config
from scripts import utils

logging.basicConfig(level=logging.INFO)

pickleDataFolder = data_config.YELP_PICKLE_DATA_FOLDER
modelFolder = data_config.MODELS_FOLDER

logging.info("Loading restaurant file...")
restaurantDF = utils.load_dataframe_from_pickle("restaurant_original.df", pickleDataFolder)

logging.info("Loading -preprocessed- review file...")
reviewDF = utils.load_dataframe_from_pickle("review_preprocessed.df", pickleDataFolder)

logging.info("Merging the two dataframes...")
groupedReviewDF = pd.DataFrame()
groupedReviewDF["reviews"] = reviewDF.groupby("business_id").preproc_text.apply(list)
del reviewDF
groupedReviewDF = groupedReviewDF.merge(restaurantDF[["categories"]],
                                     	left_index=True, right_index=True)
del restaurantDF
groupedReviewDF.reset_index(level=0, inplace=True)

logging.info("Preparing category labels (i.e., remove categories with low counts)...")
# remove exotic categories (with number of restaurants / positive examples < 50)
# also remove the "Restaurants" category
catCounts = Counter(cat for cats in groupedReviewDF.categories for cat in cats)
catFilterFn = lambda cats: [cat for cat in cats if cat != "Restaurants" and catCounts[cat] >= data_config.MINIMUM_CATEGORY_COUNTS]
groupedReviewDF.categories = groupedReviewDF.categories.apply(catFilterFn)

logging.info("Preparing data for classification: transforming reviews to TF-IDF vectors...")
toDictFn = lambda reviews: Counter(itertools.chain(*reviews))
dictVec = DictVectorizer(sparse=True)
dictX = dictVec.fit_transform(groupedReviewDF.reviews.apply(toDictFn))
tfidfTrans = TfidfTransformer()
trainX = tfidfTrans.fit_transform(dictX)
trainY = groupedReviewDF.categories.values

logging.info("Training the category predictor...")
classifier = LogisticRegression(class_weight="auto")
cp = category_prediction.CategoryPredictor(classifier)
cp.fit(trainX, trainY)

logging.info("Saving the category predictor to file...")
modelFile = os.path.join(modelFolder, "categorypredictor_linreg.pickle")
with open(modelFile, 'w') as fp:
    pickledObj = {
        "dictVectorizer": dictVec,
        "tfidfTransformer": tfidfTrans,
        "categoryPredictor": cp,
    }
    pickle.dump(pickledObj, fp)



