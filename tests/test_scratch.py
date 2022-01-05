import json
filepath = 'examples/dsm_v/dsm_v_labelled.json'
with open(filepath) as f:
    data = json.load(f)

from comorbid_graphs import ComorbidGraph
cg = ComorbidGraph(json_data=data)

# Example: Which Disorders in 'DSM-V' contain the term 'depressive disorder'?
# (but I am not interested in neurodevelopmental disorders, and skip small docs too - 
# say skip disorders smaller than 100 characters of text)

query_string = """
asdasdasdasd
"""
results_cg = cg.advanced_search(query_string, title="Searching results")
results_cg.print_head()
