import langdetect

import logging

GERMAN = "de"
ENGLISH = "en"
SPANISH = "es"
FRENCH = "fr"
UNSUPPORTED = "unsupported"

SUPPORTED_LANGUAGES = set([GERMAN, ENGLISH, SPANISH, FRENCH])

# NLTK correspondances
FULL_LANGUAGE_STRINGS = {
	GERMAN : "german",
	ENGLISH : "english",
	SPANISH : "spanish",
	FRENCH : "french",
}

def detect_language(text):
	"""
	Performs language detection.
        
	Not surprisingly, language detection is hard for short texts.
	After manually analyzing text classified as unsupported languages, a pattern emerged:
	-> unreliable detections occur mainly for very short text.
		- many have typos and/or funky casing.
		- many have foreign words, like pizza, which tends to be incorrectly classified as unsupported.
		- and most of these are English (because that's what the majority of the dataset is).
	-> there are some long reviews from 'exotic' languages (e.g., finnish) that are accurately classified.
	
	We use simple heuristics to improve the results:
	-> short text and unsupported: set as English.
	-> long text and unsupported: leave as unsupported.
	"""
	try:
		language = langdetect.detect(text)
	except:
		logging.info(u"Language detection failed for review '{}'".format(text))
		return UNSUPPORTED
	if language not in SUPPORTED_LANGUAGES:
		if len(text) <= 100:
			return ENGLISH
		return UNSUPPORTED
	return language
