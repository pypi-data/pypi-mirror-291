from ._fuzzy_ahp import Fuzzy_Ahp

def fuzzy_ahp(criteria_names, alternative_names, matrix_per_criteria, criteria_comparison, fuzzy_table, print_weight_matrix=False, print_rank_array=True, print_fuzzy_table=False):
    try:
        Fuzzy_Ahp(criteria_names, alternative_names, matrix_per_criteria, criteria_comparison, fuzzy_table, print_weight_matrix, print_rank_array, print_fuzzy_table)
    except ValueError as ve:
        print(f'Error: {ve}')
        