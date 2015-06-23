import logging
import pandas as pd

from analysis import language, preprocessing
from config import data_config
from scripts import utils

logging.basicConfig(level=logging.INFO)

pickleDataFolder = data_config.YELP_PICKLE_DATA_FOLDER

logging.info("Loading review file...")
reviewDF = utils.load_dataframe_from_pickle("review_original.df", pickleDataFolder)

logging.info("Performing language detection... This will take several hours.")
reviewDF["language"] = reviewDF.text.apply(language.detect_language)
logging.info("Languages counts:\n" + reviewDF.language.value_counts().to_string())

logging.info("Preprocessing the reviews... This will take some time.")
def preprocess(entry):
	if entry.language == language.UNSUPPORTED:
		return []
	return preprocessing.simple_preprocessing(entry.text, entry.language)
reviewDF["preproc_text"] = reviewDF[ ["text", "language"] ].apply(preprocess, axis=1) #returns an error (seems it doesn't like lists)

logging.info("Saving results back to disk...")
# keep only useful information (dont need duplicates with review_original.df)
reviewDF = reviewDF[ ["business_id", "review_id", "preproc_text", "language"] ]
utils.save_dataframe_to_pickle(reviewDF, "review_preprocessed.df", pickleDataFolder)
