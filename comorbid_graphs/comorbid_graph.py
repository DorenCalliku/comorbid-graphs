
from .from_ontology.ontology_graph_mixin import OntologyGraphMixin
from .mixins.tree_mixin import AnyTreeMixin, AnyTreeIOMixin
from .searchable import FilterableSubgraphMixin, SearchableMixin, LBLGraphMixin, SimpleSearchMixin, OrderableMixin
from .processable import ProcessableGraphMixin
from anytree import PreOrderIter, LevelOrderIter


class ComorbidGraph(
    AnyTreeMixin,
    AnyTreeIOMixin,
    OntologyGraphMixin,
    SearchableMixin,
    SimpleSearchMixin,
    OrderableMixin,
    FilterableSubgraphMixin,
    ProcessableGraphMixin,
    LBLGraphMixin,
):
    def __init__(self, json_data, node_type, assign_ids=False, root_name=None):
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

    def get_nodes(self):
        return [node for node in PreOrderIter(self.tree)]

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
        stats['leaves count'] = len(self.tree.leaves)
        stats['height'] = self.tree.height
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
        parent_name="Source",
    ):
        new_cg = cls(dict(name=parent_name), node_type=type(tree_node))
        new_cg.tree = tree_node
        return new_cg

    def select(self, node_name):
        node = self.find_node(node_name)
        if not node:
            return
        type(self).from_tree(node, parent_name=node_name)
        return node
