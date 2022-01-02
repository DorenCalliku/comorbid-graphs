from anytree import AnyNode
from .mixins.visualizable_mixin import VisualizableMixin
from .searchable import LBLNodeMixin, FilterableNodeMixin


class ComorbidGraphNode(AnyNode, VisualizableMixin, FilterableNodeMixin, LBLNodeMixin):
    def __init__(self, *args, **kwargs):
        u"""Quick Initializer for testing and defaulting"""

        super().__init__(*args, **kwargs)
        if not hasattr(self, "type"):
            self.type = "default"

    def to_dict(self):
        dict_val = {
            "id": self.__dict__["id"],
            "name": self.__dict__["name"],
            "type": self.__dict__["type"],
        }
        return dict_val

    def generate_link(self, *args, **kwargs):
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
                "body",
                "description",
            ]:
                dict_values[att] = getattr(self, att)
        node = type(self)(**dict_values)
        if parent:
            node.parent = parent
        node.children = [child.deep_copy(node) for child in self.children]
        return node
