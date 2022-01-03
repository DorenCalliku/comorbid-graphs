import json
from anytree import PostOrderIter
from comorbid_graphs import ComorbidGraph, ComorbidGraphNode

with open('tests/fixtures/symp_tree.json') as f:
    data = json.load(f)
cg = ComorbidGraph(data, ComorbidGraphNode, assign_ids=True)

cg.process_graph([cg])
