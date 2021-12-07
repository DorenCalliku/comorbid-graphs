import pprint
from .config import MAIN_FIELDS, KNOWN_ANNOTATIONS


class OntologyReader:
    """Takes file_name.json after doing: java -jar owl2vowl.jar -file file_name.owl.
    Creates a list of objects with solved parents."""

    def __init__(self, json_data):
        self.unprocessed_items = json_data['classAttribute']
        self.annotations = self.clean_annotations(KNOWN_ANNOTATIONS)

        # extract everything
        self.flattened_items = {}
        self.extract()

    def get_flattened(self):
        """The resulting flattened items tree that we are looking for
        TODO: check if this is really necessary for processing"""

        return self.flattened_items

    def extract(self):
        # use recursion to extract superClasses
        for each in self.unprocessed_items:
            self.preprocess_item(each["id"])

        # remove stuff that dont have a name
        keys = []
        for i, val in self.flattened_items.items():
            if "name" not in val:
                keys.append(i)
        for i in keys:
            del self.flattened_items[i]

    def preprocess_item(self, item_id):
        """
        Extracts the items from JSON representation of OWL
        and flattens them to a dictionary. I wanted the information
        in OWL in a simpler view and here is where I do the 'magic'.

        returns: None"""

        # find the item, and check if it is processed
        # basic step of recursion
        item = self.find_in_list(self.unprocessed_items, item_id)
        if item["id"] in self.flattened_items.keys():
            return
        # otherwise process yourself
        this_item = {}
        for label in MAIN_FIELDS:
            # if something missing, add None, skip (keeping in mind potential SQL)
            if label not in item:
                this_item[label] = None
                continue
            if label == "label":
                try:
                    # provide name
                    labels = [i for i in item["label"].keys()]
                    if 'IRI-based' in labels:
                        labels.remove("IRI-based")
                    name_label = labels[0] if len(labels) else "IRI-based"
                    this_item["name"] = item["label"][name_label]
                except Exception as e:
                    print("Warning: Error in processing.", e)
                    this_item["name"] = item["iri"]
                for each in item["label"].keys():
                    this_item["label_" + each] = item["label"][each]
            elif label == 'annotations' and 'annotations' in item:
                item_annotations = {}
                for k, j in item[label].items():
                    if k in self.annotations.keys():
                        item_annotations[self.annotations[k]] = j
                    else:
                        item_annotations[k] = j
                    
                this_item[label] = item_annotations
            else:
                this_item[label] = item[label]
            if "name" not in this_item.keys():
                this_item[label] = item["id"]
        self.flattened_items[item_id] = this_item
        if "superClasses" in item:
            for i in item["superClasses"]:
                self.preprocess_item(i)

    def clean_annotations(self, known_annotations, print_ann=False):
        """
        Manual work extracting the necessary annotations needed
        for the work with the files. Open the JSON file to understand.
        You need this to append different properties given from the annotations.

        returns: annotations
                 which is a dictionary with default values
                 that you can update based on your need.
        """
        annotations = self.get_annotations_json_items()
        for key in annotations.keys():
            if key in known_annotations:
                annotations[key] = known_annotations[key]
        if print_ann:
            print("\nThese are the dictionary of your annotations.")
            pprint.pprint(annotations)
        return annotations

    def get_annotations_json_items(self):
        """TODO: this makes unprocessed_items necessary when it shouldnt be"""
        vals = []
        for i in self.unprocessed_items:
            if "annotations" in i:
                for j in i["annotations"]:
                    vals.append(j)
        annotations = {}
        for i in set(vals):
            annotations[i] = i
        return annotations

    @staticmethod
    def find_in_list(data_in_list, item_id):
        for i in data_in_list:
            if i["id"] == item_id:
                return i
