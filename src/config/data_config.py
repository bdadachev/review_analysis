import os

# os.getcwd() will be the src/ folder
DATA_ROOT = os.path.abspath(os.path.join(os.getcwd(), "../data/"))

# folder containing the raw files downloaded from Yelp
YELP_RAW_DATA_FOLDER = os.path.join(DATA_ROOT, "raw/yelp_challenge_dataset/")
# folder containing the yelp files after munging 
YELP_PICKLE_DATA_FOLDER = os.path.join(DATA_ROOT, "pickle/yelp_challenge_dataset/") 
