from ontology_graphs.ontology_reader import OntologyReader

def test_process():
    oreader = OntologyReader(
        'tests/fixtures/symp.json'
    )
    assert oreader.flattened_items != {}
    assert len(oreader.flattened_items) == 949
    # print([i for i in oreader.flattened_items.values()][:10])
