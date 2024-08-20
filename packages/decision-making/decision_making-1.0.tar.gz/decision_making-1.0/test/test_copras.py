import pandas as pd
import numpy as np
from decision_making import copras

'''
Here we have names of criterias and alternatives.
We obey strict order so please provide these informations in list of strings
'''

#we have criteria_names and alternative_names of size=4 and 5 respectively
criteria_names=["Batting Average", "Batting Strike Rate", "Bowling Average", "Bowling Strike Rate"]
alternative_names=["Maxwell", "Dhoni", "AB de Villiers", "Andre Russell", "Rinku Singh"]

'''
Now we can provide the data in numpy format. 
We must make sure that the data we provide must have same number of rows as len(alternative_names)
We must make sure that the data we provide must have same number of columns as len(criteria_names)
'''

data=np.array([[31.08, 139.53, 29.15, 22.05], [29.12, 142.97, 33.69, 27.30]
             ,[24.08, 122.58, 29.18, 23.10], [23.17, 128.28, 24.60, 17.59]
             ,[33.33, 186.41, 27.96,18.89]])

'''
benificial_cost_mark- keep track of attributes which are either cost or benefit
make sure to keep the length same as number of attributes
This can consist of list or np.array of either 0 or 1 and nothing else
1 represents criteria is benifit, 0 represents cost
'''

benificial_cost_mark=[1, 1, 0, 0]

'''
This keeps the weight of the attributes which can be multiplied to normalized matrix in order to get weight normalized matrix
make sure to keep the length same as number of attributes
This can consist of list of int/float or numpy array of dtype=int/float
Give any value as the object can automatically normalize the weights_criteria by dividing every element by sum of array
'''


weights_criteria=[50, 50, 50, 50]
#in the class instance, the weight_criteria gets normalized so every value is scaled between 0 to 1
#so this array becomes-[0.25, 0.25, 0.25, 0.25]


#Evaluting
copras(criteria_names, alternative_names, data, weights_criteria, benificial_cost_mark)

# Alternatively creating an object
t=copras(criteria_names, alternative_names, data, weights_criteria, benificial_cost_mark)

