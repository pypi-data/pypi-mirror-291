from ._fuzzy_copras import FUZZY_COPRAS

def fuzzy_copras(criteria_names, alternative_names, data, benificial_cost_mark, decision_makers, fuzzy_table, criteria_comparison, show_rank_arry=True):
    try:
        return FUZZY_COPRAS(criteria_names, alternative_names, data, benificial_cost_mark, decision_makers, fuzzy_table, criteria_comparison, show_rank_arry)
    except ValueError as ve:
        print(f'Error: {ve}')
