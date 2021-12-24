from comorbid_graphs.from_ontology.ontology_reader import OntologyReader
import json

def test_process():
    with open('tests/fixtures/symp.json') as f:
        data = json.load(f)
    oreader = OntologyReader(data)
    assert oreader.flattened_items != {}
    assert len(oreader.flattened_items) == 949
    # print([i for i in oreader.flattened_items.values()][:10])
