# Comorbid-Graphs
A tool for visualizing and analysing hierarchical information without losing dependencies.     
Part of the [Comorbid]() project, studying volume of text-data on neuro-psychology to understand comorbidity of disorders.  


> **Warning**: Under heavy development.
<br>

### Table of Contents
* [Getting Started](#getting-started)
    - [ComorbidGraphs-101](#comorbidgraphs-101)
    - [Installation and Setup](#installation-and-setup)
* [Usage](#usage)
    - [Explore](#explore)
    - [Search](#search)
    - [Advanced Search](#advanced-search)
* [Loading Data](#loading-data)
    - [Create it yourself](docs/ontologies.md)
    - [Load from Ontology](docs/ontologies.md)
    - [Load from Wiki](docs/ontologies.md)
* [Examples](#examples)
    - [Wikipedia Categories](./examples/Wikipedia.ipynb)
    - [DSM-V Exploration](./examples/DSM-V-Symptom.ipynb)
    - [CourtListener Cases](./examples/DSM-V-Symptom.ipynb)
    - [Transcript Analysis](./examples/DSM-V-Symptom.ipynb)
* [References](#references)
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
# example: data = {"name": "Default", "children":[{"name": "Default Child", "children":[]}]}

cg = ComorbidGraph(json_data=data, node_type=ComorbidGraphNode)
```

### Installation and Setup

```bash
pip install git+https://github.com/DorenCalliku/comorbid-graphs
```

## Usage

### Explore

```python
cg.explore()
```

### Search

```python
# EXAMPLE QUESTION
# Which documents are related to depressive disorders?

results_cg = cg.simple_search("depressive disorders")
results_cg.explore()
```


### Advanced Search
Besides the basics, there are some more geeky usages possible for people not searching for only a general picture.
This is the Zoom-In feature which can bring specific results.   
For a full guide and explanation check the page [search](docs/search.md) in the documentation.

```python
# EXAMPLE QUESTION
# Which Disorders in 'DSM-V' contain the term anxiety?
# (but exclude all the stuff in 'NeuroDevelopmental Disorders'
# - I am not interested in those, and skip small docs)

query_string = """
anxiety
inc_name:Disorder
inc_text_longer:300
inc_ancestor:DSM-V
exc_ancestor:Neurodevelopmental Disorders
"""
results_cg = cg.advanced_search(query_str, node_type=ComorbidGraphNode)
results_cg.explore()
```

## Loading Data

### Create it yourself

### Load from Ontology


### Load from Wiki
## References
- [Anytree](https://anytree.readthedocs.io/en/latest/index.html)
- [Suggested Readings](docs/notes.md)
