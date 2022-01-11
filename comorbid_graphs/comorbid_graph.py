from .searchable import (
    FilterableGraphMixin,
    SearchableMixin,
    LBLGraphMixin,
    OrderableMixin,
    MergeableMixin,
)
from .processable import ProcessableGraphMixin, LabelHandlerMixin
from .mixins.tree_mixin import AnyTreeMixin, AnyTreeIOMixin
from .comorbid_graph_node import ComorbidGraphNode
from .from_ontology.ontology_graph_mixin import OntologyGraphMixin

from .io_utils import read_from_json, read_from_yaml, write_json, write_yaml
from anytree import PreOrderIter, LevelOrderIter


class ComorbidGraph(
    AnyTreeMixin,  # tree group
    AnyTreeIOMixin,
    SearchableMixin,  # search group
    MergeableMixin,
    OrderableMixin,
    LBLGraphMixin,
    FilterableGraphMixin,
    OntologyGraphMixin,  # ontology
    ProcessableGraphMixin,  # processing
    LabelHandlerMixin,
):
    def __init__(
        self, json_data, node_type=ComorbidGraphNode, assign_ids=True, root_name=None
    ):
        u"""
        A generic tree graph based on json data.

        Keyword Args:
            json_data: Reading from a json or dict content.
            node_type: Can be anything from NodeTreeMixin. Suggested: ComorbidGraphNode.
            assign_ids: For data with no ids, assign ids automatically (good for graphing).
        """

        self.tree = self.import_tree(json_data, node_type=node_type)
        if root_name:
            self.tree.name = root_name
        self.graph = None
        if assign_ids:
            id = 0
            for node in LevelOrderIter(self.tree):
                if not hasattr(node, "id"):
                    node.id = id
                    id += 1

    def get_names(self):
        return [node.name for node in PreOrderIter(self.tree)]

    def get_nodes(self, exclude_head=False):
        return [
            node
            for node in PreOrderIter(self.tree)
            if node != self.tree or not exclude_head
        ]

    def get_nodes_n_edges(self, node=None, maxlevel=3):
        if not node:
            node = self.tree
        # filter children
        return [
            j
            for n in LevelOrderIter(node, maxlevel=maxlevel)
            for j in n.get_node_edge()
        ]

    def describe(self):
        count, label_count = 0, 0
        for i in PreOrderIter(self.tree):
            count += 1
            label_count += len(i.annotation_list)

        stats = {
            "count": count,
            "label count": label_count,
        }
        stats["leaves count"] = len(self.tree.leaves)
        stats["height"] = self.tree.height
        return stats

    @classmethod
    def merge_trees(
        cls,
        json_list,
        node_type,
        parent_name="Source",
        parent_type="annotation",
        assign_ids=False,
    ):
        tree = cls(
            {"name": parent_name, "id": 0, "type": parent_type, "children": json_list},
            assign_ids=assign_ids,
            node_type=node_type,
        )
        return tree

    @classmethod
    def from_tree(
        cls,
        tree_node,
        title="search results",
    ):
        new_cg = cls(dict(name=""))
        new_cg.tree = tree_node
        new_cg.tree.name = title
        return new_cg

    @classmethod
    def from_yaml(cls, filepath):
        return cls(json_data=read_from_yaml(filepath))

    @classmethod
    def from_json(cls, filepath):
        return cls(json_data=read_from_json(filepath))

    def write(self, filepath, method="yaml"):
        data = self.export()
        if method == "json":
            write_json(filepath=filepath, data=data)
        else:
            write_yaml(filepath=filepath, data=data)
