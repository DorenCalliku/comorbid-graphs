from comorbid_graphs import ComorbidGraph, ComorbidGraphNode
from comorbid_graphs.searchable.searchable_simple_mixin import SimpleSearchMixin
from anytree import RenderTree


class SimpleComorbidGraph(ComorbidGraph, SimpleSearchMixin):
    pass

import json
with open('tests/fixtures/symp_tree.json') as f:
    data = json.load(f)
simple_cg = SimpleComorbidGraph(data, ComorbidGraphNode, assign_ids=True)

def order_by_score(items):
    return sorted(items, key=lambda item: item.score, reverse=True)

def test_simple_search():
    result_cg = simple_cg.simple_search("symptom", ComorbidGraphNode)
    result_cg.tree.children[0]

    for row in RenderTree(result_cg.tree, childiter=order_by_score, maxlevel=5):
        if hasattr(row.node, 'score'):
            print("%s%s - %s" % (row.pre, row.node.name, row.node.score))
        else:
            print("%s%s" % (row.pre, row.node.name))
