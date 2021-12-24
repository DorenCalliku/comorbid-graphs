from anytree import AnyNode
from .mixins.visualizable_mixin import VisualizableMixin


class ComorbidGraphNode(AnyNode, VisualizableMixin):
    def __init__(self, *args, **kwargs):
        u"""Quick Initializer for testing and defaulting"""

        super().__init__(*args, **kwargs)
        if not hasattr(self, "type"):
            self.type = "annotation"

    def to_dict(self):
        dict_val = {
            "id": self.__dict__["id"],
            "name": self.__dict__["name"],
            "body": self.__dict__["body"],
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
