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
import pprint
from ontology_graphs import OntologyGraph

og = OntologyGraph()
og.load_from_ontology('tests/fixtures/owl_url_1.json')

pprint.pprint(og.pretty_print_tree())
```

### Load from AnyTree json
```
>>> import json
>>> import pprint
>>> from ontology_graphs import OntologyGraph
>>> with open('tests/fixtures/symp_tree.json') as f:
...        json_data = json.load(f)
... 
>>> og = OntologyGraph()
>>> og.load_from_json(json_data)
>>> pprint.pprint(og.pretty_print_tree(max_level=4))
('Source\n'
 '├── symptom\n'
 '│   ├── urinary system symptom\n'
 '│   │   ├── urinary incontinence\n'
 '│   │   ├── renal abscess\n'
 '│   │   ├── genitourinary hemorrhage\n'
 '│   │   └── renal alteration\n'
 '│   ├── general symptom\n'
 '│   │   ├── hallucination\n'
 '│   │   ├── chills\n'
 '|   |   |   ... more\n'
 '│   │   └── asthenia\n'
 '│   ├── respiratory system and chest symptom\n'
 '│   │   ├── respiratory abnormality\n'
 '│   │   ├── cough\n'
 '|   |   |   ... more\n'
 '│   │   └── bronchiolitis\n'
 '│   ├── neurological and physiological symptom\n'
 '│   │   ├── alteration of consciousness\n'
 '|   |   |   ... more\n'
 '│   │   └── proprioception symptom\n'
 '│   ├── musculoskeletal system symptom\n'
 '│   │   ├── torticollis\n'
 '│   │   ├── abnormal posture\n'
 '|   |   |   ... more\n'
 '│   │   └── decreased jaw tone\n'
 '│   ├── nervous system symptom\n'
 '│   │   ├── coordination symptom\n'
 '|   |    |   ... more\n'
 '│   │   └── floppy head\n'
 '│   ├── abdominal symptom\n'
 '│   │   ├── abdominal rigidity\n'
 '|   |   |   ... more\n'
 '│   │   └── pelvic symptom\n'
 '│   ├── head and neck symptom\n'
 '│   │   ├── head symptom\n'
 '│   │   ├── throat symptom\n'
 '│   │   └── neck symptom\n'
 '│   ├── skin and integumentary tissue symptom\n'
 '│   │   ├── rash\n'
 '│   │   ├── skin lesion\n'
 '|   |   |   ... more\n'
 '│   │   └── eczema\n'
 '│   ├── hemic and immune system symptom\n'
 '│   │   ├── immune system symptom\n'
 '│   │   ├── hemic system symptom\n'
 '│   │   └── hematopoietic system symptom\n'
 '│   ├── digestive system symptom\n'
 '│   │   ├── rectorrhagia\n'
 '│   │   ├── tenesmus\n'
 '|   |   |   ... more\n'
 '│   │   └── belching\n'
 '│   ├── cardiovascular system symptom\n'
 '│   │   ├── palpitation\n'
 '│   │   ├── hemorrhage\n'
 '|   |   |   ... more\n'
 '│   │   └── heart failure\n'
 '│   ├── nutrition, metabolism, and development symptom\n'
 '│   │   ├── lack of expected normal physiological development in childhood\n'
 '│   │   ├── polydipsia\n'
 '│   │   ├── weight loss\n'
 '|       |   ... more\n'
 '│   │   └── decreased milk production\n'
 '│   └── reproductive system symptom\n'
 '│       ├── miscarriage\n'
 '│       ├── abortion\n'
 '|       |   ... more\n'
 '│       └── epididymitis\n'
 '├── obsolete appendicitis\n'
 '|   ... more '
 '├── acute respiratory distress\n'
 '└── excess pericardial fluid\n')
>>> 
```
