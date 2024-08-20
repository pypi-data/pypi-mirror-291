
import pandas as pd
import numpy as np

## Parameter check
'''
Check_parameters_TOPSIS-is object that check whether the parameters provided for TOPSIS is correct or not.
The parameter mainly consists of:-
criteria_names-consists of names of the criteria
alternative_names-consists of names of the alternatives
data-consist of data provided by the user. The data can have either numerical (int/float) or non numerica (object/string) values
weights_criteria-This keeps the weight of the attributes which can be multiplied to normalized matrix in order to get weight normalized matrix
benificial_cost_mark- keep track of attributes which are either cost or benefit
dict_encode(sometimes mandatory sometimes not)-maps the value of non numeric value to numeric but only mandatory if data has non numerical features
'''

class Check_parameters_TOPSIS:
    
    def __init__(self, criteria_names, alternative_names, data, weights_criteria, benificial_cost_mark, dict_encode=None):
        '''
        Assign values to the objects atrributes.
        '''
        self.criteria_names=criteria_names
        self.alternative_names=alternative_names
        self.data=data
        self.dict_encode=dict_encode
        self.benificial_cost_mark=benificial_cost_mark
        self.weights_criteria=weights_criteria
        self.check_redundancy=0
        self.data_in_numpy=None
        
        
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
        #------------------------------------------------------------------------------

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

            
        #------------------------------------------------------------------------------
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
        #--------------------------------------------------------------------------------
        
        
            
        #check whether data provide is dataframe
        if type(self.data)!=pd.core.frame.DataFrame:
            self.check_redundancy=1
            raise ValueError("The data is not pd.core.frame.DataFrame")
            
        #check whether the data has same number of rows and columns as prescribed criteria and alternatives
        if self.data.shape[0]!=len(self.alternative_names) and self.data.shape[1]!=len(self.criteria_name):
            self.check_redundancy=1
            raise ValueError("The shape of the data is not correct")
            
        #we are gonna replace all the columns having int datatype to float datatype
        for column in self.data.select_dtypes(include=['int']):
            self.data[column] = self.data[column].astype(float)

        #if any dtype is not numeric then we need to ask for the dict_encode otherwise no need
        check_for_non_numeric=False
        for i in self.data.dtypes.values:
            if (i=='int' or i=='float')==False:
                #confirmed that 'object' or 'string' datatype present
                check_for_non_numeric=True
                break
        
        #check whether the dict_encode is present or None
        if check_for_non_numeric==True:
            if type(self.dict_encode)!=dict:
                self.check_redundancy=1
                raise ValueError("The dict is not right")
        
        #now check whether each key and value is string and numeric
        if type(self.dict_encode)==dict:
            for key, value in self.dict_encode.items():
                if not isinstance(key, str):
                    self.check_redundancy=1
                    raise ValueError("The key of the dictionary provided is not string")
                if not isinstance(value, (int, float)):
                    self.check_redundancy=1
                    raise ValueError("The key of the dictionary provided is not numeric")
        
        #now all we have to do is to encode the categorical columns in the dataframe and encode it with the values
        data_copy=self.data.copy()
        for col, dt in data_copy.dtypes.items():
            if (dt=='int' or dt=='float')==False:
                data_copy[col] = data_copy[col].map(self.dict_encode)

        #suppose if any element isn't present, then we must figure it out        
        for col in self.data.select_dtypes(include=['object']).columns: 
            unique_values = self.data[col].unique() 
            for value in unique_values:
                if value not in self.dict_encode: 
                    raise ValueError(f"Value '{value}' in column '{col}' does not have a corresponding encoding in dict_encode")
            
        self.data_in_numpy=np.array(data_copy.values, dtype='float')
        
#         print(data_copy)
#         print(self.data_in_numpy)
#         print(self.benificial_cost_mark)
#         print(self.weights_criteria)



##TOPSIS
'''
The function returns the most suitable alternative provided the criteria_names, alternative_names,data, weights_criteria, benificial_cost_mark, dict_encode
It also inherits Check_parameters_TOPSIS which check whether the parameters provided is correct or not
If any error is raised in Check_parameters_TOPSIS then the process wont proceed else it will show the results.
The displayed result depends on what user want.
If they wish to see that the rank array in the end then they can see it tuning the value of rank_array which is by default set to True
The rank array consist of the score it gave to every alternative
'''

class TOPSIS(Check_parameters_TOPSIS):
    def __init__(self,criteria_names, alternative_names, data, weights_criteria, benificial_cost_mark, dict_encode=None, show_rank_array=True):
        '''
        Used the inherited Check_parameters_TOPSIS function
        '''
        super().__init__(criteria_names, alternative_names, data, weights_criteria, benificial_cost_mark, dict_encode)

        
        '''
        Assign values to other attributes
        '''
        #the rank array assign score to every single alternative
        self.rank_array=None
        
        #the normalized_matrix consist of the normalized data from self.data_in_numpy
        self.normalized_matrix=None
        
        #we need to store the values vj_plus(ideal best value) and vj_minus(ideal worst value) for evry criteria
        #user might use these parameters for evaluation
        self.vj_plus=None
        self.vj_minus=None
        
        #we need to keep track of the location of Euclidean distance between the target alternative and the best/worst alternative and for each alternative
        #which is indicated using si_plus and si_minus
        #si_plus is euclidean distance wrt vj_plus of every criteria
        #si_minus is euclidean distance wrt vj_minus of every criteria
        self.si_plus=None
        self.si_minus=None
        
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
        a=self.data_in_numpy

        #apply vector normalization
        p=a/((np.sum(a**2, axis=0)**(1/2)).reshape(1,-1))
        
        #assign p to self.normalized_matrix
        self.normalized_matrix=p

        #get the weighted normalized matrix
        t=self.weights_criteria*p

        #calculate vj+ and vj-
        v_j_plus=np.amax(t, axis=0)
        v_j_minus=np.amin(t, axis=0)
        
        #if we have cost as the criteria then v_j_plus and v_j_minus will be completely opposite
        #swap them if this occur
        for i in range(len(self.benificial_cost_mark)):
            if self.benificial_cost_mark[i]==0:  #this is cost, replace v_j_minum[i] with v_j_plus[i]
                v_j_plus[i], v_j_minus[i]=v_j_minus[i], v_j_plus[i]
        
        #assign the value of v_j_plus and v_j_minus to attribute self.vj_plus and self.vj_minus
        self.vj_plus=v_j_plus.copy()
        self.vj_minus=v_j_minus.copy()

        #calculate si+ and si- , this two can determine the rank array
        s_i_plus=(np.sum((v_j_plus.reshape(1,-1)-t)**2, axis=1, keepdims=True))**(1/2)
        s_i_minus=(np.sum((v_j_minus.reshape(1,-1)-t)**2, axis=1, keepdims=True))**(1/2)
        
        #assign the value of s_i_plus and s_i_minus to attributes self.si_plus and self.si_minus
        self.si_plus=s_i_plus
        self.si_minus=s_i_minus
        
        #calculate the rank_array and determine the rank of the alternative]
        self.rank_array=np.squeeze(s_i_minus/(s_i_plus+s_i_minus))
        
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