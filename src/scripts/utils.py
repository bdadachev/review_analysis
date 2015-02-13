import os

import json
import logging
import pandas as pd

def load_yelp_dataset(dataset, dataFolder):
	"""
	dataset: the type of Yelp dataset to load, 
		values in ["business", "checkin", "review", "tip", "user"]
	dataFolder: the folder where the raw data sits
	"""
	# check the arguments are valid, and load the data into a dataframe
	if dataset not in set(["business", "checkin", "review", "tip", "user"]):
		raise ValueError("Incorrect dataset type.")
	
	dataFileTemplate = "yelp_academic_dataset_{}.json"
	dataFile = os.path.join(dataFolder, dataFileTemplate.format(dataset))

	if not os.path.isfile(dataFile):
		raise ValueError("File {} does not exist (is the folder valid?)".format(dataFile))

	with open(dataFile) as fp:
		df = pd.DataFrame([ json.loads(line) for line in fp.readlines() ])
	
	# now, do some dataset specific treatment to have the right data types
	if dataset == "business":
		pass
	elif dataset == "checkin":
		raise NotImplementedError("We don't use the 'checkin' dataset yet.")
	elif dataset == "review":
		df["date"] = df.date.astype("datetime64")
	elif dataset == "tip":
		raise NotImplementedError("We don't use the 'tip' dataset yet.")
	else: # dataset == "user"
		raise NotImplementedError("We don't use the 'user' dataset yet.")

	return df

def load_dataframe_from_pickle(pickleFile, pickleFolder):
	pickleFile = os.path.join(pickleFolder, pickleFile)
	df = pd.read_pickle(pickleFile)	
	return df

def save_dataframe_to_pickle(df, pickleFile, pickleFolder):
	pickleFile = os.path.join(pickleFolder, pickleFile)
	df.to_pickle(pickleFile)
