from ._copras import COPRAS

def copras(criteria_names, alternative_names, data, weights_criteria, benificial_cost_mark, show_rank_array=True):
    try:
        COPRAS(criteria_names, alternative_names, data, weights_criteria, benificial_cost_mark, show_rank_array)
    except ValueError as ve:
        print(f'Error: {ve}')