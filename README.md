# Comorbid-Graphs
A tool for making it easier to compare information using KnowledgeGraphs in neuro-psychology.   
Based on `anytree` (for tree structures) and `networkx` (for graphs).  

Part of the Comorbid project.
> **Warning**: This project is EXPERIMENTAL. There is **NO-VALIDATION** yet, and some data might be **LOST** in processing.   
> **DONT USE IN PRODUCTION**.

<br>

### Table of Contents
* [Getting Started](#getting-started)
    - [ComorbidGraphs-101](#comorbidgraphs-101)
    - [Installation and Setup](#installation-and-setup)
    - [Load from Ontology](docs/ontologies.md)
* [Examples](#examples)
    - [Compare Wikipedia articles on DSM-V disorders?](./examples/Wikipedia.ipynb)
    - [Compare DSM-V disorders on symptoms found?](./examples/DSM-V-Symptom.ipynb)
* [Usage](#usage)
    - [Explore](#explore)
    - [Search](#search)
    - [Advanced Search](#advanced-search)
    - [Stacking](#stacking)
    - [Stats](#stats)
* [Insights](#insights)
* [References](#references)
    - [Software](#software)
    - [Readings](docs/notes.md)
<br><br>

## Getting Started

### ComorbidGraphs 101

For this example you can use one of [data files](https://github.com/DorenCalliku/comorbid-graphs/examples/data) in the docs.

```python
# import libraries needed
import json
from comorbid_graphs import ComorbidGraph, ComorbidGraphNode

with open('example.json') as f:
    data = json.load(f)

# load data - expects a hierarchical tree of the form
# {"name": "Default", "children":[{"name": "Default Child", "children":[]}]}
cg = ComorbidGraph(json_data=data, node_type=ComorbidGraphNode)
```

### Installation and Setup

```bash
pip install git+https://github.com/DorenCalliku/comorbid-graphs
```

## Usage

### Explore

```python
cg.pretty_print_tree()
```

### Search

```python
results = cg.search("depressive disorders")
results.pretty_print_tree()
```


### Advanced Search
Besides the basics, there are some more geeky usages possible for people not searching for only a general picture.
This is the Zoom-In feature which can bring specific results.   
For a full guide and explanation check the page [search](docs/search.md) in the documentation.

```python
# Search in 'DSM-V', but exclude all the stuff in 'NeuroDevelopmental Disorders' subgraph
# for documents containing phrases like 'anxiety', and 'Disorder' in titles
# also, the text should be better than 300 chars.
# Dont return stuff that match partially.

results = cg.advanced_search("""
anxiety

inc_parent:DSM-V
inc_title:Disorder
inc_text_longer:300

exc_ancestor:Neurodevelopmental Disorders
""", full_match=True)

results.pretty_print_tree()
```

#### Stacking

You can stack results together.

```python
# What is the extent of depression in DSM-V? Include all of the depressive disorders.

results = cg.advanced_search("""
depressive, depression, low mood
inc_type:document
inc_ancestor:DSM-V
exc_ancestor:Depressive Disorders

MERGE

inc_type:document
inc_ancestor:Depressive Disorders
""", full_match=True)

results.pretty_print_tree()
```

### Stats

```python
cg.stats()
```


## Insights


## References


### Software
- [Anytree](https://anytree.readthedocs.io/en/latest/index.html)
- [Networkx](https://networkx.org/)
