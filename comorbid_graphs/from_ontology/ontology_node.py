from anytree import Node


class OntologyNode(Node):
    def __init__(self, name="default", parent=None, children=[], *args, **kwargs):
        """Quick Initializer for testing and defaulting"""
        super().__init__(name, parent, children, *args, **kwargs)
