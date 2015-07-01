import copy
import numpy as np
import sklearn.grid_search as grid_search

class CategoryPredictor:

    def __init__(self, model, param_grid={}):
        self.model = model
        self.param_grid = param_grid

    def fit(self, x, y):
        """
        Note: you may want to exclude/filter "exotic" categories before calling this
        method (e.g., categories that have only a few restaurants).

        x: list of preprocessed reviews for each restaurant
            [ [rest_1_review_1, rest_1_review2, ...], [rest2_review_1, ..] ]
	    where rest_1_review_1 is ['word1', 'word2', ...]
        y: list of categories for each restaurant
        """
        # gather the list of categories
        self.categories = set(cat for cats in y for cat in cats)
        
	# train one model for each category
        self.models = {}
        for category in self.categories:
            # for the current category, the Ys are whether the restaurants
            # belong to that category or not
            categoryY = np.asarray([ int(category in cats) for cats in y ])
            #model = copy.deepcopy(self.model)
            #think about 'scoring'?
            cvModel = grid_search.GridSearchCV(self.model, self.param_grid)
            cvModel.fit(x, categoryY)
            self.models[category] = cvModel

    def predict(self, x):
        if self.models == None:
            raise Exception("You need to fit the model first.")
        # iterate in what order? what is the exact output?
        result = [ [] for rowIdx in xrange(x.shape[0]) ]     
        for category, model in self.models.iteritems():
            for rowIdx, predY in enumerate(model.predict(x)):
                if predY == 1:
                    result[rowIdx].append(category)
        return result
	

    def predict_proba(self, x):
        if self.models == None:
            raise Exception("You need to fit the model first.")
        # iterate in what order? what is the exact output?        
        result = [ [] for rowIdx in xrange(x.shape[0]) ]     
        for category, model in self.models.iteritems():
            for rowIdx, predProba in enumerate(model.predict_proba(x)):
                result[rowIdx].append((category, predProba))
        return result

if __name__ == "__main__":
    pass
