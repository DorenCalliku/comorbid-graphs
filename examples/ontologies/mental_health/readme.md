# Mental Health Issues

Helping people with mental health issues is a difficult problem because of the many factors affecting the <b>subject</b>. To help with this issue there have been many endeavours to <u>organize our knowledge</u> and <u>make it available</u> for use from the <b>practician</b> (psychologist, psychiatrist, neurologist, neuro-psychologist, therapist). Still we do not have open-source tools which have reproducible results with a clear usage.  

When building this tool, I tried to keep in mind the needs that it needs to fulfill.  
<b>Annotations</b>   
* annotate transcripts with disorder and symptom info
* connect references to annotated transcripts  
* provide keyword - get related disorders/symptoms

<b>Solutions</b>   
* provide symptoms - get disorders   
* provide disorder - get diagnosis
* provide disorder - get therapy   

<b>Visualizations</b>   
* step-by-step diagnosis
* visualize disorders tree for comprehensive view

<b>Analysis</b>   
* compare diseases for shared symptoms
* group based on disease description

## Knowledge Trees
A knowledge-tree is a tree structure of information organized in the form `parent-child` that I have seen it as easy to use to understand hierarchical knowledge. Eventually this (hopefully-your opinion) helped with the visualization, in giving a sense of depth of information. The code was based on [anytree](https://anytree.readthedocs.io/en/latest/index.html) - a `python library` for dealing with trees. Kudos to its writer!  


| tree | code | result |
| ---- | ---- | ------ |
|      |      |        |
```
{
    "id": 1,
    "name": "profile",
    "children": [
        {
            "id": 2,
            "name": "document",
            "children": []
        }
    ]
}
```

### Knowledge Trees from Ontologies

<b> Ontologies </b>  
One well-defined and expandable way of structuring knowledge are ontologies. They are structured nets/graphs of nodes of information where everything is well defined. According to my (non-exhaustive) search, these are the ontologies available for use when it comes to neuro-psychology:

* [Human Diseases Ontology](https://github.com/DiseaseOntology/HumanDiseaseOntology) and [webpage](https://disease-ontology.org/)
* [Neurological Disease Ontology](https://github.com/addiehl/neurological-disease-ontology) and [paper](https://github.com/addiehl/neurological-disease-ontology/blob/master/docs/ICBO2012_Paper.pdf)
* [Mental Functioning Ontology](https://github.com/jannahastings/mental-functioning-ontology) and [paper](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6186823/)

<b>Turning to Knowledge Tree</b>  
As these ontologies are expressed in `owl` or `obo` format, I didnt find any easy tools to use them in a visual/practical way. After skimming through their structures I decided to use another more <b>simplified (and dumbified)</b> version of them: turning them to `json` and using them as knowledge trees.   

To do this, I did the following:   
* [OWL2VOWL](https://github.com/VisualDataWeb/OWL2VOWL) and [website](http://vowl.visualdataweb.org/), [download here](http://vowl.visualdataweb.org/webvowl.html): turn `owl` to `json`  
* [Notebooks of Python Scripts](): to organize and clean the `json` files, expand them with more information

Known Limitations:  
* first parent of children is set as only parent, dummy example: `violence` is a `[mental health, neurological disease]` symptom, but only `mental health` was used.
* ids are not maintained, or changed as some of them contradict each other.

### Knowledge Trees from DSM-V
<b> DSM-V </b>    
I did not find any online good version of the `DSM-V` except the `pdf` version of the book.   
The downloaded `pdf` can be found [here](dsm_v/raw/DSM_V.pdf). 

<b> Turning to Knowledge Tree </b>   
As this was the case, then I decided to process the book and turn it into a `knowledge-tree`. After skimming and understanding the structure I extracted the diseases with `Diagnosis Criteria` as they were the ones that were well defined. Still, I kept a [table of contents](dsm_v/raw/toc.yaml) (built mainly by my friend - Hilal) for reference and comparison. The processing `DSM-V` is found [here](). 

## Annotations


## Validation

## Results
<b> Transcripts </b>

<br><br><br>

## Further Readings
* [Psychological Text Analysis in the Digital Humanities](https://www.researchgate.net/publication/313523262_Psychological_Text_Analysis_in_the_Digital_Humanities)
* [Clinical Text Mining](https://link.springer.com/content/pdf/10.1007%2F978-3-319-78503-5.pdf)
* [An advanced review on Text Mining in Medicine](https://www.researchgate.net/publication/329948994_An_advanced_review_on_Text_Mining_in_Medicine)
* [Text mining and item response theory for psychiatric and psychological assessment](https://www.apadivisions.org/division-5/publications/score/2018/01/text-mining)
* [PsyGeNet: Text mining and expert curation to develop a database on psychiatric diseases and their genes](http://www.psygenet.org/web/PsyGeNET/menu/downloads) and [webpage](http://www.psygenet.org/web/PsyGeNET/menu/home)
