from .mixins.tree_mixin import AnyTreeMixin, AnyTreeIOMixin
from .from_ontology.ontology_graph import OntologyGraphMixin

from anytree import PreOrderIter, LevelOrderIter


class ComorbidGraph(AnyTreeMixin, AnyTreeIOMixin, OntologyGraphMixin):
    def __init__(self, json_data, node_type, assign_ids=False):
        u"""
        A generic tree graph based on json data.

        Keyword Args:
            json_data: Reading from a json or dict content.
            node_type: Can be anything from NodeTreeMixin. Suggested: ComorbidGraphNode.
            assign_ids: For data with no ids, assign ids automatically (good for graphing).
        """

        self.tree = self.import_tree(json_data, node_type=node_type)
        if assign_ids:
            id = 0
            for node in LevelOrderIter(self.tree):
                if not hasattr(node, "id"):
                    node.id = id
                    id += 1

    def set_options(self):
        self.options = [node.name for node in PreOrderIter(self.tree)]

    def get_nodes_n_edges(self, node=None, max_level=3):
        if not node:
            node = self.tree
        # filter children
        vals = [
            j
            for child in node.children
            for n in LevelOrderIter(child, maxlevel=max_level - 1)
            for j in n.get_node_edge()
        ]
        # get own node
        val_node = node.name + " " + str(node.id)
        if not hasattr(node, "type"):
            type = "search_for"
        else:
            type = node.type
        my_node = [{"data": {"id": val_node, "label": node.name, "type": type}}]
        return vals + my_node

    @classmethod
    def merge_trees(
        cls, json_list, parent_name="Source", parent_type="annotation", assign_ids=False
    ):
        tree = cls(
            {"name": parent_name, "id": 0, "type": parent_type, "children": json_list},
            assign_ids=assign_ids,
        )
        return tree
