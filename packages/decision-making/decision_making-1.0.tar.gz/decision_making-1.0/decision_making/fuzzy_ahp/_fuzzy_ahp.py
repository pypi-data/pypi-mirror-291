import numpy as np
from scipy.stats import gmean
import pandas as pd

#Parameter chcek

'''
Matrix_check_FUZZY_AHP-is object that check whether the parameters provided for Fuzzy_Ahp is correct or not.
The parameter mainly consists of:-
criteria_names-consists of names of the criteria
alternative_names-consists of names of the alternatives
matrix_per_criteria-consist of 3d tensor that contain alternative-alternative comparision per criteria in form of human 
semantics
criteria_comparison-consist of comparision between criterias in form of human semantics.
'''

class Matrix_check_FUZZY_AHP:
    
    def __init__(self, criteria_names, alternative_names, matrix_per_criteria, criteria_comparison, fuzzy_table):
        
        '''
        Assign values to the objects atrributes.
        '''
        
        self.criteria_names=criteria_names
        self.alternative_names=alternative_names
        self.matrix_per_criteria=matrix_per_criteria
        self.criteria_comparison=criteria_comparison
        self.fuzzy_table=fuzzy_table
        self.check_redundancy=0
        
        '''
        the function check_dimentions_and_dtype checks everythings
        if any error is raised, it will show and it wont proceed
        if not, we will see the message-"Everything is fine"
        '''
        
        self.check_dimentions_and_dtype()
        print("Parameter check: Passed")

    
    
    def check_dimentions_and_dtype(self):
        
        #check for dtype
        if type(self.criteria_names)!=list:
            self.check_redundancy=1
            raise ValueError("The criterias must be a list of string.")
        #check if every element in the array is string
        for ele in self.criteria_names:
            if type(ele)!=str:
                self.check_redundancy=1
                raise ValueError("Element in the criteria list is not string.")
        
        #do the same for self.alternative_names
        if type(self.alternative_names)!=list:
            self.check_redundancy=1
            raise ValueError("The alternatives must be a list of string.")
        #check if every element in the array is string
        for ele in self.alternative_names:
            if type(ele)!=str:
                self.check_redundancy=1
                raise ValueError("Element in the alternative list is not string.")
            
        #find the length of self.criteria_names and self.alternative_names
        
        criteria_len=len(self.criteria_names)
        alternative_len=len(self.alternative_names)
        
        #--------------------------------------------------------
        
        
        #now check fuzzy_table
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
                    
        #--------------------------------------------------------
                    
        
        #check whether each element is numpy array or not

        if type(self.matrix_per_criteria)!=np.ndarray:
            self.check_redundancy=1
            raise ValueError("Element in the matrix_per_criteria is not numpy array.")    
         
        if self.matrix_per_criteria.ndim!=3:
            self.check_redundancy=1
            raise ValueError("The dimention of the element in matrix_per_criteria is not 3D.")
            
        if self.matrix_per_criteria.shape[0]!=criteria_len or self.matrix_per_criteria.shape[1]!=alternative_len or self.matrix_per_criteria.shape[2]!= alternative_len:
            self.check_redundancy=1
            raise ValueError(f"The shape of the element in matrix list of criteria is not correct. It should be ({criteria_len}, {alternative_len}, {alternative_len})")
            
        #check whether every element if present in the key provided in the fuzzy table or not
        
        m=len(self.criteria_names)
        n=len(self.alternative_names) 
        
        for i in range(m):
            for j in range(n):
                for k in range(n):
                    if self.matrix_per_criteria[i][j][k] not in self.fuzzy_table:
                        self.check_redundancy=1
                        raise ValueError("The element not present in the dictionary")
                    
            
        
        #-------------------------------------------------------- 
        
            
        #finally for the last guy which is self.criteria_comparison
        
        if type(self.criteria_comparison)!=np.ndarray:
            self.check_redundancy=1
            raise ValueError("The criteria comparision is not numpy array.")
            
        #the dimentions must be 2 as we are only accepting comparision matrix
        if self.criteria_comparison.ndim!=2:
            self.check_redundancy=1
            raise ValueError("The dimention of the element in criteria comparision is not 2D.")
            
        #check the shape
        if self.criteria_comparison.shape[0]!=criteria_len or self.criteria_comparison.shape[1]!=criteria_len:
            self.check_redundancy=1
            raise ValueError("The row or columns of the element in criteria comparision is not correct.")
        
        #check whether every element if present in the key provided in the fuzzy table or not
        for i in range(m):
            for j in range(m):
                if self.criteria_comparison[i][j] not in self.fuzzy_table:
                    self.check_redundancy=1
                    raise ValueError("The element not present in the dictionary")
        #-------------------------------------------------------- 



#Fuzzy_AHP
'''
The function returns the most suitable alternative provided the criteria_names, alternative_names, matrix_per_criteria, 
criteria_comparison and fuzzy_table
It also inherits Matrix_check_FUZZY_AHP which check whether the parameters provided is correct or not
If any error is raised in Matrix_check_FUZZY_AHP then the process wont proceed else it will show the results.
The displayed result depends on what user want.
If they wish to see that the weight matrix in the end then they can see it tuning the value of print_weight_matrix which is 
by default set to false
If they wish to see that the rank array in the end then they can see it tuning the value of rank_array which is by default set
to True
'''

class Fuzzy_Ahp(Matrix_check_FUZZY_AHP):
    def __init__(self, criteria_names, alternative_names, matrix_per_criteria, criteria_comparison, fuzzy_table, print_weight_matrix=False, print_rank_array=True, print_fuzzy_table=False):
        
        '''
        Used the inherited Matrix_check_FUZZY_AHP function
        '''
    
        super().__init__(criteria_names, alternative_names, matrix_per_criteria, criteria_comparison, fuzzy_table)
        self.rank_array=None
        
        #we have used two attributes which keep the fuzzy representation of matrix_per_criteria and criteria_comparison
        #this can be useful for the user
        self.fuzzy_representation_of_matrix_per_criteria=None
        self.fuzzy_representation_of_criteria_comparison=None
        
        #we have used to attribute to store the unweighted_matrix and weighted_matrix, user might use these information
        self.unweighted_matrix=None
        self.weighted_matrix=None
        self.most_suitable_alternative=None
        
        '''
        Assign values to other attributes
        '''
        self.print_weight_matrix=print_weight_matrix
        self.print_rank_array=print_rank_array
        self.print_fuzzy_table=print_fuzzy_table
        self.fuzzy_table_rep=None
        
        '''
        The find_chart does the heavy lifting. It does all the computation part
        Since we have deployed 2d/3d and even 4d tensors instead of normals lists, we get to see good efficiency and reduced 
        computation
        Once this is done, we have calculated the weighted_matrix and rank_array.
        Once done we can use show find to print the best alternative
        '''
        
        self.find_chart() #<-computation
        self.show()
        
        
    def find_chart(self):
        #maintained a copy
        a=self.matrix_per_criteria  
        
        m=len(self.criteria_names)
        n=len(self.alternative_names) 
        
        #declare a 4d tensor which keeps the fuzzy weights
        t=np.ones((m, n, n, 3)) 
        
        #assign the fuzzy_array to tensor t
        for i in range(m):
            for j in range(n):
                for k in range(n):
                    t[i][j][k]=np.array(self.fuzzy_table[a[i][j][k]])
        
        self.fuzzy_representation_of_matrix_per_criteria=t
                    
        
        #find geometric mean in t tensor
        fuzzy_geometric_mean=gmean(t, axis=2)
        
        #apply transformation
        #transformation-> wi=ri * (r1 + r2 + r3 ---- rn)'s inverse
        
        #the next few compacted step can fulfill the steps
        
        k=np.sum(fuzzy_geometric_mean, axis=1, keepdims=True)
        k=1/k
        p=k[:, :, ::-1]
        fuzzified_matrix=fuzzy_geometric_mean*p
        final_matrix_unweighted=(np.sum(fuzzified_matrix, axis=2)/3).T
        
        
        final_matrix_comparision=None
        #now we will do the same thing to find the criteria_comparison matrix

        a_comparision=self.criteria_comparison
        t_comparision=np.ones((m, m, 3))



        for i in range(m):
            for j in range(m):
                t_comparision[i][j]=np.array(self.fuzzy_table[a_comparision[i][j]])

        self.fuzzy_representation_of_criteria_comparison=t_comparision

        fuzzy_geometric_mean_comparision=gmean(t_comparision, axis=1)

        #the computation stuff
        k_comparision=np.sum(fuzzy_geometric_mean_comparision, axis=0, keepdims=True)
        k_comparision=1/k_comparision
        p_comparision=k_comparision[:, ::-1]
        fuzzified_matrix_comparision=fuzzy_geometric_mean_comparision*p_comparision
        final_matrix_comparision=(np.sum(fuzzified_matrix_comparision, axis=1)/3).T
        
        #keep the copy of final_matrix_unweighted in self.normalized_unweighted_matrix
        self.unweighted_matrix=final_matrix_unweighted
    
        #we have the weighted_matrix
        self.weighted_matrix=final_matrix_comparision.reshape(1,-1) * final_matrix_unweighted
        #find the rank_array
        self.rank_array=np.sum(self.weighted_matrix, axis=1)
        
        
    def show(self):
        if self.print_weight_matrix!=False:
            print("The rank matrix is:-")
            print(pd.DataFrame(self.weighted_matrix, index=self.alternative_names, columns=self.criteria_names))
            
        print()
        
        if self.print_rank_array!=False:
            print(f"The rank array is: {self.rank_array}")
            
        print()
        
        self.fuzzy_table_rep=pd.DataFrame(self.fuzzy_table , index=["low", "medium", "high"]).T
        if self.print_fuzzy_table==True:
            print("The fuzzy table is:-")
            print(self.fuzzy_table_rep)
            
        #now I have self.rank_array and self.alternative_names
        
        # Combine list and array into a list of tuples
        combined = list(zip(self.alternative_names, self.rank_array))
        
        # Sort the list of tuples based on the values in the array (in descending order)
        sorted_combined = sorted(combined, key=lambda x: x[1], reverse=True)
        
        self.most_suitable_alternative=sorted_combined[0][0]
        
        for index, ele in enumerate(sorted_combined):
            print(f"{index+1}. {ele[0]} has value = {ele[1]}")
            
        print(f"The most suitable alternative to choose is :- {self.most_suitable_alternative}")

