from anytree import Node
from .searchable import LBLNodeMixin, FilterableNodeMixin
from .processable import LabelHandlerMixin, ProcessableNodeMixin
from .mixins.visualizable_mixin import VisualizableMixin


class ComorbidGraphNode(
    Node,                  # anytree
    FilterableNodeMixin,   # searchable group
    LBLNodeMixin,
    ProcessableNodeMixin,  # processing group
    LabelHandlerMixin,
    VisualizableMixin,     # visualizable
):
    def __init__(self, *args, **kwargs):
        u"""Quick Initializer for testing and defaulting"""

        super().__init__(*args, **kwargs)
        if not hasattr(self, "body"):
            self.body = None
        if not hasattr(self, "type"):
            self.type = "default"
        if not hasattr(self, "score"):
            self.score = 0
        if not hasattr(self, "annotation_list"):
            self.annotation_list = []

    def to_dict(self):
        dict_val = {
            "id": self.__dict__["id"],
            "name": self.__dict__["name"],
            "type": self.__dict__["type"],
            "score": self.__dict__["score"],
        }
        return dict_val

    def generate_link(self, *args, **kwargs):
        # OVERWRITE THIS FOR APPLICATION PURPOSES
        if not hasattr(self, "type"):
            return "/"
        return "/" + str(self.type)

    def get_node_edge(self):
        value = self.name + " " + str(self.id)
        node = {
            "data": {
                "id": value,
                "label": self.name,
                "href": self.generate_link(),
                "type": self.type,
            }
        }
        edge = None
        if self.parent:
            edge = {
                "data": {
                    "source": self.parent.name + " " + str(self.parent.id),
                    "target": value,
                }
            }
        return [node, edge] if edge else [node]

    def deep_copy(self, parent=None):
        dict_values = {}
        for att in dir(self):
            if att not in ["children", "parent"] and att in [
                "id",
                "name",
                "type",
                "score",
                "body",
                "description",
                "annotation_list",
            ]:
                dict_values[att] = getattr(self, att)
        node = type(self)(**dict_values)
        if parent:
            node.parent = parent
        node.children = [child.deep_copy(node) for child in self.children]
        return node
