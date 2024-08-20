from ._ahp import Ahp

def ahp(criteria_names, alternative_names, matrix_per_criteria, criteria_comparison, custom_inconsistency=0.1, print_weight_matrix=False, print_rank_array=True):
    try:
        return Ahp(criteria_names, alternative_names, matrix_per_criteria, criteria_comparison, custom_inconsistency , print_weight_matrix, print_rank_array)
    except ValueError as ve:
        print(f'Error: {ve}')