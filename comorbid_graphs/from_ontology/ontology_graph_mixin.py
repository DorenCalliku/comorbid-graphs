from .ontology_reader import OntologyReader


class OntologyGraphMixin(object):
    @classmethod
    def from_ontology(cls, json_data, node_type, name="Source", id=1):
        ontology_graph = cls(dict(name=name), node_type=node_type)
        ontology_graph._load_from_ontology(
            json_data=json_data, name=name, id=id, node_type=node_type
        )
        return ontology_graph

    def _load_from_ontology(self, json_data, name, id, node_type):
        """Takes a dictionary of preprocessed from OntologyReader,
        and creates an AnyTree from that for easy processing."""

        oreader = OntologyReader(json_data)
        self.flattened_items = oreader.get_flattened()
        del oreader

        self.lookup_table = {}
        # TODO
        self.tree = node_type(name=name, id=id)
        for val in self.flattened_items.values():
            self._add_to_tree(val, node_type)

    def _add_to_tree(self, item, node_type):
        # basic step of recursion
        if item["id"] in self.lookup_table:
            return

        if "superClasses" not in item:
            item["superClasses"] = []

        # if no superclasses, then add to source
        if item["superClasses"] is None or item["superClasses"] == []:
            node = node_type(name=item["name"], parent=self.tree)
            self.lookup_table[item["id"]] = node
            return

        # else, check first the superclasses
        for i in item["superClasses"]:
            if i not in self.lookup_table:
                if i in self.flattened_items:
                    self._add_to_tree(self.flattened_items[i], node_type=node_type)

        # add to list, superparent the first one (otherwise its a graph)
        first_parent_id = item["superClasses"][-1]
        if first_parent_id in self.lookup_table:
            parent = self.lookup_table[item["superClasses"][-1]]
        else:
            parent = self.tree
        node = node_type(**item)
        node.parent = parent
        self.lookup_table[item["id"]] = node
