from ._fuzzy_topsis import FUZZY_TOPSIS


def fuzzy_topsis(criteria_names, alternative_names, data, weights_criteria, benificial_cost_mark, dict_encode,show_rank_array=True):
    try:
        FUZZY_TOPSIS(criteria_names, alternative_names, data, weights_criteria, benificial_cost_mark, dict_encode,show_rank_array)
    except ValueError as ve:
        print(f'Error : {ve}')