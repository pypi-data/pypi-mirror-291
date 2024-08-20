
import pandas as pd
import numpy as np
from decision_making import fuzzy_copras

'''
Here we have names of criterias and alternatives.
We obey strict order so please provide these informations in list of strings
'''

#we have criteria_names and alternative_names of size=4 and 5 respectively
criteria_names=["Hard disk","RAM", "Price", "Weight"]
alternative_names=["Dell", "HP", "Lenovo", "Asus", "Acer", "Sony", "Apple", "Toshiba"]

'''
Now we can provide the data in numpy format. 
We must make sure that the data we provide must have same number of rows as len(alternative_names)
We must make sure that the data we provide must have same number of columns as len(criteria_names)
'''

data=np.array([[1000, 4, 43000, 1.5],[750, 6, 45000, 1.7],[1000, 8, 35000, 2.0], [750, 6, 38000, 2.1],
             [900, 8, 39000, 1.8], [750, 6, 46000, 1.2],[600, 6, 50000, 1.1], [800, 10, 42000, 2.5]])

'''
benificial_cost_mark- keep track of attributes which are either cost or benefit
make sure to keep the length same as number of attributes
This can consist of list or np.array of either 0 or 1 and nothing else
1 represents criteria is benifit, 0 represents cost
'''

benificial_cost_mark=[1, 1, 0, 0]



'''
These represents the decision makers that assign importance to each criteria based on their expertise in the 
form of linguistic terms.

!!Please make note of this.
The names of the decision makers wont impact our final result at all.
So even if you dont feel the comfort of unnecesarily providing the names of decision makers in a list,
provide their length instead.

Here, you can also provide decision_makers=5 and it wont make any difference in the result or such.
'''

decision_makers=['A1', 'A2', 'A3', 'A4', 'A5']

'''
criteria_comparision_fuzzy:-
Now in order to calculate the weight of the criterias we can use linguistic terms which will be replaced with
fuzzy numbers.
Here, we can use some decision makers which can based on their expertise can assign each criteria with a 
linguistic term.
These linguistic term can be used to define importance of each criteria w.r.t each decision makers.
Once we get the linguistic terms, we can simply use fuzzy number assigned in the dictionary provided by the user
and can replace the terms to their respective fuzzy number corresponds in the dictionary.
Then we can use fuzzy aggregation technique to combine the fuzzy number from all decision maker into a single 
fuzzy number assigned to each criteria.
We must make sure that the number of rows in the decision making must be same as len(criteria_names).
There must be atleast one decision maker to make a decision or we are left with nothing.
The number of columns in the in the decision making must be same as len(decisiona_makers).
We must also make sure that the linguistic terms used by the decision makers must be be present in the dictionary.
Failing these condition will throw an error in the code.
'''

criteria_comparison=np.array([['M','M','EH','EH','VH'],['VH','M','VH','EH','EH'],['EH','M','M','L','H'],['VL','M','VH','VH','H']], dtype=str)

'''
Here you need to provide fuzzy table where you give input in the form of semantics or human linguistics 
It may involve words like -"Good", "Bad" ,"Very bad", "Average" etc.
Along with each semantics, you must assign fuzzy values ranging as [lower, medium, upper]
Make sure the values you provide is numeric.
Make sure the key should a string and the fuzzy number must be list of integers.
'''

fuzzy_table={
    "EL": [0, 0, 0.1], "VL": [0, 0.1, 0.3], "L": [0.1, 0.3, 0.5], "M": [0.3, 0.5, 0.7], "H": [0.5, 0.7, 0.9], 
    "VH": [0.7, 0.9, 1], "EH": [0.9, 1, 1]
}
#evaluting
k=fuzzy_copras(criteria_names, alternative_names, data, benificial_cost_mark, decision_makers, fuzzy_table, criteria_comparison)