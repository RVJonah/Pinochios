def sql_results_to_dict(results):
    dictionary = []
    for row in results:
        current_row_dict = row.__dict__
        current_row_dict.pop('_sa_instance_state')
        dictionary.insert(0,current_row_dict)
    return dictionary