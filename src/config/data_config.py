import os

# os.getcwd() is the src/ folder (assume all scripts are run from there)
DATA_ROOT = os.path.abspath(os.path.join(os.getcwd(), "../data/"))

# folder containing the raw files downloaded from Yelp
YELP_RAW_DATA_FOLDER = os.path.join(DATA_ROOT, "raw/yelp_challenge_dataset/")
# folder containing the Yelp files after munging 
YELP_PICKLE_DATA_FOLDER = os.path.join(DATA_ROOT, "pickle/yelp_challenge_dataset/") 
# folder storing the various models built
MODELS_FOLDER = os.path.join(DATA_ROOT, "models/")

# number of topics to uncover with LDA
LDA_TOPICS_COUNT = 50
