from ontology_graphs import OntologyGraph
import json 


def test_load_from_ontology():
    og = OntologyGraph()
    og.load_from_ontology('tests/fixtures/symp.json')
    assert og.tree != None
    assert og.tree.name == 'Source'

    # with open('tests/fixtures/symp_tree.json', 'w+') as f:
    #     json.dump(og.export(), f)

def test_load_from_json():
    og = OntologyGraph()
    with open('tests/fixtures/symp_tree.json') as f:
        data = json.load(f)
    og.load_from_json(data)
    assert og.tree != None
    assert og.tree.name == 'Source'
