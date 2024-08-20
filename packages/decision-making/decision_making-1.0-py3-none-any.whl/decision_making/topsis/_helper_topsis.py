from ._topsis import TOPSIS

def topsis(criteria_names, alternative_names, data, weights_criteria, benificial_cost_mark, dict_encode=None, show_rank_array=True):
    try:
        TOPSIS(criteria_names, alternative_names, data, weights_criteria, benificial_cost_mark, dict_encode, show_rank_array)
    except ValueError as ve:
        print(f'Error: {ve}')