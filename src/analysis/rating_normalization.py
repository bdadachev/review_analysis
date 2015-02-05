import numpy as np
import scipy as sp
import scipy.stats

from math import sqrt

def wilson_score_low(ratings, upThreshold=3.5, alpha=0.05):
	"""
	Returns the lower bound of the Wilson interval.
	The Wilson interval estimates a binomial proportion
	(you can think of it as a probability of success),
	so the ratings are converted into positive ratings
	and negative ratings (see upThreshold parameter).

	ratings: the list of ratings (stars, valid range [1,2,3,4,5])
	upThreshold: float, all ratings with value greater or equal to 
		this quantity are considered positive, all strictly lower
		are considered negative 
		(default 3.5, so 4 and 5 stars are considered positive).
	alpha: the significance level for the confidence interval (default 0.05)
	"""
	nbUpVotes = sum(1 if rating >= upThreshold else 0 for rating in ratings)
	nbDownVotes = len(ratings) - nbUpVotes
	nbVotes = nbUpVotes + nbDownVotes	
	if nbVotes == 0:
		return 0.

	z = scipy.stats.norm.ppf(1 - alpha/2)
	phat = float(nbUpVotes) / float(nbVotes)
	return ((phat + z*z/(2*n) - z * sqrt((phat*(1-phat)+z*z/(4*n))/n))/(1+z*z/n))
    
if __name__ == "__main__":
	print wilson_score_low([5])
	print wilson_score_low([1, 1, 1, 3, 4, 4, 4, 5, 5])
	print wilson_score_low([5, 5, 5, 5, 5])    
