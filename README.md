# Comorbid-Graphs
Create a mental map of resources.  
A *batteries-included easy-to-use tool* for <ins>search, compare, analyse and visualize</ins> hierarchically-oriented text-resources (mainly on neuro-psychology).   

Read how this started: [Story](./docs/story.md).  
Used by: [ComorbidLab]().   
Previous apps: [Garden-of-Graphs](http://garden-of-graphs.herokuapp.com/), [DiseasePainter](https://diseasepainter.herokuapp.com/).

> **Warning**: Under heavy development. Please [report bug]() if something doesnt work.
<br>

### Table of Contents
* [Getting Started](#getting-started)
    - [Why a new tool](#why-a-new-tool)
    - [Installation](#installation)
    - [Comorbid-Graphs 101](#comorbid-graphs-101)
* [Usage](#usage)
    - [Explore](#explore)
    - [Search](#search)
    - [Advanced Search](#advanced-search)
    - [Stats](#stats)
    - [Language Processing](#analytics)
    - [Compare](#compare)
* [Examples](#examples)
    - [Load from Ontology](./examples/Ontologies.md)
    - [DSM-V Exploration (Book-to-CG)](./examples/DSM-V.ipynb)
    - [Wikipedia Categories](./examples/Wikipedia.ipynb)
    - [CourtListener Cases](./examples/CourtListener.ipynb)
    - [Case Transcript Analysis](./examples/Case-Analysis.ipynb)
* [References](#references)
    - [Libraries](#libraries)
    - [Other options](#other-options)
    - [Contribute](#contribute)
<br><br>

## Getting Started

### Why a new tool

This tool is here to help with:  
- *Informed decision making* on direction of research.
- *Mental Knowledge Graph* to understand where is your contribution and how that impacts.
- *Maintaining dependencies* of information.

For whom?
- *mentors* for showing students where they can contribute
- *academicians* doing meta-review, but want a quick-tool before going all-in for an ontology.

Existential problem this tool?
- Is this a *comorbid* tool - which seems like its solving problems but actually adding more confusion?
- Aim: Reduce self's *comorbidity* level.

What this tool is **not**?
- Ontology-Viewer - we simplify ontologies into hierarchical structures. Check [Other options](#other-options).
- Knowledge-Graph automatic creator.

### Installation

Setup: For using `Comorbid-Graphs` you need [python]() installed in your computer.  
Together with `python` comes the `pip` installer for installing this package.  
For installing python and jupyter and more, you can follow [this guide](). 

Then write in your terminal or jupyter notebook:  
`!pip install git+https://github.com/DorenCalliku/comorbid-graphs`

### Comorbid-Graphs 101

For this example you can use one of [data files](https://github.com/DorenCalliku/comorbid-graphs/examples/data) in the docs.

#### Loading from file
```python
# import libraries needed
import json
from comorbid_graphs import ComorbidGraph, ComorbidGraphNode

with open('example.json') as f:
    data = json.load(f)
# example: data = {"name": "Default", "children":[{"name": "Default Child", "children":[]}]}

cg = ComorbidGraph(json_data=data, node_type=ComorbidGraphNode)
cg.explore()
```

#### Saving for later

```python
with open('exported_data.json', 'w+') as f:
    json.dump(cg.export(), f)
```


## Usage

### Explore
Prints in an organized way the tree-version of the information. 
```python
# explore all
cg.explore()

# explore only the first 3 levels of the tree
cg.explore(maxlevel=3)
```

### Search
Finds the related nodes regarding specific terms. It iterates through the nodes, and scores them based on a simple function.
After that returns only the included nodes ordered by relevance. (for now only default behaviors are allowed)
```python
# Example: Which graph nodes are related to depressive disorders?
results_cg = cg.simple_search("depressive disorder")
results_cg.explore()

# Example: What are the nodes that are related to pain or ache?
results_cg = cg.simple_search("pain,ache")
results_cg.explore()
```


### Advanced Search
For users who are looking for specifics in a hierarchical graph.  
For a full guide and explanation check the page [search](docs/search.md) in the documentation.

```python
# Example: Which Disorders in 'DSM-V' contain the term anxiety?
# (but I am not interested in neurodevelopmental disorder, and skip small docs too - say smaller than 100 characters of text)

query_string = """anxiety
inc_name:Disorder
inc_text_longer:100
inc_ancestor:DSM-V
exc_ancestor:neurodevelopmental disorder
"""
results_cg = cg.advanced_search(query_str, node_type=ComorbidGraphNode)
results_cg.explore()
```

### Stats

### Language Processing

### Compare

## Examples
Here you can find notebooks of analysis. They are found under the [examples](./examples) folder.

- [Load from Ontology](./examples/Ontologies.md)
- [Wikipedia Categories](./examples/Wikipedia.ipynb)
- [DSM-V Exploration](./examples/DSM-V-Symptom.ipynb)
- [CourtListener Cases](./examples/CourtListener.ipynb)
- [Case Transcript Analysis](./examples/Case-Analysis.ipynb)

For a web-application and ease of usage you can check [ComorbidLab]().

## References

### Libraries
These are libraries that I am using for the project.  
- [Anytree](https://anytree.readthedocs.io/en/latest/index.html)
- [Spacy](https://spacy.io/)

### Other options
If you are looking for something like `Comorbid-Graphs`, but in a different taste - check these other options.  
Most of them are more mature than `Comorbid-Graphs` and probably can help you out with more validatable results.  

* Knowledge-Graphs/Ontologies
    * KGlab - [docs](https://derwen.ai/docs/kgl/), [code](https://github.com/DerwenAI/kglab) 
    * OntoBio's [OntolFactory](https://github.com/biolink/ontobio/blob/master/ontobio/ontol_factory.py) - [docs](https://ontobio.readthedocs.io/en/latest/), [sample notebook on wikidata](https://nbviewer.org/github/biolink/ontobio/blob/master/notebooks/Wikidata_Ontology.ipynb) - [interesting](https://nbviewer.org/github/biolink/ontobio/blob/master/notebooks/output/anxiety-disorder.png)
    * Ontospy - visualize ontologies - [code](https://github.com/lambdamusic/Ontospy)  
* Text Processing
    * Spacy - [docs](https://spacy.io/)
    * PyTextRank - [ppt](https://derwen.ai/s/kcgh#106), [code](https://github.com/DerwenAI/pytextrank)


Check also the [notes](./docs/notes.md) for text processing and knowledge graph creation useful resources I have found during the exploration of the topic. Maybe you find something useful there.  

### Contribute
You find the project interesting and want to expand it for your usage and others? [Contact me through twitter](https://twitter.com/dcalliku)
