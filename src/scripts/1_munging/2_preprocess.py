import logging
import pandas as pd

from analysis import preprocessing
from config import data_config
from scripts import utils

logging.basicConfig(level=logging.INFO)

pickleDataFolder = data_config.YELP_PICKLE_DATA_FOLDER

logging.info("Loading review file...")
reviewDF = utils.load_dataframe_from_pickle("review_original.df", pickleDataFolder)

logging.info("Preprocessing the reviews. That should take about 20 minutes...")
reviewDF["preproc_text"] = reviewDF.text.apply(preprocessing.simple_preprocessing)
# keep only useful information (dont need duplicates with review_original.df)
reviewDF = reviewDF[ ["business_id", "review_id", "preproc_text"] ]

logging.info("Saving results back to disk...")
utils.save_dataframe_to_pickle(reviewDF, "review_preprocessed.df", pickleDataFolder)
