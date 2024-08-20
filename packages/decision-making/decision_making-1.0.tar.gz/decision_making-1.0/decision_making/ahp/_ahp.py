
import numpy as np
from scipy.stats import gmean
import pandas as pd


## Parameter check
'''
Matrix_check_AHP-is object that check whether the parameters provided for AHP is correct or not.
The parameter mainly consists of:-
criteria_names-consists of names of the criteria
alternative_names-consists of names of the alternatives
matrix_per_criteria-consist of 3d tensor that contain alternative-alternative comparision per criteria
criteria_comparison-consist of comparision between criterias(This can also contain weights in 1d numpy array)
custom_inconsistency-default assigned as 0.1 that rules out any matrix if it's consistency is beyond the prescribed value
show_consistency-shows the consistency table of every matrix.
'''

class Matrix_check_AHP:
    
    def __init__(self, criteria_names, alternative_names, matrix_per_criteria, criteria_comparison, custom_inconsistency=0.1, show_consistency=True):
        
        
        '''
        Assign values to the objects atrributes.
        '''
        self.criteria_names=criteria_names
        self.alternative_names=alternative_names
        self.matrix_per_criteria=matrix_per_criteria
        self.criteria_comparison=criteria_comparison
        self.inconsistency=custom_inconsistency
        self.check_redundancy=0
        self.show_consistency=show_consistency
        
        #dimention and the consistency will be checked on the spot
        '''
        this function check_dimentions_and_dtype checks everythings
        if any error is raised, it will show and it wont proceed
        if not, we will see the message-"Everything is fine"
        '''

        self.check_dimentions_and_dtype()
        print("Parameter check: PASSED")  
        
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
        
        #check whether each element is numpy array or not
        if type(self.matrix_per_criteria)!=np.ndarray:
            self.check_redundancy=1
            raise ValueError("Element in the matrix_per_criteria is not numpy array.")
            
        if self.matrix_per_criteria.dtype!=float and self.matrix_per_criteria.dtype!=int:
            self.check_redundancy=1
            raise ValueError("Dtype of matrix_per_criteria must be float or int")
            
        if self.matrix_per_criteria.ndim!=3:
            self.check_redundancy=1
            raise ValueError("The dimention of the element in matrix_per_criteria is not 3D.")
            
        if self.matrix_per_criteria.shape[0]!=criteria_len or self.matrix_per_criteria.shape[1]!=alternative_len or self.matrix_per_criteria.shape[2]!= alternative_len:
            self.check_redundancy=1
            raise ValueError(f"The shape of the element in matrix list of criteria is not correct. It should be ({criteria_len},{alternative_len}, {alternative_len})")
            
        #every guy must have value > 0
        if (self.matrix_per_criteria <= 0).any():
            self.check_redundancy=1
            raise ValueError("The element in the matrix list of criteria must have value greater than 0")
            
        #finally for the last guy
        if type(self.criteria_comparison)!=np.ndarray:
            self.check_redundancy=1
            raise ValueError("The criteria comparision is not numpy array.")  
            
        if self.criteria_comparison.dtype!=float and self.criteria_comparison.dtype!=int:
            self.check_redundancy=1
            raise ValueError("Dtype of matrix_per_criteria must be float or int")
        
        if self.criteria_comparison.ndim!=1 and self.criteria_comparison.ndim!=2:
            self.check_redundancy=1
            raise ValueError("The dimention of the element in criteria comparision is not 1D/2D.")
            
        if self.criteria_comparison.ndim==1:
            if self.criteria_comparison.shape[0]!=criteria_len:
                self.check_redundancy=1
                raise ValueError("The number of element in criteria comparision is not correct")
        
        if self.criteria_comparison.ndim==2:
            if self.criteria_comparison.shape[0]!=criteria_len or self.criteria_comparison.shape[1]!=criteria_len:
                self.check_redundancy=1
                raise ValueError("The row or columns of the element in criteria comparision is not correct.")
        
        #every guy must have value>0
        if (self.criteria_comparison <= 0).any():
            self.check_redundancy=1
            raise ValueError("The element in the criteria comparision must have value greater than 0")
            
        #check whether the consistency is numerical value of not
        if type(self.inconsistency)!=float and type(self.inconsistency)!=int:
            self.check_redundancy=1
            raise ValueError("The inconsistency value must be a integer")
        
        #check for the consistency
        self.consistency_check_overall()
    
    
    def consistency_check_overall(self):
        #calculate the consistency per alternative-alternative comparision
        list_consistency_per_criteria=[]
        for matrix in self.matrix_per_criteria:
            list_consistency_per_criteria.append(self.consistency_check_single_matrix(matrix))
            
        
        consitency_criteria_comparison=None
        #calculate the consistency of criteria_comparison matrix is and only if ndims=2
        if self.criteria_comparison.ndim==2:
            consitency_criteria_comparison=self.consistency_check_single_matrix(self.criteria_comparison)
        
        if self.show_consistency==True:
            
            lis=[[self.criteria_names[i], list_consistency_per_criteria[i]] for i in range(len(self.criteria_names))]
            print("The consistency of alternative-alternative per comparision:-")
            print(pd.DataFrame(lis, columns=['Criteria', 'Consistency']))
            
            if consitency_criteria_comparison==None:
                print("criteria_comparison matrix had ndim=1 which doesn't require consistency matrix")
            else:
                print(f"The consistency of criteria_comparision is:-{consitency_criteria_comparison}")
        
        
        ##check for whether the value of inconsistency is greater than the self.custom_inconsistency
        for i in range(len(list_consistency_per_criteria)):
            if list_consistency_per_criteria[i]>self.inconsistency:
                self.check_redundancy=1
                raise ValueError(f"The matrix with criteria {self.criteria_names[i]} is inconsistent.")
                
        ##similarly check for consitency_criteria_comparison
        if consitency_criteria_comparison!=None and consitency_criteria_comparison>self.inconsistency:
            self.check_redundancy=1
            raise ValueError("The criteria_comparsion matrix is inconsistent")
    
    #ahpmatrix should be 2d numpy araay with height and width.
    #this only works for 50*50 array at max
    def consistency_check_single_matrix(self,ahpmat):
        #this calculated consistency of a given matrix.
        matrix = ahpmat
        maxeigen = None
        CI = None
        CR = None
        RI = [0.0000000, 0.0000000, 0.5251686, 0.8836651, 1.1081014, 1.2492774, 1.3415514, 1.4048466, 1.4507197, 1.4857266, 1.5141022,
          1.5356638, 1.5545925, 1.5703498, 1.5839958, 1.5955704, 1.6053208, 1.6140648, 1.6218900, 1.6288505, 1.6355145, 1.6410749,
          1.6462439, 1.6509834, 1.6554325, 1.6592237, 1.6631050, 1.6662368, 1.6696396, 1.6723214, 1.6751007, 1.6778474, 1.6801459,
          1.6824754, 1.6844494, 1.6865981, 1.6884438, 1.6901943, 1.6918461, 1.6935071, 1.6950605, 1.6965334, 1.6979425, 1.6992006,
          1.7004654, 1.7016392, 1.7027780, 1.7038778, 1.7050314, 1.7060381] + [1.7060381] * 1000

        if(matrix.shape[0]>50):
            raise ValueError("The attributes must be less than 50")
        
        #figure out the value of CR(consistency ratio)
        eigenvalues = np.linalg.eigvals(matrix)
        maxeigen=max(eigenvalues.real[np.abs(eigenvalues.imag) < 0.000001])
        CI=(maxeigen-matrix.shape[0])/(matrix.shape[0]-1)
        CR=CI/RI[matrix.shape[0]-1]
        return CR   



##AHP
    
'''
The function returns the most suitable alternative provided the criteria_names, alternative_names, matrix_per_criteria, criteria_comparison
It also inherits Matrix_check_AHP which check whether the parameters provided is correct or not
If any error is raised in Matrix_check_AHP then the process wont proceed else it will show the results.
The displayed result depends on what user want.
If they wish to see that the weight matrix in the end then they can see it tuning the value of print_weight_matrix which is by default set to false
If they wish to see that the rank array in the end then they can see it tuning the value of rank_array which is by default set to True
'''
class Ahp(Matrix_check_AHP):
    
    def __init__(self, criteria_names, alternative_names, matrix_per_criteria, criteria_comparison, custom_inconsistency=0.1,
                print_weight_matrix=False, print_rank_array=True):
        
        '''
        Used the inherited Matrix_check_AHP function
        '''
        
        super().__init__(criteria_names, alternative_names, matrix_per_criteria, criteria_comparison, custom_inconsistency)
        
        '''
        Assign values to other attributes
        '''
        #the rank array stores the score of every alternative in their respective order
        self.rank_array=None
        
        #user can see the normalized and weighted matrix using the class atributes
        self.normalized_unweighted_matrix=None
        self.weighted_matrix=None
        self.most_suitable_alternative=None
        self.print_weight_matrix=print_weight_matrix
        self.print_rank_array=print_rank_array
        
        '''
        The find_chart does the heavy lifting. It does all the computation part
        Since we have deployed 2d/3d tensors instead of normals lists, we get to see good efficiency and reduced computation
        Once this is done, we have calculated the weighted_matrix and rank_array.
        Once done we can use show find to print the best alternative
        '''
        
        self.find_chart() #<-computation
        self.show()
        

    def find_chart(self):
        #iterate through every matrix_per_criteria to find the geometric mean and then stacking the array one by one
        geometric_mean_matrix=None
        p=self.matrix_per_criteria/np.sum(self.matrix_per_criteria, axis=1, keepdims=True)
        geometric_mean_matrix=gmean(p, axis=2).T
        
        #the shape of geometric_mean_matrix is (len(alternative_names),len(criteria_names)). 
        #We must multiple this with the weight array we got from criteria_comparison matrix
        if self.criteria_comparison.ndim==2:
            t=self.criteria_comparison
            weight_array=gmean(t/t.sum(axis=0), axis=1)
        else:
            weight_array=self.criteria_comparison
        
        #now since we got these both matrix, we can find the resultant matrix which can give us weight matrix
        #then we can find out the ranks
        
        #but first of all we can assign the weight_array to 
        self.normalized_unweighted_matrix=geometric_mean_matrix.copy()
        
        #we have the weighted_matrix
        self.weighted_matrix=weight_array.reshape(1,-1) * geometric_mean_matrix
        
#         print(weight_array.reshape(1,-1).shape, geometric_mean_matrix.shape)
        
        #find the rank array
        self.rank_array=np.sum(self.weighted_matrix, axis=1)
    
    def show(self):
        if self.print_weight_matrix!=False:
            print("The rank matrix is:-")
            print(pd.DataFrame(self.weighted_matrix, index=self.alternative_names, columns=self.criteria_names))
            
        print()
        if self.print_rank_array!=False:
            print(f"The rank array is: {self.rank_array}")
            
        print()
            
        #now I have self.rank_array and self.alternative_names
        
        # Combine list and array into a list of tuples
        combined = list(zip(self.alternative_names, self.rank_array))
        
        # Sort the list of tuples based on the values in the array (in descending order)
        sorted_combined = sorted(combined, key=lambda x: x[1], reverse=True)
        
        self.most_suitable_alternative=sorted_combined[0][0]
        
        for index, ele in enumerate(sorted_combined):
            print(f"{index+1}. {ele[0]} has value = {ele[1]}")
        print()
        
        print(f"The most suitable alternative to choose is :- {self.most_suitable_alternative}")