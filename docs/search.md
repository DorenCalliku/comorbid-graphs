# Search

The main functionality that I am trying to give to this package is to have a good search in an intuitive way.
This way people will be able to reach the information they want, without having to use SPARQL (that I havent learned yet ... shameee!).
 
* [Basics](#basics)
* [Levels of Search](#levels-of-search)
    * [Subgraphs](#subgraphs)
    * [Filtering](#filtering)
    * [Content](#content)


## Basics

A search is based on `{DIRECTION}_{FILTER}` for making things easier for people to use.

| DIRECTION | Meaning               | Example                                    |
| --------- | --------------------- | ------------------------------------------ |
| inc       | include or filter-in  | `inc_parent:DSM-V`                         |
| exc       | exclude or filter-out | `exc_name: Disorder` exclude all disorders |
| include   | include or filter-in  | `include_parent:DSM-V`                     |
| exclude   | exclude or filter-out | `exclude_title:Disorder`                   |

> **Info: inc and exc**: If a graph is included and excluded, it will be excluded in the end.  

<br>

| FILTER      | Filter inc/                                  | Expects | Strict Match | Example                          | Sorting Order                         |
| ----------- | -------------------------------------------- | ------- | ------------ | -------------------------------- | ------------------------------------- |
| name        | if graph has name/title                      | string  | False        | `inc_name: Disorder`             | `+ 100` per subgraph containing       |
| phrase      | these words are in the body                  | string  | True         | `exc_phrase:developmental`       | `+ 10` per time found in any subgraph |
| type        | if node has type like this                   | string  | True         | `inc_type:section`               | `NaN`                                 |
| text_longer | filter the nodes with text longer than count | int     | True         | `inc_text_longer:300`            | `NaN`                                 |
| ancestor    | if one of ancestors has a name like this     | string  | False        | `inc_ancestor: Phobic`           | `NaN`                                 |
| parent      | if parent has name like this                 | string  | False        | `inc_parent: Neurodevelopmental` | `NaN`                                 |

> **Info: Strict match**: Means if we are checking with `==` or with `contains`.  

> **Warning: parent vs ancestor**: If you write `inc_parent`, this will override `inc_ancestor`

<br>


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

## Levels of Search
To be able to integrate with DBs and similars, I am separating the search functionality.

### Subgraph 
SubGraph Cutting:  `Ancestors` & `Parents`

### Filtering
Node Structure Filtering: Name, Type, Body-Length

### Content
Content Filtering checks if a word is the document we are looking for.


## Ordering: PageRank
Will be useful later when increasing in complexity of information.

