from ontology_graphs import OntologyGraph, ontology_graph
import json 

fixtures = {
    "ontologies": [
        'tests/fixtures/symp.json',
        'tests/fixtures/ND.json',
    ],
    "json":[
        'tests/fixtures/symp.json',
        'tests/fixtures/ND.json',
    ]
}

def test_load_from_ontology():
    for ontology_file in fixtures['ontologies']:

        with open(ontology_file) as f:
            data = json.load(f)

        og = OntologyGraph()
        og.load_from_ontology(data)
        assert og.tree != None
        assert og.tree.name == 'Source'

        with open(ontology_file.replace('.json', '_tree.json'), 'w+') as f:
            json.dump(og.export(), f)

def test_load_from_json():
    for ontology_file in fixtures['json']:
        with open(ontology_file) as f:
            data = json.load(f)

        og = OntologyGraph()
        og.load_from_json(data)
        assert og.tree != None
        # assert og.tree.name == 'Source'
