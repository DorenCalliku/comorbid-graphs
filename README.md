# ontology-graphs
Turning owl files to json for application purposes.

> **Warning: tree, not a graph**: For simplification purposes, I am turning these into trees. Check `anytree_mixin.py`.

## Usage

### Load from ontology of owl.
1. Download `owl2vowl`   

downloadable here: http://vowl.visualdataweb.org/webvowl.html


2. Create a script for extraction from online source.
```
# extract_from_web.sh

owl_url_1="https://example.com/owl_url_1.json"
owl_url_2="https://example.com/owl_url_2.json"

for i in $owl_url_1 $owl_url_2
do
    java -jar $owl_location -iri $i
done
```

3. Turn to Graph json.
```
# mycode.py

from ontology_graph import OntologyGraph
og = OntologyGraph()
og.load_from_ontology('tests/fixtures/owl_url_1.json')
og.pretty_print_tree()
```