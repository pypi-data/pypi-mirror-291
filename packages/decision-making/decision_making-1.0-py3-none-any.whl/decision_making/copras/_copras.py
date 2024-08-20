import pandas as pd
import numpy as np


#Parameter check

'''
Check_parameters_COPRAS-is object that check whether the parameters provided for COPRAS is correct or not.
The parameter mainly consists of:-
criteria_names-consists of names of the criteria. The criteria can be benifit or cost criteria.
alternative_names-consists of names of the alternatives
data-consist of data provided by the user. 
weights_criteria-This keeps the weight of the attributes which can be multiplied to normalized matrix in order to get weight normalized matrix
benificial_cost_mark- keep track of attributes which are either cost or benefit
'''

class Check_parameters_COPRAS:
    
    def __init__(self, criteria_names, alternative_names, data, weights_criteria, benificial_cost_mark):
        '''
        Assign values to the objects atrributes.
        '''
        self.criteria_names=criteria_names
        self.alternative_names=alternative_names
        self.data=data
        self.benificial_cost_mark=benificial_cost_mark
        self.weights_criteria=weights_criteria
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

            
        #------------------------------------------------------------------------------
        #check whether the weight_criteria is a list or not
        if type(self.weights_criteria)!=list and type(self.weights_criteria)!=np.ndarray:
            self.check_redundancy=1
            raise ValueError("The weight_criteria is neither list nor np.array")
        
        
        #check if weights_criteria is nd.array, it should have one dimention and shape must be good
        if type(self.weights_criteria)==np.ndarray:
            if self.weights_criteria.ndim!=1 or self.weights_criteria.shape[0]!=len(self.criteria_names):
                self.check_redundancy=1
                raise ValueError("The weights_criteria must have 1 dim or correct shape")  
                
        #if weights_criteria is not np.array, then it must be a list, in that case check its length
        if type(self.weights_criteria)!=list or len(self.weights_criteria)!=len(self.criteria_names):
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
        #print(self.weights_criteria)

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


#Copras
'''
The function returns the most suitable alternative provided the criteria_names, alternative_names,data, weights_criteria, benificial_cost_mark, dict_encode
It also inherits Check_parameters_TOPSIS which check whether the parameters provided is correct or not
If any error is raised in Check_parameters_TOPSIS then the process wont proceed else it will show the results.
The displayed result depends on what user want.
If they wish to see that the rank array in the end then they can see it tuning the value of rank_array which is by default set to True
The rank array consist of the score it gave to every alternative
'''

class COPRAS(Check_parameters_COPRAS):
    def __init__(self,criteria_names, alternative_names, data, weights_criteria, benificial_cost_mark, show_rank_array=True):
        '''
        Used the inherited Check_parameters_COPRAS function
        '''
        super().__init__(criteria_names, alternative_names, data, weights_criteria, benificial_cost_mark)
        
        '''
        Assign values to other attributes
        '''
        #the rank array assign score to every single alternative
        self.rank_array=None
        
        #the normalized_matrix consist of the normalized data from self.data_in_numpy
        self.normalized_matrix=None
        
        #this consist of normalized matrix multiplied with the criteria weights
        self.weighted_matrix=None
        
        #bi and ci attributes contain sum of all the respective benifit and cost criteria's sum from the weighted_matrix
        self.bi=None
        self.ci=None
        
        #similar we can have attributes for qi(relative significance) 
        self.qi=None
        
        #udi(utility degree) can be used in rank array that can be used to assign the preference of alternative
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
        a=self.data
        #calculated the normalized matrix
        self.normalized_matrix=a/a.sum(axis=0)
        
        #calculated the weighted matrix
        self.weighted_matrix=self.normalized_matrix*self.weights_criteria.reshape(1,-1)
        
        #get the bi and ci
        self.bi=np.sum(self.weighted_matrix*self.benificial_cost_mark.reshape(1, -1), axis=1, keepdims=True)
        self.ci=np.sum(self.weighted_matrix*(1-self.benificial_cost_mark.reshape(1, -1)), axis=1, keepdims=True)
        
        
        #calculate the qi
        self.qi=self.bi+np.min(self.ci)*np.sum(self.ci)/(self.ci*np.sum(min(self.ci)/self.ci))
        
        #the rank array or the udi
        self.rank_array=self.qi/np.max(self.qi) * 100 
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