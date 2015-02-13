import logging
import pandas as pd

from config import data_config
from scripts import utils

logging.basicConfig(level=logging.INFO)

rawDataFolder = data_config.YELP_RAW_DATA_FOLDER
pickleDataFolder = data_config.YELP_PICKLE_DATA_FOLDER

# Load the raw JSON data
logging.info("Reading raw business and review files...")
businessDF = utils.load_yelp_dataset("business", rawDataFolder)
reviewDF = utils.load_yelp_dataset("review", rawDataFolder)

# Filter restaurant data
logging.info("Removing data relating to businesses other than restaurants...")
isRestaurantColumn = pd.Series([ "Restaurants" in cats for cats in businessDF.categories ])
restaurantDF = businessDF[ isRestaurantColumn ]
restaurantReviewDF = reviewDF[ reviewDF.business_id.isin(restaurantDF.business_id) ]
# NB: some restaurants may be closed, but we keep them because the review data are precious.
logging.info("Found {} restaurants and {} restaurant reviews.".format(restaurantDF.shape[0], restaurantReviewDF.shape[0]))

# Clean a bit and drop fields we are not going to use
logging.info("More cleaning...")
pd.options.mode.chained_assignment = None # to disable some false positive warnings.
# ... the business dataset
categoryFilterFn = lambda categories: filter(lambda x: x != "Restaurants", categories)
restaurantDF["categories"] = restaurantDF.categories.apply(categoryFilterFn)
restaurantDF.drop("neighborhoods", axis=1, inplace=True)
restaurantDF.drop("type", axis=1, inplace=True)
restaurantDF.set_index("business_id", drop=True, inplace=True)
# ... the review dataset
restaurantReviewDF.drop("user_id", axis=1, inplace=True)
restaurantReviewDF.drop("type", axis=1, inplace=True)

# And save back to disk for easy manipulation
logging.info("Saving clean datasets back to disk...")
utils.save_dataframe_to_pickle(restaurantDF, "restaurant_original.df", pickleDataFolder)
utils.save_dataframe_to_pickle(restaurantReviewDF, "review_original.df", pickleDataFolder)
