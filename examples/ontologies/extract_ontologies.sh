#!/bin/bash
cd examples/mental_health/ontologies

# define owl2vowl location
# downloadable here: http://vowl.visualdataweb.org/webvowl.html
owl_location='../../../../owl2vowl.jar'

# set owl file urls
human_doid_owl="https://raw.githubusercontent.com/DiseaseOntology/HumanDiseaseOntology/main/src/ontology/HumanDO.owl"
doid_owl="https://raw.githubusercontent.com/DiseaseOntology/HumanDiseaseOntology/main/src/ontology/doid.owl"
neurological_disease_owl="https://raw.githubusercontent.com/addiehl/neurological-disease-ontology/master/src/ontology/ND.owl"
mf_disorder_owl="https://raw.githubusercontent.com/jannahastings/mental-functioning-ontology/master/ontology/internal/MD-core.owl"
mf_cognitive_owl="https://raw.githubusercontent.com/jannahastings/mental-functioning-ontology/master/ontology/internal/MF-core.owl"
symptoms_owl="https://raw.githubusercontent.com/DiseaseOntology/SymptomOntology/main/symp.owl"


for i in $neurological_disease_owl # $doid_owl $symptoms_owl $human_doid_owl $mf_disorder_owl $mf_cognitive_owl 
do
    java -jar $owl_location -iri $i
done
