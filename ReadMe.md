---
jupyter:
  jupytext:
    formats: ipynb,md
    text_representation:
      extension: .md
      format_name: markdown
      format_version: '1.3'
      jupytext_version: 1.13.5
  kernelspec:
    display_name: Python 3 (ipykernel)
    language: python
    name: python3
---


# Comorbid-Graphs
Side by side comparison of disorders based on comorbidity factors for clinical psychology.

- create hierarchies of information
- analyse text for psychological terms
- visualize


**[Examples](https://github.com/DorenCalliku/comorbid-graphs/examples)**: Learn how to apply it to your problem through our use-cases.  
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
* [Short Story Long](https://github.com/DorenCalliku/comorbid-graphs/docs/story.md): What is this tool trying to archive?   
* [Ontologies](https://github.com/DorenCalliku/comorbid-graphs/docs/ontologies.md): Where do we get the terminology from?   
* [Data](https://github.com/DorenCalliku/comorbid-graphs/docs/data.md): How to load information?  

- [Applications](https://github.com/DorenCalliku/comorbid-graphs/docs/applications.md): Who is using Comorbid-Graphs?  
- [Readings](https://github.com/DorenCalliku/comorbid-graphs/docs/notes.md): Interesting related articles or repositories.  




## Getting Started

### Installation
You can install `comorbid-graph` in any `python` environment.

<!-- #region -->
```sh
!pip install git+https://github.com/DorenCalliku/comorbid-graphs
```
<!-- #endregion -->

## Comorbid-Graphs 101: Exploration of DSM-V
An example usage is the analysis of DSM-V.  
Create the **ComorbidGraph** from raw-json.  

```python tags=["hide-input"]
import json

# read a json file
filepath = 'examples/dsm_v/dsm_v.json'
with open(filepath) as f:
    data = json.load(f)
    
# create the comorbid graph
from comorbid_graphs import ComorbidGraph, ComorbidGraphNode
cg = ComorbidGraph(json_data=data, node_type=ComorbidGraphNode)
cg.print_head()
```

## Exploration
These are methods that might come handy during your work with ComorbidGraphs.   

Explore the whole hierarchy through `cg.explore()` or print just the top info `cg.print_head()`.

* **maxlevel**:  how deep in tree you want to go, print_head default = 3 
* **include_score**: shows on the side how much each result was evaluated, useful in search
* **top**: shows top X lines

```python
cg.print_head(maxlevel=3, top=10)
```

### Select
If you know the name of node that you are looking for, this will return it with all its children.

```python
results_cg = cg.select("Neurodevelopmental Disorders")
results_cg.print_head(maxlevel=2)
```

### Search
Finds the related nodes regarding specific terms. You can search multiple terms using `,` between terms.  
It iterates through the nodes, and scores them based on a simple function. After that returns only the included nodes ordered by *relevance*.  

* **select_from**: filter from a certain ancestor that you know
* **filter_type**: based on your preference, you might filter only sections
* **title**:    provide a meaningful title for you

**Warning**: Relevance score is **not** meaningful yet.

```python
# Example: 
results_cg = cg.search(
    "headache,migraine",
    select_from='caffeine',
    filter_type='default,section',
    title='Caffeine Solution',
)
results_cg.print_head()
```

### Advanced Search

As you can see from previous search, if you have a **high level of granularity** you might want to do some **filtering** so that you will get more meaningful results. For users who are using search a lot for specifics in a hierarchical graph. For a full guide and explanation check the page [advanced search](https://github.com/DorenCalliku/comorbid-graphs/docs/search.md) in the documentation.

#### Types of filters
- **inc**: include or filter-in 
- **exc**: exclude or filter-out

#### Element of filters
* **name** : find all the nodes that contain these words in their name/title
* **content** : find all the nodes that contain these words in the body - by default also the unassigned text.
* **type** : filter the nodes that have a type like this
* **text_longer** : filter the nodes with text longer than provided
* **parent** : if parent has name like this

#### Special Filter
* **ancestor** : Checks if any of the names of the ancestors in the tree is like pattern

```python
# Example: Which Disorders in 'DSM-V' contain the term 'depressive disorder'?
# (but I am not interested in neurodevelopmental disorders, and skip small docs too - 
# say skip disorders smaller than 100 characters of text)

query_string = """
depressive disorder
inc_name:        depress,diagnostic criteria
exc_ancestor:    neurodevelopmental
inc_text_longer: 100
"""
# cg.get_query(query_string)
```

```python
results_cg = cg.advanced_search(query_string)
results_cg.print_head()
```

### Save for Later

```python
with open('search_results.json', 'w+') as f:
    json.dump(results_cg.export(), f)
```

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
