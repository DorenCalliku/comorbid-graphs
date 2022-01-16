# Comorbid-Graphs
Side by side comparison of disorders based on comorbidity factors for clinical psychology.

1. create hierarchies of sources of information
2. extract valuable elements from text
3. visualize dependencies


## Simple Example 
Create from [sample file](big_picture.yaml):
```py
from comorbid_graphs import ComorbidGraph
my_graph = ComorbidGraph.from_yaml('big_picture.yaml')

print(my_graph.explore(maxlevel=4))
```


Results:  
```
Diagnosing Mental Health Issues
├── Frameworks
│   ├── DSM-V
│   │   ├── what
│   │   ├── where
│   │   │   ├── wikipedia
│   │   │   ├── website
│   │   │   └── manual
│   │   ├── who
│   │   │   └── APA
│   │   ├── elements
│   │   │   ├── disorder
│   │   │   ├── symptom
│   │   │   └── diagnostic guideline
│   │   └── mini versions
│   │       ├── Chinese Classification of Mental Disorders
│   │       │   └── wikipedia
│   │       └── Psychodynamic Diagnostic Manual
│   │           └── wikipedia
│   ├── ICD-10
│   │   ├── what
│   │   ├── where
│   │   │   ├── website
│   │   │   ├── manual
│   │   │   └── wikipedia
│   │   ├── who
│   │   │   └── WHO
│   │   └── elements
│   │       └── disorder
│   ├── HiTOP
│   │   ├── what
│   │   ├── where
│   │   │   ├── website
│   │   │   └── manual
│   │   └── elements
│   │       ├── spectra
│   │       ├── subfactor
│   │       ├── syndrome
│   │       ├── maladaptive trait
│   │       ├── symptoms
│   │       └── disorder
│   └── RDoC
│       ├── what
│       ├── where
│       │   ├── website
│       │   └── wikipedia
│       ├── who
│       │   └── nimh
│       └── elements
│           ├── genes
│           ├── molecules
│           ├── cells
│           ├── circuits
│           ├── physiology
│           ├── behaviors
│           ├── self-reports
│           └── paradigms
└── approaches
    ├── authoritative
    ├── psychodynamic
    ├── empirical
    └── network
```

## Additional Resources
- **[Short story long](https://github.com/DorenCalliku/comorbid-graphs/blob/main/docs/story.md)**: Why? What are the elements I am trying to study?  
- **[In-depth example](https://github.com/DorenCalliku/comorbid-graphs/blob/main/ReadMe.ipynb)**: Check in depth the tool in a notebook.   
- **[Examples & Resources](https://github.com/DorenCalliku/comorbid-graphs/tree/main/examples)**: Learn how to apply it to your problem through these use-cases.   
    - [Ontologies on Psychology](https://github.com/DorenCalliku/comorbid-graphs/tree/main/examples) showing different tools to be used when analysing psychological text.   
    - [DSM-V Exploration](https://github.com/DorenCalliku/comorbid-graphs/tree/main/examples) extraction from book, and analysis of usage of terms.  
    - [Forensic Neuroscience](https://github.com/DorenCalliku/comorbid-graphs/tree/main/examples/forensic_neuroscience) extraction of cases, and analysis of terms used.   
    - [Wikipedia Articles](https://github.com/DorenCalliku/comorbid-graphs/tree/main/examples) extract and analyse the well-known source of data.   
<br>

- **[Report issue](https://github.com/DorenCalliku/comorbid-graphs/issues)**: If something doesnt seem right.
- **[Applications](https://github.com/DorenCalliku/comorbid-graphs/blob/main/docs/applications.md)**: Who is using Comorbid-Graphs?   
- **[Readings](https://github.com/DorenCalliku/comorbid-graphs/blob/main/docs/notes.md)**: Interesting related articles or repositories.  


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