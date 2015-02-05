import numpy as np
import pandas as pd
import statsmodels.regression as smreg

def get_trend(xs, ys, alpha=0.05):
	"""
	Fits an OLS model y = ax + b to the xs and ys variables.
	The trend is stable if 0 is in the confidence interval of 'a'.

	xs: a numpy array (the time variables)
	ys: a numpy array (the price/rating/... variables)
	alpha: the significance level for the confidence interval

	Returns: an int, -1, 0 or 1 (respectively decrease, stability and increase)
    	"""
	# Note: we use statsmodels rather than sklearn
	# because it gives confidence intervals (as well as other stats)
	if xs.size == 0:
		raise ValueError("Empty array.")
    
	# fit the model
	df = pd.DataFrame({"intercept": np.ones(xs.size), "x": xs})
	model = smreg.linear_model.OLS(ys, df).fit()

	# get the confidence interval (CI) for the slope
	#intercept = result.params['intercept']
	xCoeff = model.params['x']
	xLowCI, xHighCI = model.conf_int(alpha).ix['x', :]

	# if 0 is in the CI, we can't reject the null hypothesis (=stable)
	if xLowCI > 0:
 		# ys are increasing
		return 1 
	elif xHighCI < 0:
		# ys are decreasing
		return -1 
	else: 
        	# 0 is in the confidence interval, ys are stable
        	return 0
