import json
from ontology_graphs import OntologyGraph


filter_nodes = {
    "HumanDO.json": {
        "annotations": [
            "disease of mental health",
            "nervous system disease",
        ],
        "example_text": [
            "disease of mental health",
        ],
    },
    "ND.json": {
        "annotations": [
            "pathological bodily process",
            "disease stage",
            "disorder",
            "neurological disease",
            "syndrome",
        ],
        "example_text": [
            "disease course",
            "diagnosis of syndrome",
            "diagnosis of disease",
            "diagnosis of disorder",
            "diagnostic guideline",
        ],
    },
    "symp.json": {
        "annotations": [
            "general symptom",
            "neurological and physiological symptom",
            "nervous system symptom",
            "head and neck symptom",
        ],
        "example_text": [],
    },
    "MD-core.json": {
        "annotations": [
            "mental disorder",
            "pathological mental process",
        ],
        "example_text": [],
    },
    "MF-core.json": {
        "annotations": [
            "bodily disposition",
            "interpersonal process",
            "mental process",
            "consciousness",
            "representation",
        ],
        "example_text": [
            "problem solving behavior",
        ],
    },
}


def save_json(json_data, filename):
    with open(filename, "w+") as f:
        json.dump(json_data, f)


def extract_file(file):

    ontology_name = file.replace("mental_health/ontologies/", "")
    with open(file) as f:
        json_data = json.load(f)
    
    # processing
    og = OntologyGraph()
    og.load_from_ontology(json_data)

    # pick the right nodes
    for dir, val in filter_nodes[ontology_name].items():
        for node_name in val:
            node = og.find_node(node_name, pos=-1)
            if node:
                new_name = file.replace(
                    "ontologies/" + ontology_name,
                    dir + "/" + node_name + "_" + ontology_name,
                )
                save_json(og.export_node(node), new_name)
                print(node_name)
            else:
                print("Node ", node_name, " was not found")


if __name__ == "__main__":
    for i in filter_nodes.keys():
        print(i)
        extract_file("mental_health/ontologies/" + i)
    print()