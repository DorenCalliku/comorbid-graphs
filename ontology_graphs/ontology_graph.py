from anytree import Node, PreOrderIter
from .ontology_reader import OntologyReader
from .tree_mixin import AnyTreeMixin


class OntologyGraph(AnyTreeMixin):

    def __init__(self):
        self.tree = None

    def load_from_ontology(self, filename, name="Source", id=1):
        """Takes a dictionary of preprocessed from OntologyReader,
        and creates an AnyTree from that for easy processing."""

        oreader = OntologyReader(filename)
        self.flattened_items = oreader.get_flattened()
        del oreader

        self.lookup_table = {}

        self.tree = Node(name, id=id)
        for val in self.flattened_items.values():
            self.add_to_tree(val)

    def add_to_tree(self, item):
        # basic step of recursion
        if item["id"] in self.lookup_table:
            return

        if "superClasses" not in item:
            item["superClasses"] = []

        # if no superclasses, then add to source
        if item["superClasses"] is None or item["superClasses"] == []:
            node = Node(item["name"], parent=self.tree)
            self.lookup_table[item["id"]] = node
            return

        # else, check first the superclasses
        for i in item["superClasses"]:
            if i not in self.lookup_table:
                if i in self.flattened_items:
                    self.add_to_tree(self.flattened_items[i])

        # add to list, superparent the first one (otherwise its a graph)
        first_parent_id = item["superClasses"][-1]
        if first_parent_id in self.lookup_table:
            parent = self.lookup_table[item["superClasses"][-1]]
        else:
            parent = self.tree
        node = Node(**item)
        node.parent = parent
        self.lookup_table[item["id"]] = node

    def load_from_json(self, json_data, options=False):
        self.tree = self.import_tree(json_data)
        if options:
            self.options = [node.name for node in PreOrderIter(self.tree)]
