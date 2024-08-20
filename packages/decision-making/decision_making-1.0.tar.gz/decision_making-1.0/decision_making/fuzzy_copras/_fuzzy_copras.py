import pandas as pd
import numpy as np


#Parameter check

'''
Check_parameters_FUZZY_COPRAS-is object that check whether the parameters provided for COPRAS is correct or not.
The parameter mainly consists of:-


criteria_names-consists of names of the criteria. The criteria can be benifit or cost criteria.

alternative_names-consists of names of the alternatives.

data-consist of data provided by the user. 

benificial_cost_mark- keep track of attributes which are either cost or benefit.

decision_makers-you can either provide the names of the decision makers or provide numebr of decision makers-since
the name of the decision makers wont impact the final result, so we wont constrain you from not providing the name of decision 
makers.
However, the number of decision makers must be atleast one to provide weights to the criterias.

fuzzy_table-will map the fuzzy number from it's respective linguistic term present in the criteria_comparison.
fuzzy_table is a dictionary which contains key as linguistic term and values as list containing fuzzy numbers.
Since different people have different fuzzy_table, we inspire that you must provide your own fuzzy_table.

criteria_comparison- a numpy array that contains data that determine the weight of different criteria based on the linguistic
term
provided by different decision makers.
'''

class Check_parameters_FUZZY_COPRAS:
    
    def __init__(self, criteria_names, alternative_names, data, benificial_cost_mark, decision_makers, fuzzy_table, criteria_comparison):
        '''
        Assign values to the objects atrributes.
        '''
        self.criteria_names=criteria_names
        self.alternative_names=alternative_names
        self.data=data
        self.benificial_cost_mark=benificial_cost_mark
        self.decision_makers=decision_makers
        self.fuzzy_table=fuzzy_table
        self.criteria_comparison=criteria_comparison
        self.check_redundancy=0
        
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
        
        #----------------------------------------------------------------------------------------
    
        #check for self.data

        if(type(self.data)!=np.ndarray):
            self.check_redundancy=1
            raise ValueError("The data provided is not numpy array")
        #the self.data should have dtype as float or int
        if(not(self.data.dtype=='int' or self.data.dtype=='float')):
            self.check_redundancy=1
            raise ValueError("The dtype of the given data should either be int or float")
            
        #check for dimentions
        if(self.data.ndim!=2):
            self.check_redundancy=1
            raise ValueError("The numpy tensor doesnt have dimention=2")
        
        #check for the shape of data provided
        if(self.data.shape[0]!=len(self.alternative_names) or self.data.shape[1]!=len(self.criteria_names)): # type: ignore
            self.check_redundancy=1
            raise ValueError("The shape of the data provided is inconsistent")

            
        #----------------------------------------------------------------------------------------
        

        #check whether the beneficial_cost_mark is a list or not
        if type(self.benificial_cost_mark)!=list and type(self.benificial_cost_mark)!=np.ndarray:
            self.check_redundancy=1
            raise ValueError("The benificial_cost_mark is neither list nor np.array")
            
        #check if beneficial_cost_mark is nd.array, it should have one dimention and shape must be good
        if type(self.benificial_cost_mark)==np.ndarray:
            if self.benificial_cost_mark.ndim!=1 or self.benificial_cost_mark.shape[0]!=len(self.criteria_names):
                self.check_redundancy=1
                raise ValueError("The benificial_cost_mark must have 1 dim or correct length")
        
        #if benificial_cost_mark is not np.array, then it must be a list, in that case check its length 
        if type(self.benificial_cost_mark)!=list or len(self.benificial_cost_mark)!=len(self.criteria_names):
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

    
        #----------------------------------------------------------------------------------------
        
        #check for decision_makers
        
        #the decision_makers must be a list or integer value
        if type(self.decision_makers)!=list and type(self.decision_makers)!=int:
            self.check_redundancy=1
            raise ValueError("The decision makers must be a list or a numeric value")
            
        #if the decision_maker is a list, assign it with the length of the decision maker list.
        #because either ways it wont impact the result
        if type(self.decision_makers)==list:
            self.decision_makers=len(self.decision_makers)
            
        #and there must be atleast one decision maker
        if self.decision_makers<1:
            self.check_redundancy=1
            raise ValueError("The decision makers length cannot be less than 1")
            
        
        #----------------------------------------------------------------------------------------
        
        
        #now check for fuzzy_table
        #check that every key in the dictionary is a string
        #check that every value has a list of size three all consisting of numerical values
        
        for key, value in self.fuzzy_table.items():
            if type(key)!=str:
                self.check_redundancy=1
                raise ValueError("The key in the fuzzy_table is not string")
                
            if type(value)!=list:
                self.check_redundancy=1
                raise ValueError("The value in the fuzzy_table is not list")
            
            if len(value)!=3:
                self.check_redundancy=1
                raise ValueError("The value in the fuzzy_table does not have size equal to 3")
            
            for i in value:
                if type(i)!=int and type(i)!=float:
                    self.check_redundancy=1
                    raise ValueError("The items in values in fuzzy_table is not numeric")
                    
        
        #----------------------------------------------------------------------------------------
        
        #for criteria_comparison, we must check:-
        #if criteria_comparison is numpy array
        #if the number of dimentions in equal to 2
        #is the number of rows equal to len(criteria_names) and columns equals decision_makers
        
        if type(self.criteria_comparison)!=np.ndarray:
            self.check_redundancy=1
            raise ValueError("The criteria comparision is not numpy array.")
            
        #the dimentions must be 2 as we are only accepting comparision matrix
        if self.criteria_comparison.ndim!=2:
            self.check_redundancy=1
            raise ValueError("The dimention of the element in criteria comparision is not 2D.")
            
            
        #check the shape
        if self.criteria_comparison.shape[0]!=len(self.criteria_names) or self.criteria_comparison.shape[1]!=self.decision_makers:
            self.check_redundancy=1
            raise ValueError("The row or columns of the element in criteria comparision is not correct.")
            
        #check whether every element if present in the key provided in the fuzzy table or not
        for i in range(len(self.criteria_names)):
            for j in range(self.decision_makers):
                if self.criteria_comparison[i][j] not in self.fuzzy_table:
                    self.check_redundancy=1
                    raise ValueError("The element not present in the dictionary")


#Fuzzy-COPRAS

'''
The function returns the most suitable alternative provided the criteria_names, alternative_names, data, 
benificial_cost_mark, decision_makers, fuzzy_table, criteria_comparison, show_rank_arry 
It also inherits Check_parameters_FUZZY_COPRAS which check whether the parameters provided is correct or not
If any error is raised in Check_parameters_FUZZY_COPRAS then the process wont proceed else it will show the results.
The displayed result depends on what user want.
If they wish to see that the rank array in the end then they can see it tuning the value of rank_array which is by 
default set to True
The rank array consist of the score it gave to every alternative
'''


class FUZZY_COPRAS(Check_parameters_FUZZY_COPRAS):
    def __init__(self, criteria_names, alternative_names, data, benificial_cost_mark, decision_makers, fuzzy_table, criteria_comparison, show_rank_arry=True):
        '''
        Used the inherited Check_parameters_FUZZY_COPRAS function
        '''
        super().__init__(criteria_names, alternative_names, data, benificial_cost_mark, decision_makers, fuzzy_table, criteria_comparison)
        
        '''
        Assign values to other attributes
        '''
        self.normalized_data=None
        self.fuzzy_criteria_comparison=None
        self.fuzzy_aggregated_matrix=None
        self.fuzzy_weighted_normalized_matrix=None
        self.fuzzy_bi=None
        self.fuzzy_ci=None
        self.fuzzy_qi=None
        self.rank_array=None
        self.show_rank_array=show_rank_arry
        self.solve()
        '''
        Once solved we can show the result
        '''
        self.show()
        
        
        
        
    def solve(self):
        #the first thing is lets store the size of criteria_names, alternative_names and decision_makers in 
        #variable a, b and c
        #these variable will help us in computation and parallelism
        a=len(self.criteria_names)
        b=len(self.alternative_names)
        c=self.decision_makers
        
        #now compute the normalized_data, this can be used to get the fuzzy_weighted_normalized_matrix as we proceed
        self.normalized_data=self.data/self.data.sum(axis=0)
        
        
        #fuzzy_criteria_comparison contains the criteria_comparison matrix replaced with fuzzy numbers
        self.fuzzy_criteria_comparison=np.ones((a,c,3))
        
        for i in range(a):
            for j in range(c):
                self.fuzzy_criteria_comparison[i][j]=np.array(self.fuzzy_table[self.criteria_comparison[i][j]])
                
        #so we have got the fuzzy_criteria_comparison which has shape of (a, c, 3)
    
        #now we need to get the fuzzy_aggregated_matrix which is aggregation of all the fuzzy number given by various
        #decision maker. We use arithmatic mean for this purpose.
        #the fuzzy_aggregated_matrix represents the weight of each criteria but in the form of fuzzy numbers
        
        self.fuzzy_aggregated_matrix=np.mean(self.fuzzy_criteria_comparison, axis=1)
        
        #the will fuzzy_aggregated_matrix will have shape of (a,3) that will be multiplied with the normalized_data
        #of shape (b,a) and the result matrix we get is fuzzy_weighted_normalized_matrix that will have a shape
        #of (b, a, 3)
        
        
        #so we will need python broadcasting to make this possible
        data_extend_axis=self.normalized_data[:, :, np.newaxis]
        self.fuzzy_weighted_normalized_matrix=data_extend_axis*self.fuzzy_aggregated_matrix
        
        
        
        #now we need to compute bi and ci
        #both of these will have a dimention of (b, 1)
        self.fuzzy_bi=np.sum(np.sum(self.fuzzy_weighted_normalized_matrix*(self.benificial_cost_mark[:, np.newaxis]), axis=-1),axis=-1).reshape(-1, 1)
        self.fuzzy_ci=np.sum(np.sum(self.fuzzy_weighted_normalized_matrix*(1-self.benificial_cost_mark[:, np.newaxis]), axis=-1), axis=-1).reshape(-1, 1)
        

        
        #now compute fuzzy_qi-this will have the same dimention as fuzzy_bi which is (b,1)
        self.fuzzy_qi=self.fuzzy_bi+np.min(self.fuzzy_ci)*np.sum(self.fuzzy_ci)/(self.fuzzy_ci*np.sum(min(self.fuzzy_ci)/self.fuzzy_ci))
        
        
        #now compute the rank array which is nothing but 'ui'
        #the rank array or the udi
        self.rank_array=self.fuzzy_qi/np.max(self.fuzzy_qi) * 100
        self.rank_array=self.rank_array.reshape(-1)
        
#         print(self.rank_array)
        
        
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
            
            print(pd.DataFrame(show, index=self.alternative_names, columns=['Score(Udi)', 'Rank']))
            
        #show the most suitable alternative
        max_index = np.argmax(self.rank_array)
        self.most_suitable_alternative=self.alternative_names[max_index]
        print(f"The most suitable alternative is:-{self.most_suitable_alternative} with score of {self.rank_array[max_index]}")

