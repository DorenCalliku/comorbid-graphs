#!/bin/bash
cd tests/fixtures

# define owl2vowl location
# downloadable here: http://vowl.visualdataweb.org/webvowl.html
owl_location='../../../owl2vowl.jar'

# set owl file urls
symptoms_owl="https://raw.githubusercontent.com/DiseaseOntology/SymptomOntology/main/symp.owl"


for i in $symptoms_owl
do
    java -jar $owl_location -iri $i
done
