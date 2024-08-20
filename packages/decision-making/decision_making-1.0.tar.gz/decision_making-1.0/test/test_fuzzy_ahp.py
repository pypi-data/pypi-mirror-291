import numpy as np
# from scipy.stats import gmean
# import pandas as pd
#the most important thing is to provide name of criteria and the alternatives

from decision_making import fuzzy_ahp

#Example 1


'''
Provide the names of the criteria and the alternatives you want to build your decision on.
The data type must be a list and strictly consist of strings
'''

criteria_names=["Experience", "Education", "Charisma", "Age"]
alternative_names=["Tom", "Rick", "Harry"]



'''
Here you need to provide fuzzy table where you give input in the form of semantics or human linguistics 
It may involve words like -"Good", "Bad" ,"Very bad", "Average" etc.
Along with each semantics, you must assign fuzzy values ranging as [lower, medium, upper]
Make sure the values you provide is numeric
Here in the example I have provide the human linguistics as -"1", "2", "1/3", etc.
Don't worry they resemble the same thing. Maybe some human want to give linguistics in the form of number, then it's comepletely okey!!
Make sure that the linguistics provided either seems numeric or words but data type must be a string.
'''


#we are using triangular fuzzy number
fuzzy_table = {
    "1": [1, 1, 1], "2": [1, 2, 3], "3": [2, 3, 4], "4": [3, 4, 5], "5": [4, 5, 6], 
    "6": [5, 6, 7], "7": [6, 7, 8], "8": [7, 8, 9], "9": [8, 9, 10], "10": [10, 10, 10], 
    "1/2": [1/3, 1/2, 1], "1/3": [1/4, 1/3, 1/2], "1/4": [1/5, 1/4, 1/3], "1/5": [1/6, 1/5, 1/4],
    "1/6": [1/7, 1/6, 1/5], "1/7": [1/8, 1/7, 1/6], "1/8": [1/9, 1/8, 1/7], "1/9": [1/10, 1/9, 1/8], "1/10": [1/10, 1/10, 1/10]
}


'''
The data provided is in the form of linguistic terms. 
Make sure that the data user provide must be present in the fuzzy table they provide
In the example we have 4 matrix where the comparision per alternative is made using a specific criteria.
They are stacked in a 3d tensor so that more parallelism operations can be achieved.
And we have a criteria comparision matrix where the comparision between criterias is made.
'''


criteria1 = np.array([["1", "1/4", "4"],["4", "1", "9"],["1/4", "1/9", "1"]], dtype=str)

criteria2 = np.array([["1", "3", "1/5"],["1/3", "1", "1/7"],["5", "7", "1"]], dtype=str)

criteria3 = np.array([["1", "5", "9"],["1/5", "1", "4"],["1/9", "1/4", "1"]], dtype=str)

criteria4 = np.array([["1", "1/3", "5"],["3", "1", "9"],["1/5", "1/9", "1"]], dtype=str)


matrix_per_criteria=np.array([criteria1, criteria2, criteria3, criteria4], dtype=str) 
#list of matrix containing alternativeto alternative comparision for every single criteria
#the dtype of the matrix_per_criteria must be object or string

criteria_comparison = np.array([["1", "4", "3", "7"],["1/4", "1", "1/3", "3"],["1/3", "3", "1", "5"],["1/7", "1/3", "1/5", "1"]] ,dtype=str)
#the dtype of the criteria_comparison must be a string

q=fuzzy_ahp(criteria_names, alternative_names, matrix_per_criteria, criteria_comparison, fuzzy_table, print_weight_matrix=True,)     
# q.most_suitable_alternative