from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer

# This is the list of stop-words from NLTK.
# It is hardcoded to avoid the manual download step (cf. nltk.download())
STOP_WORDS = set(
	['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 
	'you', 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 
	'his', 'himself', 'she', 'her', 'hers', 'herself', 'it', 'its', 
	'itself', 'they', 'them', 'their', 'theirs', 'themselves', 
	'what', 'which', 'who', 'whom', 'this', 'that', 'these', 'those', 
	'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 
	'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 
	'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 
	'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 
	'into', 'through', 'during', 'before', 'after', 'above', 'below', 
	'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 
	'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 
	'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 
	'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 
	'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 
	'don', 'should', 'now']
)

def simple_preprocessing(text, removeStopWords=True, stem=True):
	"""
	Preprocessing function: tokenizes the text into words, 
	lower-case all words and optionally,
	performs stop words removal and stemming

	text: the string to preprocess
	removeStopWords: boolean indicating whether to filter stop words (default True)
	stem: boolean indicating whether to stem words (default True)

	returns: a list of words/stems
	"""
	# does lower-casing, and optionally, stop words removal and stemming
	if removeStopWords:
		keepWordFn = lambda word: word.isalpha() and word not in STOP_WORDS
	else:
		keepWordFn = lambda word: word.isalpha()

	if stem:
		stemmer = PorterStemmer()
		wordProcessingFn = lambda word: stemmer.stem(word.lower())
	else:
		wordProcessingFn = lambda word: word.lower()

	return [
		wordProcessingFn(word) for word in word_tokenize(text) if
		keepWordFn(word)
    	]
