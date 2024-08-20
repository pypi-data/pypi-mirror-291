import pandas as pd
import numpy as np
from decision_making import topsis

'''
Here we have names of criterias and alternatives.
We obey strict order so please provide these informations in list of strings
'''

criteria_names=["Price", "Storage", "Camera", "Looks"]
alternative_names=["X1", "X2", "X3", "X4", "X5"]

'''
Now we have dict_encode which maps the value of non numeric value to numeric
Whether or not this stuff is mandatory depends on the type of data user provides.
If in the data provide consists of some attributes with dtype=object or string, then providing dict_encode is mandatory
In other cases it's not, so by default, we set it to null
'''

dict_encode={
    "Low":1,
    "Below Average":2,
    "Average":3,
    "Good":4,
    "Excellent": 5
}

'''
Just to maintain smoothness and better efficiency, we accepted data in dataframe rather than numpy array
This is good because dataframe helps us to identy which of the attributes is object/string or numeric
'''

d=[[250, 16, 12.22, "Excellent"], [200, 16, 8, "Average"], [300, 32, 16, "Good"],[275, 32, 8, "Good"], [225, 16, 16, "Below Average"]]
data=pd.DataFrame(d, index=alternative_names,  columns=criteria_names)
#we got the data in this way

'''
benificial_cost_mark- keep track of attributes which are either cost or benefit
make sure to keep the length same as number of attributes
This can consist of list or np.array of either 0 or 1 and nothing else
1 represents criteria is benifit, 0 represents cost
'''

benificial_cost_mark=[0, 1, 1, 1]

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
topsis(criteria_names, alternative_names, data, weights_criteria, benificial_cost_mark, dict_encode=dict_encode) 

# Alternatively creating an object
t=topsis(criteria_names, alternative_names, data, weights_criteria, benificial_cost_mark, dict_encode=dict_encode) 

