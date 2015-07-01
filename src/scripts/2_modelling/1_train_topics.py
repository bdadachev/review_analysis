from gensim import corpora, models
import logging
import numpy as np
import pandas as pd
import os

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

dictFile = os.path.join(modelFolder, "reviews_all.dict")
mmFile = os.path.join(modelFolder, "reviews_all.mm")
ldaFile = os.path.join(modelFolder, "reviews_all.lda{}".format(ldaTopicsCount))

logger.info("Loading reviews...")
reviewDF = utils.load_dataframe_from_pickle("review_preprocessed.df", pickleDataFolder)
logger.info("Dropping non English reviews...")
reviews = reviewDF[ reviewDF.language == "en" ].preproc_text
del reviewDF

logger.info("LDA: Creating gensim dictionary...")
# a dictionary is just a mapping word to int (unique id)
dictionary = corpora.Dictionary(reviews)
dictionary.save(dictFile)

logger.info("LDA: Converting reviews into bags of words...")
# converts input documents into lists of tuples (wordID, wordCount)
corpus = [dictionary.doc2bow(reviewWords) for reviewWords in reviews]
del reviews
corpora.MmCorpus.serialize(mmFile, corpus)

logger.info("LDA: Training LDA with {} topics. This will take some time...".format(ldaTopicsCount))
ldaModel = models.ldamodel.LdaModel(corpus=corpus, id2word=dictionary,
                                    num_topics=ldaTopicsCount)
# ldamulticore didn't work on my Windows machine but it worked fine on Linux.
#ldaModel = models.ldamulticore.LdaMulticore(corpus=corpus, id2word=dictionary, 
#                                            num_topics=ldaTopicsCount, workers=1)
ldaModel.save(ldaFile)

logger.info("LDA: All done.")
