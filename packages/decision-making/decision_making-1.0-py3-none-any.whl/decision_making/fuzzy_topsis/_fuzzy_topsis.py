import numpy as np
import pandas as pd
from scipy.stats import gmean

#Parameter check

'''
Check_parameters_Fuzzy_TOPSIS-is object that check whether the parameters provided for Fuzzy TOPSIS is correct or not.
The parameter mainly consists of:-
criteria_names-consists of names of the criteria
alternative_names-consists of names of the alternatives
data-consist of data provided by the user. The data can have either numerical (int/float) or non numerica (object/string) 
values
weights_criteria-This keeps the weight of the attributes which can be multiplied to normalized matrix in order to get weight
normalized matrix
benificial_cost_mark- keep track of attributes which are either cost or benefit
dict_encode(sometimes mandatory sometimes not)-maps the value of non numeric value to numeric but only mandatory if data has
non numerical features
'''
class Check_parameters_Fuzzy_TOPSIS:
    
    def __init__(self, criteria_names, alternative_names, data, weights_criteria,  benificial_cost_mark, dict_encode):
        '''
        Assign values to the objects atrributes.
        '''
        self.criteria_names=criteria_names
        self.alternative_names=alternative_names
        self.weights_criteria=weights_criteria
        self.data=data
        self.benificial_cost_mark=benificial_cost_mark
        self.dict_encode=dict_encode
        self.check_redundancy=0
        
        #the contains the data with encoded with fuzzy value
        self.data_with_fuzzy=None
        
        '''
        the function check_dimentions_and_dtype checks everythings
        if any error is raised, it will show and it wont proceed
        if not, we will see the message-"Everything is fine"
        '''
        
        self.check_dimentions_and_dtype()
        print("Parameter check: Passed")
        
        
    def check_dimentions_and_dtype(self):
        #check dtypes of criteria and alternative names
        if type(self.criteria_names)!=list:
            self.check_redundancy=1
            raise ValueError("The criteria_names is not list")
        #check if every element in the array is string
        for ele in self.criteria_names:
            if type(ele)!=str:
                self.check_redundancy=1
                raise ValueError("Element in the criteria list is not string.")
        
        if type(self.alternative_names)!=list:
            self.check_redundancy=1
            raise ValueError("The criteria_names is not list")
        #check if every element in the array is string
        for ele in self.alternative_names:
            if type(ele)!=str:
                self.check_redundancy=1
                raise ValueError("Element in the alternative list is not string.")
        
        
        
        #-------------------------------------------------------------------------

        #check for weights_criteria
        
        #check whether the weight_criteria is a list or not
        if type(self.weights_criteria)!=list and type(self.weights_criteria)!=np.ndarray:
            self.check_redundancy=1
            raise ValueError("The weight_criteria is neither list nor np.array")
        
        
        #check if weights_criteria is nd.array, it should have one dimention and shape is good
        if type(self.weights_criteria)==np.ndarray:
            if self.weights_criteria.ndim!=1 or self.weights_criteria.shape[0]!=len(self.criteria_names):
                self.check_redundancy=1
                raise ValueError("The weights_criteria must have 1 dim or correct shape")  
                
        #if weights_criteria is not np.array, check its len
        if type(self.weights_criteria)==list and len(self.weights_criteria)!=len(self.criteria_names):
            self.check_redundancy=1
            raise ValueError("The benificial_cost_mark list have correct shape")
            
        #every value in the list or np array must be less than 1 and greater than 0
        if type(self.weights_criteria)==list:
            for item in self.weights_criteria:
                if not isinstance(item, (int, float)):
                    self.check_redundancy=1
                    raise ValueError("The items in the weights_criteria must be numeric")
                    
        if type(self.weights_criteria)==np.ndarray:
            if self.weights_criteria.dtype!="float" and self.weights_criteria.dtype!="int":
                self.check_redundancy=1
                raise ValueError("The items in the weights_criteria must be numeric")
            
        #convert the list to np.array
        if type(self.weights_criteria)==list:
            self.weights_criteria=np.array(self.weights_criteria)
        
        #the most important thing is whether the weight provided by user is normalized or not
        #we will make it normalized by deviding elements by sum of the array
        self.weights_criteria=self.weights_criteria/np.sum(self.weights_criteria, axis=0)
            
        #-------------------------------------------------------------------------
        #check for benificial_cost_mark
        
        #check whether the beneficial_cost_mark is a list or not
        if type(self.benificial_cost_mark)!=list and type(self.benificial_cost_mark)!=np.ndarray:
            self.check_redundancy=1
            raise ValueError("The benificial_cost_mark is neither list nor np.array")
            
        #check if beneficial_cost_mark is nd.array, it should have one dimention and shape is good
        if type(self.benificial_cost_mark)==np.ndarray:
            if self.benificial_cost_mark.ndim!=1 or self.benificial_cost_mark.shape[0]!=len(self.criteria_names):
                self.check_redundancy=1
                raise ValueError("The benificial_cost_mark must have 1 dim or correct length")
        
        #if benificial_cost_mark is not np.array, check its len
        if type(self.benificial_cost_mark)==list and len(self.benificial_cost_mark)!=len(self.criteria_names):
            self.check_redundancy=1
            raise ValueError("The benificial_cost_mark list have correct shape")
            
        #check if anything inside the benificial_cost_mark is not 0 or 1
        for i in self.benificial_cost_mark:
            if i!=1 and i!=0:
                self.check_redundancy=1
                raise ValueError("The benificial_cost_mark can either be 1 or 0")
        
        
        #if benificial_cost_mark is not np.array, make it np.array, easier for comptation
        if type(self.benificial_cost_mark)==list:
            self.benificial_cost_mark=np.array(self.benificial_cost_mark)
            
        #-------------------------------------------------------------------------
        
        #check for data
        if type(self.data)!=np.ndarray:
            self.check_redundancy=1
            raise ValueError("The data is not np.ndarray")
            
        if self.data.ndim!=2:
            self.check_redundancy=1
            raise ValueError("The data is not a 2d tensor")
        
        if self.data.shape[0]!=len(self.alternative_names) and self.data.shape[1]!=len(self.criteria_names):
            self.check_redundancy=1
            raise ValueError("The shape of the data is not correct")
            
        
        #-------------------------------------------------------------------------
        #now check dict_encode
        #check that every key in the dictionary is a string
        #check that every value has a. list of size three all consisting of numerical values
        
        for key, value in self.dict_encode.items():
            if type(key)!=str:
                self.check_redundancy=1
                raise ValueError("The key in the dictionary is not string")
                
            if type(value)!=list:
                self.check_redundancy=1
                raise ValueError("The value in the dictionary is not list")
            
            if len(value)!=3:
                self.check_redundancy=1
                raise ValueError("The value in the dictionary does not have size equal to 3")
            
            for i in value:
                if type(i)!=int and type(i)!=float:
                    self.check_redundancy=1
                    raise ValueError("The items in values in dictionary is not numeric")
                    
        #-------------------------------------------------------------------------

        #finally we need to check whether every element in the data can be mapped to the dictionary
        #do every element in the data is present in the keys of dict_encode
        self.data_with_fuzzy=np.ones((self.data.shape[0], self.data.shape[1], 3))
        for i in range(self.data.shape[0]):
            for j in range(self.data.shape[1]):
                if self.data[i][j] not in self.dict_encode: 
                    self.check_redundancy=1
                    raise ValueError("The element not present in the dictionary")
                self.data_with_fuzzy[i][j]=np.array(self.dict_encode[self.data[i][j]])
                
#         print(self.data_with_fuzzy)

#Fuzzy_Topsis

'''
The function returns the most suitable alternative provided the criteria_names, alternative_names,data, weights_criteria,
benificial_cost_mark, dict_encode
It also inherits Check_parameters_Fuzzy_TOPSIS which check whether the parameters provided is correct or not
If any error is raised in Check_parameters_TOPSIS then the process wont proceed else it will show the results.
The displayed result depends on what user want.
If they wish to see that the rank array in the end then they can see it tuning the value of rank_array which is by default 
set to True
The rank array consist of the score it gave to every alternative
'''

class FUZZY_TOPSIS(Check_parameters_Fuzzy_TOPSIS):
    def __init__(self, criteria_names, alternative_names, data, weights_criteria, benificial_cost_mark, dict_encode, show_rank_array=True):
        '''
        Used the inherited Check_parameters_Fuzzy_TOPSIS function
        '''
        super().__init__(criteria_names, alternative_names, data, weights_criteria, benificial_cost_mark, dict_encode)
        
        '''
        Assign values to other attributes
        '''
        #the rank_array attribute keeps the score of every attributes assigned to them
        self.rank_array=None
        
        #fuzzy_weighted_decision_matrix keeps the weighted fuzzy data aquired after multiplying criteria weights
        self.fuzzy_weighted_decision_matrix=None
        
        #we need to store the values vj_plus(ideal best value) and vj_minus(ideal worst value) for evry criteria
        #user might use these parameters for evaluation
        self.vj_plus=None
        self.vj_minus=None
        
        #we need to keep track of the location of Euclidean distance between the target alternative and the best/worst 
        #alternative and for each alternative
        #which is indicated using di_plus and di_minus
        #di_plus is euclidean distance wrt vj_plus of every criteria
        #di_minus is euclidean distance wrt vj_minus of every criteria
        self.di_plus=None
        self.di_minus=None
        
        self.show_rank_array=show_rank_array
        self.most_suitable_alternative=None
        '''
        The solve function does the heavy lifting. It does all the computation part
        Since we have deployed 2d/3d tensors instead of normals lists, we get to see good efficiency and reduced computation
        Once this is done, we have calculated the rank_array along with their score.
        Once done we can use show find to print the best alternative
        '''
        
        self.solve()
        '''
        Once solved we can show the result
        '''
        self.show()
        
        
    def solve(self):
        
        #find the fuzzy weighted matrix
        a=self.data_with_fuzzy 
        b=self.weights_criteria
        fuzzy_weighted_matrix=a*b.reshape(-1,1)
        
        #assign this to self.fuzzy_weighted_decision_matrix
        self.fuzzy_weighted_decision_matrix=fuzzy_weighted_matrix.copy()

        #calculate vj_plus and vj_minus
        v_j_plus=np.ones((len(self.criteria_names), 3))
        v_j_plus=v_j_plus*self.benificial_cost_mark.reshape(-1,1)
        v_j_minus=np.where(v_j_plus == 0, 1.0, 0.0)
        
        #assign the value of v_j_plus and v_j_minus to attributes self.vj_plus and self.vj_minus 
        self.vj_plus=v_j_plus
        self.vj_minus=v_j_minus
        
        #calculate di_plus and di_minus (some say it si_plus and si_minus but it's the same thing)
        d_i_plus=np.sum(((np.sum((fuzzy_weighted_matrix-v_j_plus)**2, axis=-1))*1/3)**(1/2), axis=-1)
        d_i_minus=np.sum(((np.sum((fuzzy_weighted_matrix-v_j_minus)**2, axis=-1))*1/3)**(1/2), axis=-1)
        
        #assign the value of d_i_plus and d_i_minus to attributes self.di_plus and self.di_minus
        self.di_plus=d_i_plus
        self.di_minus=d_i_minus
        
        #calculate rank_array
        self.rank_array=d_i_minus/(d_i_plus+d_i_minus)
        
    def show(self):
        if self.show_rank_array==True:
            print("The rank array is:-")
#             print(pd.DataFrame(self.rank_array, columns=['score'], index=self.alternative_names))
            
            #also show the ranks too
            sorted_indices = np.argsort(-self.rank_array)
            ranks = np.empty_like(sorted_indices)
            ranks[sorted_indices] = np.arange(1, len(self.rank_array) + 1)
            show=np.array([self.rank_array,ranks])
            show=show.T
            
            print(pd.DataFrame(show, index=self.alternative_names, columns=['Score', 'Rank']))
            
        #show the most suitable alternative
        max_index = np.argmax(self.rank_array)
        self.most_suitable_alternative=self.alternative_names[max_index]
        print(f"The most suitable alternative is:-{self.most_suitable_alternative} with score of {self.rank_array[max_index]}")
        
