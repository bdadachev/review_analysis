from nltk.corpus import stopwords
from nltk import stem
import re
import unidecode

import language

STOP_WORDS = {
	shortStr : stopwords.words(language.FULL_LANGUAGE_STRINGS[shortStr]) for
	shortStr in language.SUPPORTED_LANGUAGES
}
STEMMERS = {
	shortStr : stem.SnowballStemmer(language.FULL_LANGUAGE_STRINGS[shortStr]) for
	shortStr in language.SUPPORTED_LANGUAGES
}

def word_tokenize(text):
	"""
	A simple word tokenizer. Unicode strings are converted to ascii
	using unidecode, to normalize the text (e.g., remove accents)
	and make sure that tokenization is done properly.
	"""
	return filter(len, re.split("[^A-Za-z0-9]", unidecode.unidecode(text)))

def simple_preprocessing(text, textLanguage, removeStopWords=True, stem=True):
	"""
	Preprocessing function: tokenizes the text into words, 
	lower-case all words and optionally,
	performs stop words removal and stemming

	text: the string to preprocess
	removeStopWords: boolean indicating whether to filter stop words (default True)
	stem: boolean indicating whether to stem words (default True)

	returns: a list of tokens (words or stems)
	"""
	if textLanguage not in language.SUPPORTED_LANGUAGES:
		raise ValueError("Unknown language.")

	if removeStopWords:
		keepWordFn = lambda word: word not in STOP_WORDS[textLanguage]
	else:
		keepWordFn = lambda word: True

	if stem:
		wordProcessingFn = lambda word: STEMMERS[textLanguage].stem(word.lower())
	else:
		wordProcessingFn = lambda word: word.lower()

	return [
		wordProcessingFn(word) for word in word_tokenize(text) if
		keepWordFn(word)
    	]
