from gensim import models
import json
import logging
import os

from config import data_config
from scripts import utils

# Create handler because gensim writes a lot on INFO...
logger = logging.getLogger(__name__)
sh = logging.StreamHandler()
sh.setLevel(logging.INFO)
logger.setLevel(logging.INFO)
logger.addHandler(sh)

logger.info("Loading LDA model...")
modelFolder = data_config.MODELS_FOLDER
ldaTopicsCount = data_config.LDA_TOPICS_COUNT

ldaFile = os.path.join(modelFolder, "reviews_all.lda{}".format(ldaTopicsCount))
ldaModel = models.ldamodel.LdaModel.load(ldaFile)
#ldaModel = models.ldamulticore.LdaMulticore.load(ldaFile)

logger.info("Now let us label the topics...")
topicLabels = []
for topicIdx in xrange(nbTopics):
    print "Topic {}:".format(topicIdx+1), ldaModel.print_topic(topicIdx, 20)
    print "Please enter a topic label:"
    label = raw_input()
    topicLabels.append(label)
    print

labelFile = os.path.join(modelFolder, "topic_labels.lda{}".format(ldaTopicsCount))
with open(labelFile, 'w') as fp:
    json.dump(topicLabels, fp)
