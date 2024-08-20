import numpy as np
from decision_making import ahp

'''
Here I provide the criteria names and alternative names
The order is strict so please provide list of strings
'''

criteria_names=["Experience", "Education", "Charisma", "Age"]
alternative_names=["Tom", "Rick", "Harry"]

'''
The data provided is in the form of comparision between two terms.
In the example we have 4 matrix where the comparision between alternatives is made using a specific criteria.
They are stacked in a 3d tensor so that more parallelism operations can be achieved.
And we have a criteria comparision matrix where the comparision between criterias is made.(This can also contain weights in 1d numpy array)
'''

criteria1 = np.array([[1,1/4,4],[4,1,9],[1/4,1/9,1]])
criteria2 = np.array([[1,3,1/5],[1/3,1,1/7],[5,7,1]])
criteria3 = np.array([[1,5,9],[1/5,1,4],[1/9,1/4,1]])
criteria4 = np.array([[1,1/3,5],[3,1,9],[1/5,1/9,1]])

matrix_per_criteria=np.array([criteria1, criteria2, criteria3, criteria4]) 

#list of matrix containing alternative to alternative comparision for every single criteria
criteria_comparison=np.array([[1,4,3,7], [1/4,1,1/3,3], [1/3,3,1,5],[1/7,1/3,1/5,1]])

# Evaluting
ahp(criteria_names, alternative_names, matrix_per_criteria, criteria_comparison, print_weight_matrix=True)

# Alternatively creating an object
# a = ahp(criteria_names, alternative_names, matrix_per_criteria, criteria_comparison, print_weight_matrix=True)

# Can print different attributes while evaluting with the help of object 
# print(a.normalized_unweighted_matrix)