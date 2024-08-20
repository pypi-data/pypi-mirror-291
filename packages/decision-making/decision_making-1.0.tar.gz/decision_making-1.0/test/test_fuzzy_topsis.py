import numpy as np
import pandas as pd
from scipy.stats import gmean
from decision_making import fuzzy_topsis

'''
Here we have names of criterias and alternatives.
We obey strict order so please provide these informations in list of strings
'''

criteria_names=["C1",  "C2", "C3",  "C4",  "C5", "C6", "C7", "C8", "C9", "C10"]
alternative_names=["Amazon EC2", "Digital ocean", "Google",
                  "Microsoft azure", "Rack space", "Softlayer"]

'''
Now we have dict_encode which maps the value of non numeric value to fuzzy number.
This thing is mandatory to provide at all cost. That how fuzzy concept will be implemented
The keys must be strings whereas the fuzzy_number is a list of size 3 containing numerical values
'''

dict_encode={
    "VL": [0.0, 0.0, 0.2], 
    "L": [0.0, 0.2, 0.4],
    "M":  [0.2, 0.4, 0.6],
    "H": [0.4, 0.6, 0.8],
    "VH": [0.6, 0.8, 1.0],
    "E": [0.8, 1.0, 1.0] #we can encode this with fuzzy value and we always take key to be a string
}

'''
Now provide the data in the form of nd.ndarray and make sure that every thing present in the matrix is a semantic or words
So that it can be mapped in dict_encode to extract the fuzzy numbers
'''

#we need data that compare the alternative against criteria in linguistic terms
#it's best to se numpy array for fast manipulation
data=np.array([
    ['L', 'VL', 'L', 'L', 'L', 'L', 'H', 'H', 'L', 'L'],
    ['L', 'M', 'VL', 'VL', 'L', 'L', 'H', 'H', 'L', 'L'],
    ['L', 'H', 'L', 'L', 'L', 'L', 'H', 'H', 'VL', 'VL'],
    ['L', 'M', 'L', 'L', 'VL', 'VL', 'M', 'M', 'L', 'L'],
    ['M', 'M', 'M', 'M', 'L', 'L', 'H', 'H', 'H', 'L'],
    ['L', 'VL', 'L', 'M', 'L', 'L', 'H', 'H', 'M', 'M']
], dtype=object
)

'''
benificial_cost_mark- keep track of attributes which are either cost or benefit
make sure to keep the length same as number of attributes
This can consist of list or np.array of either 0 or 1 and nothing else
1 represent that given criteria is benifit, 0 represents cost
'''

benificial_cost_mark=([0, 0, 0, 0, 1, 1, 1, 1, 1, 1])

'''
This keeps the weight of the attributes which can be multiplied to normalized matrix in order to get weight normalized matrix
make sure to keep the length same as number of attributes
This can consist of list of int/float or numpy array of dtype=int/float
Give any value as the object can automatically normalize the weights_criteria by dividing every element by sum of array
'''

weights_criteria=np.array([0.1195,  0.1048, 0.0748, 0.0890,  0.1345, 0.1191, 0.0898, 0.1046, 0.0744, 0.0894])

#Evaluting
fuzzy_topsis(criteria_names, alternative_names, data, weights_criteria, benificial_cost_mark, dict_encode)


# Alternatively creating an object
t=fuzzy_topsis(criteria_names, alternative_names, data, weights_criteria, benificial_cost_mark, dict_encode)
# Can print different attributes while evaluting with the help of object 
t.most_suitable_alternative