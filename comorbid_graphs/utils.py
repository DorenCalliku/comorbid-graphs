import json
from . import ComorbidGraph, ComorbidGraphNode


def generate_test_data(data_file, analysis_files=[]):
    with open(data_file) as f:
        data = json.load(f)
    cg = ComorbidGraph(
        data, node_type=ComorbidGraphNode, assign_ids=True, root_name="dsm-v"
    )
    # analyse
    analysis_cgs = []
    for file in analysis_files:
        with open(file) as f:
            data = json.load(f)
        name = file[file.rfind("/") + 1 :].replace(".json", "")
        analysis_cgs.append(
            ComorbidGraph(
                data, node_type=ComorbidGraphNode, assign_ids=True, root_name=name
            )
        )
    print(f"Analysing with {len(analysis_cgs)} analysis graphs.")
    cg.process_graph(analysis_cgs)
    with open(data_file.replace(".json", "_labelled.json"), "w+") as f:
        json.dump(cg.export(), f)
    return cg


def open_existing_data(data_file):
    with open(data_file.replace(".json", "_labelled.json")) as f:
        data = json.load(f)
    return ComorbidGraph(
        data, node_type=ComorbidGraphNode, assign_ids=True, root_name="dsm-v"
    )
