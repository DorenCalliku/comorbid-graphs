
# Comorbid-Graphs
Create a mental map of resources using hierarchical trees.

**[Examples](./examples)**: Learn how to apply it to your problem through our use-cases.  
**[Report issue](https://github.com/DorenCalliku/comorbid-graphs/issues)**: If something doesnt seem right.

### Table of Contents
* [Intro](#intro)
* [Getting Started](#getting-started)
    - [Installation](#installation)
    - [Comorbid-Graphs 101](#comorbid-graphs-101)
* [Usage](#usage)
    - [Explore](#explore)
    - [Select](#select)
    - [Search](#search)
    - [Advanced Search](#advanced-search)
    - [Stats](#stats)
    - [Process](#analytics)
    - [Compare](#compare)
* [References](#references)

## Intro
* [Short Story Long](./docs/story.md): Why create this tool and who should use it.  
* [Ontologies](./docs/ontologies.md): Why use ontologies, and how?   
* [Data](./docs/data.md): How to load information?  

- [Applications](./docs/applications.md): Who is using Comorbid-Graphs?  
- [Readings](./docs/notes.md): Interesting related articles or repositories.  

## Getting Started

### Installation
`!pip install git+https://github.com/DorenCalliku/comorbid-graphs`

### Comorbid-Graphs 101
For this example you can use also one of [example data files](https://github.com/DorenCalliku/comorbid-graphs/examples/data) in the docs.   
Suggested methods to be developed can be found [here](./docs/data.md), and some of them are implemented in the [examples](./examples).   
```python
# create on the go
import json
with open('example_data_file.json') as f:
    data = json.load(f)
```

Create the **CG**:  
```python
from comorbid_graphs import ComorbidGraph, ComorbidGraphNode
cg = ComorbidGraph(json_data=data, node_type=ComorbidGraphNode)
print(cg.explore())
``` 

Saving for later:  
```python
import json
with open('exported_data.json', 'w+') as f:
    json.dump(cg.export(), f)
```


## Usage
These are methods that might come handy during your work with ComorbidGraphs.

### Explore
Explore the whole hierarchy.   
```python
# explore all
cg.explore()
```

Or explore only the top nodes.  
```python
# explore only the first 3 levels of the tree
cg.explore(maxlevel=3)
```
### Search
If you know the name of node that you are looking for, this will return it with all its dependencies.
```python
results_cg = cg.select("parent")
results_cg.explore()
```

### Search
Finds the related nodes regarding specific terms. It iterates through the nodes, and scores them based on a simple function.
After that returns only the included nodes ordered by relevance. (for now only default behaviors are allowed)
```python
# Example: Which graph nodes are related to depressive disorders?
results_cg = cg.simple_search("depressive disorder")
results_cg.explore()
```

You can search multiple terms using `,` between terms.
```python
# Example: What are the nodes that are related to pain or ache?
results_cg = cg.simple_search("pain,ache")
results_cg.explore()
```


### Advanced Search
For users who are looking for specifics in a hierarchical graph.  
For a full guide and explanation check the page [advanced search](./docs/search.md) in the documentation.

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

### Process
For now we are using a bag-of-words method for extracting cross references.

```python
# previously loaded comorbid graphs
ontologies = [ontology1, ontology2]

# extract all related labels (cross-referencing)
cg.process_graph(ontologies)
```

### Compare


## References
This package can be thought as a thin wrapper to [Anytree](https://anytree.readthedocs.io/en/latest/index.html), with some useful functionalities for use-case of ontologies and text-processing.   

* Applications using this tool
    - [Garden-of-Graphs](http://garden-of-graphs.herokuapp.com/) - latest version usage  
    - [DiseasePainter](https://diseasepainter.herokuapp.com/) - first version usage
* Libraries I am using
    - [Pandas](https://pandas.pydata.org/docs/reference/index.html#api) - for bulk analysis
    - [Spacy](https://spacy.io/) - future usage
* Similar packages
    * KGlab - [docs](https://derwen.ai/docs/kgl/), [code](https://github.com/DerwenAI/kglab) 
    * OntoBio's [OntolFactory](https://github.com/biolink/ontobio/blob/master/ontobio/ontol_factory.py) - [docs](https://ontobio.readthedocs.io/en/latest/), [sample notebook on wikidata](https://nbviewer.org/github/biolink/ontobio/blob/master/notebooks/Wikidata_Ontology.ipynb) - [interesting](https://nbviewer.org/github/biolink/ontobio/blob/master/notebooks/output/anxiety-disorder.png)
    * Ontospy - visualize ontologies - [code](https://github.com/lambdamusic/Ontospy)  
    * PyTextRank - [ppt](https://derwen.ai/s/kcgh#106), [code](https://github.com/DerwenAI/pytextrank)
